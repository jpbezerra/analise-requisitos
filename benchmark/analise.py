#!/usr/bin/env python3
"""Calcula as métricas do benchmark a partir de respostas_brutas/*.jsonl.

Requer: pandas, numpy   (pip install pandas numpy)
Uso:    python analise.py --raw respostas_brutas --corpus corpus_requisitos.csv --out resultados

Intervalos de confiança: bootstrap percentil (2.000 reamostragens) sobre os
12 requisitos-base (cada base e suas 4 variantes formam um bloco).
O júri é calculado aqui, sem novas chamadas de API, a partir das respostas dos modelos individuais.
"""
import argparse, glob, json, os
import numpy as np
import pandas as pd

SCORES = ["completeness", "unambiguity", "verifiability", "consistency"]
DEFECTS = ["ambiguity", "incompleteness", "non_verifiability", "inconsistency"]
ALL_CLASSES = ["none"] + DEFECTS
RNG = np.random.default_rng(42)
NBOOT = 2000

# ---------------- utilidades ----------------
def ci(vec, rng=RNG):
    """média e IC 95% (bootstrap percentil) de um vetor com um valor por requisito-base."""
    v = np.asarray(vec, dtype=float)
    v = v[~np.isnan(v)]
    if len(v) == 0:
        return np.nan, np.nan, np.nan
    idx = rng.integers(0, len(v), size=(NBOOT, len(v)))
    b = v[idx].mean(axis=1)
    return v.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5)

def alpha_interval(matrix):
    """alfa de Krippendorff (métrica de intervalo). matrix: unidades x avaliadores, NaN = ausente."""
    m = np.asarray(matrix, dtype=float)
    d_o_num, n = 0.0, 0
    allv = []
    for row in m:
        v = row[~np.isnan(row)]
        if len(v) < 2:
            continue
        mu = len(v)
        d_o_num += (2 * (mu * np.sum(v**2) - np.sum(v)**2)) / (mu - 1)
        n += mu
        allv.extend(v)
    if n < 2:
        return np.nan
    allv = np.array(allv)
    d_e = 2 * (n * np.sum(allv**2) - np.sum(allv)**2) / (n * (n - 1))
    if d_e == 0:
        return np.nan
    return 1 - (d_o_num / n) / d_e

def md_table(df, nd=3):
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            x = r[c]
            cells.append(f"{x:.{nd}f}" if isinstance(x, (float, np.floating)) and not pd.isna(x) else ("" if pd.isna(x) else str(x)))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)

# ---------------- carga e júri ----------------
def load(raw_dir, corpus_path):
    corpus = pd.read_csv(corpus_path)
    frames = [pd.read_json(p, lines=True) for p in sorted(glob.glob(os.path.join(raw_dir, "*.jsonl")))]
    if not frames:
        raise SystemExit(f"nenhum .jsonl em {raw_dir}")
    df = pd.concat(frames, ignore_index=True)
    n_err = int(df["error"].notna().sum()) if "error" in df else 0
    df = df[df["error"].isna()] if "error" in df else df
    df = df.dropna(subset=SCORES + ["defect_type", "decision"])
    df = df.merge(corpus[["id_requisito", "id_base", "versao", "defeito_injetado", "criterio_afetado"]],
                  left_on="requirement_id", right_on="id_requisito", how="left")
    return df, corpus, n_err

def make_jury(df):
    """Júri: mediana das notas; decisão 'revise' se >= metade dos juízes pedir revisão;
    tipo de defeito = mais votado entre os votos != 'none' (empate: ordem alfabética)."""
    models = sorted(df["model_label"].unique())
    rows = []
    for (rid, pert, rep), g in df.groupby(["requirement_id", "perturbation", "repetition"]):
        if g["model_label"].nunique() < len(models):
            continue
        rev = (g["decision"] == "revise").mean() >= 0.5
        votes = g.loc[g["defect_type"] != "none", "defect_type"].value_counts()
        top = sorted(votes[votes == votes.max()].index)[0] if (rev and len(votes)) else "none"
        r = {s: g[s].median() for s in SCORES}
        r.update(requirement_id=rid, perturbation=pert, repetition=rep, model_label="JURY",
                 decision="revise" if rev else "accept", defect_type=top if rev else "none",
                 id_base=g["id_base"].iloc[0], versao=g["versao"].iloc[0],
                 defeito_injetado=g["defeito_injetado"].iloc[0], criterio_afetado=g["criterio_afetado"].iloc[0])
        rows.append(r)
    return pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

# ---------------- métricas ----------------
def per_base(vals_by_base, bases):
    return [vals_by_base.get(b, np.nan) for b in bases]

def sensibilidade(df, bases):
    p0 = df[df.perturbation == "P0"]
    rows = []
    for m, g in p0.groupby("model_label"):
        for d in DEFECTS:
            x = g[g.versao == d]
            exact = x.assign(v=(x.defect_type == d)).groupby("id_base")["v"].mean().to_dict()
            strict = x.assign(v=(x.defect_type == d) & (x.decision == "revise")).groupby("id_base")["v"].mean().to_dict()
            flag = x.assign(v=(x.decision == "revise")).groupby("id_base")["v"].mean().to_dict()
            e, el, eh = ci(per_base(exact, bases)); f, fl, fh = ci(per_base(flag, bases))
            st, stl, sth = ci(per_base(strict, bases), rng=np.random.default_rng(4242))
            rows.append(dict(model=m, defect=d, exact_detection=e, exact_lo=el, exact_hi=eh,
                             exact_and_revise=st, strict_lo=stl, strict_hi=sth,
                             flagged_revise=f, flag_lo=fl, flag_hi=fh))
    return pd.DataFrame(rows)

def especificidade_f1(df, bases):
    p0 = df[df.perturbation == "P0"]
    rows = []
    for m, g in p0.groupby("model_label"):
        o = g[g.versao == "original"]
        acc = o.assign(v=(o.decision == "accept")).groupby("id_base")["v"].mean().to_dict()
        s, sl, sh = ci(per_base(acc, bases))
        f1s = []
        for c in ALL_CLASSES:
            tp = ((g.defeito_injetado == c) & (g.defect_type == c)).sum()
            fp = ((g.defeito_injetado != c) & (g.defect_type == c)).sum()
            fn = ((g.defeito_injetado == c) & (g.defect_type != c)).sum()
            f1s.append(2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else np.nan)
        mutants = g[g.versao != "original"]
        rows.append(dict(model=m, specificity_accept_originals=s, spec_lo=sl, spec_hi=sh,
                         false_positive_rate=1 - s,
                         false_negative_rate=1 - (mutants.decision == "revise").mean(),
                         macro_F1_5classes=np.nanmean(f1s)))
    return pd.DataFrame(rows)

def queda_criterio(df, bases):
    p0 = df[df.perturbation == "P0"]
    rows = []
    for m, g in p0.groupby("model_label"):
        for d in DEFECTS:
            crit = {"ambiguity": "unambiguity", "incompleteness": "completeness",
                    "non_verifiability": "verifiability", "inconsistency": "consistency"}[d]
            orig = g[g.versao == "original"].groupby("id_base")[crit].mean()
            mut = g[g.versao == d].groupby("id_base")[crit].mean()
            diff = (orig - mut).reindex(bases)
            mu, lo, hi = ci(diff.values)
            sd = np.nanstd(diff.values, ddof=1)
            rows.append(dict(model=m, defect=d, criterion=crit, mean_drop=mu, drop_lo=lo, drop_hi=hi,
                             effect_size_dz=mu / sd if sd else np.nan))
    return pd.DataFrame(rows)

def erro_banda(df, bases):
    p0 = df[df.perturbation == "P0"]
    rows = []
    for m, g in p0.groupby("model_label"):
        errs = []
        for _, r in g.iterrows():
            if r.versao == "original":
                for c in SCORES:
                    errs.append((r.id_base, c, max(0, 4 - r[c], r[c] - 5)))
            else:
                c = r.criterio_afetado
                errs.append((r.id_base, c, max(0, 1 - r[c], r[c] - 2)))
        e = pd.DataFrame(errs, columns=["id_base", "criterion", "err"])
        mu, lo, hi = ci(per_base(e.groupby("id_base")["err"].mean().to_dict(), bases))
        row = dict(model=m, band_MAE=mu, lo=lo, hi=hi)
        for c in SCORES:
            row[f"MAE_{c}"] = e[e.criterion == c]["err"].mean()
        rows.append(row)
    return pd.DataFrame(rows)

def estabilidade(df, bases):
    p0 = df[df.perturbation == "P0"]
    rows = []
    for m, g in p0.groupby("model_label"):
        piv = {s: g.pivot_table(index="requirement_id", columns="repetition", values=s) for s in SCORES}
        full = piv[SCORES[0]].dropna().index
        if len(full) == 0:
            continue
        same_def = g.groupby("requirement_id")["defect_type"].nunique().loc[full].eq(1)
        same_dec = g.groupby("requirement_id")["decision"].nunique().loc[full].eq(1)
        sd = np.mean([piv[s].loc[full].std(axis=1, ddof=0).mean() for s in SCORES])
        mat = np.vstack([piv[s].loc[full].values for s in SCORES])
        base_of = g.drop_duplicates("requirement_id").set_index("requirement_id")["id_base"].loc[full]
        per_b = same_dec.groupby(base_of).mean().to_dict()
        mu, lo, hi = ci(per_base(per_b, bases))
        rows.append(dict(model=m, n_items=len(full), same_decision_across_reps=mu, lo=lo, hi=hi,
                         same_defect_type_across_reps=same_def.mean(), mean_score_SD_across_reps=sd,
                         alpha_across_reps=alpha_interval(mat)))
    return pd.DataFrame(rows)

def robustez(df, bases):
    rows = []
    for m, g in df.groupby("model_label"):
        def get(p, r):
            x = g[(g.perturbation == p) & (g.repetition == r)].set_index("requirement_id")
            return x
        a1 = get("P0", 1)
        comps = [("ruido_P0rep1_vs_P0rep2", a1, get("P0", 2)),
                 ("P0_vs_P1_formatacao", a1, get("P1", 1)),
                 ("P0_vs_P2_ordem_contexto", a1, get("P2", 1))]
        for name, x, y in comps:
            idx = x.index.intersection(y.index)
            if len(idx) == 0:
                continue
            d_score = sum((x.loc[idx, s] - y.loc[idx, s]).abs() for s in SCORES) / len(SCORES)
            flip = (x.loc[idx, "decision"] != y.loc[idx, "decision"]).astype(float)
            chg = (x.loc[idx, "defect_type"] != y.loc[idx, "defect_type"]).astype(float)
            b = x.loc[idx, "id_base"]
            r = dict(model=m, comparison=name, n_pairs=len(idx))
            for lab, ser in [("mean_abs_score_change", d_score), ("decision_flip_rate", flip), ("defect_type_change_rate", chg)]:
                mu, lo, hi = ci(per_base(ser.groupby(b).mean().to_dict(), bases))
                r[lab] = mu; r[lab + "_lo"] = lo; r[lab + "_hi"] = hi
            rows.append(r)
    return pd.DataFrame(rows)

def efeito_pareado_perturbacoes(df, bases):
    """Diferença por base: mudança P0-P1/P2 menos ruído P0rep1-P0rep2.

    O IC reamostra bases inteiras, preservando os cinco itens de cada base.
    """
    rows = []
    for model, g in df.groupby("model_label"):
        def get(p, rep):
            return g[(g.perturbation == p) & (g.repetition == rep)].set_index("requirement_id")
        p0, rep2 = get("P0", 1), get("P0", 2)
        for perturbation in ("P1", "P2"):
            altered = get(perturbation, 1)
            ids = p0.index.intersection(rep2.index).intersection(altered.index)
            if len(ids) == 0:
                continue
            base = p0.loc[ids, "id_base"]
            noise_score = sum((p0.loc[ids, s] - rep2.loc[ids, s]).abs() for s in SCORES) / len(SCORES)
            pert_score = sum((p0.loc[ids, s] - altered.loc[ids, s]).abs() for s in SCORES) / len(SCORES)
            noise_flip = (p0.loc[ids, "decision"] != rep2.loc[ids, "decision"]).astype(float)
            pert_flip = (p0.loc[ids, "decision"] != altered.loc[ids, "decision"]).astype(float)
            row = dict(model=model, perturbation=perturbation, n_pairs=len(ids), n_bases=base.nunique())
            for name, difference in (("score_change_minus_noise", pert_score - noise_score),
                                     ("decision_flip_minus_noise", pert_flip - noise_flip)):
                row[name], row[name + "_lo"], row[name + "_hi"] = ci(
                    per_base(difference.groupby(base).mean().to_dict(), bases))
            rows.append(row)
    return pd.DataFrame(rows)

def inconsistencias_decisao_rotulo(df):
    """Respostas que rotulam um defeito, mas aceitam o requisito (sem o júri)."""
    g = df[(df.model_label != "JURY") & (df.decision == "accept") & (df.defect_type != "none")]
    return g[["model_label", "requirement_id", "perturbation", "repetition",
              "defeito_injetado", "defect_type", "decision"]].sort_values(
                  ["model_label", "requirement_id", "perturbation", "repetition"])

def concordancia(df):
    g = df[(df.perturbation == "P0") & (df.repetition == 1) & (df.model_label != "JURY")]
    models = sorted(g.model_label.unique())
    if len(models) < 2:
        return pd.DataFrame()
    rows = []
    for s in SCORES + ["ALL"]:
        cols = SCORES if s == "ALL" else [s]
        mats = []
        for c in cols:
            mats.append(g.pivot_table(index="requirement_id", columns="model_label", values=c).values)
        rows.append(dict(criterion=s, alpha_between_models=alpha_interval(np.vstack(mats))))
    dec = g.pivot_table(index="requirement_id", columns="model_label", values="decision", aggfunc="first")
    pair = [(dec[a] == dec[b]).mean() for i, a in enumerate(models) for b in models[i + 1:]]
    rows.append(dict(criterion="decision_pairwise_agreement", alpha_between_models=float(np.mean(pair))))
    return pd.DataFrame(rows)

def custo(df):
    g = df[df.model_label != "JURY"]
    return g.groupby("model_label").agg(calls=("run_id", "count"), tokens_in=("tokens_in", "sum"),
                                         tokens_out=("tokens_out", "sum"), mean_latency_s=("latency", "mean"),
                                         extra_attempts=("attempts", lambda s: int((s - 1).sum()))).reset_index().rename(columns={"model_label": "model"})

# ---------------- principal ----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="respostas_brutas")
    ap.add_argument("--corpus", default="corpus_requisitos.csv")
    ap.add_argument("--out", default="resultados")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    df, corpus, n_err = load(a.raw, a.corpus)
    bases = sorted(corpus.id_base.unique())
    if df.model_label.nunique() >= 2:
        df = make_jury(df)

    tabs = {
        "01_sensibilidade_por_defeito (RQ1, RQ4)": sensibilidade(df, bases),
        "02_especificidade_e_F1 (RQ1)": especificidade_f1(df, bases),
        "03_queda_de_nota_no_criterio_afetado (RQ1, RQ4)": queda_criterio(df, bases),
        "04_erro_em_relacao_a_faixa_esperada": erro_banda(df, bases),
        "05_estabilidade_entre_repeticoes (RQ2, RQ3)": estabilidade(df, bases),
        "06_robustez_a_mudancas_superficiais (RQ2, RQ3)": robustez(df, bases),
        "07_concordancia_entre_modelos": concordancia(df),
        "08_custo_e_tempo": custo(df),
        "10_efeito_pareado_perturbacoes (RQ2)": efeito_pareado_perturbacoes(df, bases),
        "11_inconsistencias_decisao_rotulo (auditoria)": inconsistencias_decisao_rotulo(df),
    }
    md = ["# Resultados do benchmark\n",
          f"Respostas válidas: {len(df[df.model_label != 'JURY'])}; falhas técnicas registradas e excluídas: {n_err}.",
          "Intervalos: bootstrap percentil 95% sobre os requisitos-base. 'JURY' = agregação dos modelos individuais.\n"]
    for name, t in tabs.items():
        fn = name.split(" ")[0] + ".csv"
        t.to_csv(os.path.join(a.out, fn), index=False)
        md += [f"## {name}\n", md_table(t) if len(t) else "_sem dados suficientes_", ""]
    # RQ4: ranking de dificuldade (média entre modelos individuais)
    q = tabs["03_queda_de_nota_no_criterio_afetado (RQ1, RQ4)"]
    q = q[q.model != "JURY"].groupby(["defect", "criterion"], as_index=False)["mean_drop"].mean().sort_values("mean_drop")
    md += ["## 09_dificuldade_por_dimensao (RQ4: menor queda = dimensão mais difícil de avaliar)\n", md_table(q), ""]
    q.to_csv(os.path.join(a.out, "09_dificuldade_por_dimensao.csv"), index=False)
    open(os.path.join(a.out, "resumo.md"), "w", encoding="utf-8").write("\n".join(md))
    print("ok ->", os.path.join(a.out, "resumo.md"))

if __name__ == "__main__":
    main()

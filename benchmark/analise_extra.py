#!/usr/bin/env python3
"""Análises complementares (acerto estrito e sensibilidade à exclusão de itens do gabarito em dúvida).

Uso: python analise_extra.py [--raw respostas_brutas] [--corpus corpus_requisitos.csv] [--out resultados]
Reutiliza analise.py (mesmo júri, mesmo bootstrap sobre as bases).
Saídas: 10_acerto_rotulo_e_estrito.csv, 11_sensibilidade_exclusao_gabarito.csv
"""
import argparse, os
import numpy as np
import pandas as pd
import analise as A

DOUBT = ["B06", "B07", "B11"]  # bases cuja variante AMB tem dúvida no gabarito


def label_strict(df, bases):
    """Acerto do rótulo e acerto estrito (rótulo certo E decisão 'revise'), em P0, por modelo e defeito."""
    p0 = df[df.perturbation == "P0"]
    rows = []
    for m, g in p0.groupby("model_label"):
        for d in A.DEFECTS:
            x = g[g.versao == d]
            lab = x.assign(v=(x.defect_type == d)).groupby("id_base")["v"].mean().to_dict()
            st = x.assign(v=(x.defect_type == d) & (x.decision == "revise")).groupby("id_base")["v"].mean().to_dict()
            l, ll, lh = A.ci(A.per_base(lab, bases)); s, sl, sh = A.ci(A.per_base(st, bases))
            rows.append(dict(model=m, defect=d, label_acc=l, label_lo=ll, label_hi=lh,
                             strict_acc=s, strict_lo=sl, strict_hi=sh))
    return pd.DataFrame(rows)


def metrics(df, bases, drop_amb_of=()):
    """Métricas-chave sobre as bases dadas; drop_amb_of remove só a variante 'ambiguity' dessas bases."""
    d = df[df.id_base.isin(bases)]
    d = d[~((d.versao == "ambiguity") & d.id_base.isin(drop_amb_of))]
    p0 = d[d.perturbation == "P0"]
    out = {}
    # rótulo e decisão em ambiguidade (média sobre os 4 modelos individuais, P0)
    ind = p0[p0.model_label != "JURY"]
    amb = ind[ind.versao == "ambiguity"]
    out["amb_label_acc"] = (amb.defect_type == "ambiguity").mean()
    out["amb_flagged"] = (amb.decision == "revise").mean()
    out["amb_no_defect"] = (amb.defect_type == "none").mean()
    # confusão da falta de verificabilidade, 4 modelos x 5 condições
    nv = d[(d.model_label != "JURY") & (d.versao == "non_verifiability")]
    out["nv_as_ambiguity"] = (nv.defect_type == "ambiguity").mean()
    out["nv_label_acc"] = (nv.defect_type == "non_verifiability").mean()
    # macro-F1 por modelo
    for m, g in p0.groupby("model_label"):
        f1s = []
        for c in A.ALL_CLASSES:
            tp = ((g.defeito_injetado == c) & (g.defect_type == c)).sum()
            fp = ((g.defeito_injetado != c) & (g.defect_type == c)).sum()
            fn = ((g.defeito_injetado == c) & (g.defect_type != c)).sum()
            f1s.append(2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else np.nan)
        out[f"F1_{m}"] = np.nanmean(f1s)
    # RQ4: queda média de nota por dimensão (modelos individuais) e ordem
    q = A.queda_criterio(d[d.model_label != "JURY"], sorted(d.id_base.unique()))
    drop = q.groupby("defect")["mean_drop"].mean()
    for k, v in drop.items():
        out[f"queda_{k}"] = v
    out["ordem_dificuldade"] = " < ".join(drop.sort_values().index)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="respostas_brutas")
    ap.add_argument("--corpus", default="corpus_requisitos.csv")
    ap.add_argument("--out", default="resultados")
    a = ap.parse_args()
    df, corpus, _ = A.load(a.raw, a.corpus)
    bases = sorted(corpus.id_base.unique())
    df = A.make_jury(df)

    ls = label_strict(df, bases)
    ls.to_csv(os.path.join(a.out, "10_acerto_rotulo_e_estrito.csv"), index=False)
    n_inc = len(df[(df.model_label != "JURY") & (df.defect_type != "none") & (df.decision == "accept")])
    n_inc0 = len(df[(df.model_label != "JURY") & (df.perturbation == "P0") & (df.defect_type != "none")
                    & (df.decision == "accept")])
    print(f"respostas com rótulo de defeito e decisão 'accept': {n_inc} (P0: {n_inc0})")

    scen = {
        "todos (12 bases)": metrics(df, bases),
        "sem as 3 variantes AMB em dúvida": metrics(df, bases, drop_amb_of=DOUBT),
        "sem as 3 bases em dúvida (9 bases)": metrics(df, [b for b in bases if b not in DOUBT]),
    }
    sens = pd.DataFrame(scen).T.reset_index().rename(columns={"index": "cenario"})
    sens.to_csv(os.path.join(a.out, "11_sensibilidade_exclusao_gabarito.csv"), index=False)
    print(ls.round(2).to_string(index=False))
    print(sens.round(3).T.to_string())


if __name__ == "__main__":
    main()

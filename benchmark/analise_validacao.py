#!/usr/bin/env python3
"""Compara duas avaliações cegas (validacao/analista_A.csv, analista_B.csv) com o gabarito.
Uso: python analise_validacao.py   (na pasta benchmark/)  -> validacao/resumo_validacao.csv"""
import numpy as np, pandas as pd

corpus = pd.read_csv("corpus_requisitos.csv")
ids = pd.read_json("respostas_brutas/claude.jsonl", lines=True)[["requirement_id", "prompt_id", "perturbation"]]
ids = ids[ids.perturbation == "P0"].drop_duplicates("requirement_id")
g = corpus.merge(ids, left_on="id_requisito", right_on="requirement_id")[
    ["prompt_id", "id_requisito", "id_base", "versao", "defeito_injetado"]]
MAP = {"ambiguity": "ambiguidade", "incompleteness": "incompletude",
       "non_verifiability": "nao_verificabilidade", "inconsistency": "inconsistencia", "none": "nenhum"}
g["alvo"] = g.defeito_injetado.map(MAP)

def load(k):
    d = pd.read_csv(f"validacao/analista_{k}.csv")
    d["set"] = d.defeitos_presentes.fillna("nenhum").apply(
        lambda s: frozenset(x.strip() for x in str(s).split(";") if x.strip()) or frozenset(["nenhum"]))
    return d.set_index("prompt_id")

R = {k: load(k) for k in "AB"}
rows = []
for k, d in R.items():
    x = g.join(d, on="prompt_id")
    x["alvo_presente"] = [a in s for a, s in zip(x.alvo, x["set"])]
    x["exato"] = [s == frozenset([a]) for a, s in zip(x.alvo, x["set"])]
    x["extra"] = [bool(s - {a, "nenhum"}) and a != "nenhum" or (a == "nenhum" and s != {"nenhum"}) for a, s in zip(x.alvo, x["set"])]
    x["dec_ok"] = x.decisao == np.where(x.versao == "original", "aceitar", "revisar")
    x.to_csv(f"validacao/anotado_{k}.csv", index=False)
    R[k] = x
    mut = x[x.versao != "original"]; org = x[x.versao == "original"]
    rows.append(dict(analista=k, alvo_marcado_variantes=mut.alvo_presente.mean(), so_alvo_variantes=mut.exato.mean(),
                     defeito_alem_do_alvo_variantes=mut.extra.mean(), originais_sem_defeito=org.alvo_presente.mean(),
                     decisao_conforme_gabarito=x.dec_ok.mean()))
a, b = R["A"], R["B"]
def kappa(p, q):
    po = (p == q).mean(); pe = sum((p == c).mean() * (q == c).mean() for c in set(p) | set(q))
    return (po - pe) / (1 - pe) if pe < 1 else np.nan
for lab, m in [("kappa_decisao_A_vs_B", kappa(a.decisao, b.decisao))]:
    rows.append({"analista": lab, "decisao_conforme_gabarito": m})
al = a.set_index("prompt_id"); bl = b.set_index("prompt_id")
rows.append(dict(analista="concordancia_conjunto_defeitos_A_vs_B", decisao_conforme_gabarito=(al["set"] == bl["set"]).mean()))
pd.DataFrame(rows).to_csv("validacao/resumo_validacao.csv", index=False)
print(pd.DataFrame(rows).round(3).to_string(index=False))

# por tipo de variante
for k in "AB":
    x = R[k]
    print(f"\n[{k}] por variante: alvo marcado / só o alvo / defeito além do alvo")
    print(x.groupby("versao").agg(alvo=("alvo_presente", "mean"), so_alvo=("exato", "mean"), extra=("extra", "mean"),
                                  dec_ok=("dec_ok", "mean")).round(2).to_string())
# itens em dúvida
print("\nItens em dúvida e itens com discordância do gabarito (A e B):")
for i in ["B06-AMB", "B07-AMB", "B11-AMB"]:
    for k in "AB":
        r = R[k][R[k].id_requisito == i].iloc[0]
        print(i, k, sorted(r["set"]), r.decisao, "|", r.observacao)
bad = a.merge(b, on="prompt_id", suffixes=("_A", "_B"))
bad = bad[(~bad.alvo_presente_A) & (~bad.alvo_presente_B)]
print("\nAmbos NÃO marcam o alvo:")
for _, r in bad.iterrows():
    print(r.id_requisito_A, "alvo=", r.alvo_A, "A:", sorted(r.set_A), "B:", sorted(r.set_B))

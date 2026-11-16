# Além da concordância: robustez de LLMs na análise da qualidade de requisitos

Benchmark controlado que avalia LLMs como juízes da qualidade de requisitos de software:
12 requisitos-base × (1 original + 4 variantes com um defeito injetado), 4 modelos via OpenRouter,
3 repetições + 2 perturbações superficiais = 1.200 julgamentos.

| Pasta | Conteúdo |
| --- | --- |
| `benchmark/benchmark/` | corpus, `run_benchmark.py`, `analise.py`, respostas brutas, resultados e `graficos.ipynb` |
| `docs/` | rascunho do artigo por seções e `artigo_completo.md` |
| `docs/latex/` | artigo no modelo SBC (`artigo.tex`, `referencias.bib`, figuras e `artigo.pdf`) |

## Reproduzir

```
cd benchmark/benchmark
pip install pandas numpy matplotlib
echo OPENROUTER_API_KEY=sk-or-... > .env
python run_benchmark.py --config config.json
python analise.py --raw respostas_brutas --corpus corpus_requisitos.csv --out resultados
jupyter nbconvert --to notebook --execute --inplace graficos.ipynb
```

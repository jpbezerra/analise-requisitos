# Benchmark de LLMs como juízes de qualidade de requisitos

Início rápido (detalhes em `experimento-protocolo.md`):

    pip install pandas numpy
    cp config.example.json config.json        # preencha os IDs exatos dos modelos
    export GEMINI_API_KEY=...                 # e as demais chaves usadas
    python run_benchmark.py --config config.json --dry-run
    python run_benchmark.py --config config.json --limit 4     # teste curto
    python run_benchmark.py --config config.json               # execução completa (retomável)
    python analise.py --raw respostas_brutas --corpus corpus_requisitos.csv --out resultados

`config.mock.json` usa juízes simulados e serve só para testar o pipeline. Não use seus resultados no artigo.

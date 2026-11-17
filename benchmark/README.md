# Benchmark de LLMs como juízes de qualidade de requisitos

Início rápido a partir da pasta `benchmark/`:

    pip install pandas numpy
    python analise.py --raw respostas_brutas --corpus corpus_requisitos.csv --out resultados

`config.json` registra a configuração usada na coleta de 15–16/11/2026; `config.example.json` é um exemplo sem chave. Para **só refazer a análise**, nenhuma chave é necessária. Para uma **nova coleta**, revise custos e disponibilidade dos modelos, configure `OPENROUTER_API_KEY` no ambiente e execute primeiro `python run_benchmark.py --config config.json --dry-run`. O script é retomável, mas novas respostas não devem ser misturadas silenciosamente com as antigas. `config.mock.json` usa juízes simulados e serve só para testar o pipeline — nunca use seus resultados no artigo.

Saídas da análise: `01_sensibilidade_por_defeito.csv` distingue acerto do rótulo (`exact_detection`) de acerto do rótulo **com** decisão de revisão (`exact_and_revise`); `10_efeito_pareado_perturbacoes.csv` compara P1/P2 ao ruído nos mesmos itens e informa IC por 12 bases; `11_inconsistencias_decisao_rotulo.csv` lista respostas com defeito rotulado e decisão “aceitar”. Veja também [REVISAO_CORPUS.md](REVISAO_CORPUS.md) para as pendências do gabarito.

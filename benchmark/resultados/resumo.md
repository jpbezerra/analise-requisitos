# Resultados do benchmark

Respostas válidas: 1200; falhas técnicas registradas e excluídas: 0.
Intervalos: bootstrap percentil 95% sobre os requisitos-base. 'JURY' = agregação dos modelos individuais.

## 01_sensibilidade_por_defeito (RQ1, RQ4)

| model | defect | exact_detection | exact_lo | exact_hi | exact_and_revise | strict_lo | strict_hi | flagged_revise | flag_lo | flag_hi |
|---|---|---|---|---|---|---|---|---|---|---|
| JURY | ambiguity | 0.639 | 0.417 | 0.861 | 0.639 | 0.389 | 0.861 | 0.833 | 0.583 | 1.000 |
| JURY | incompleteness | 0.611 | 0.361 | 0.861 | 0.611 | 0.361 | 0.861 | 0.833 | 0.583 | 1.000 |
| JURY | non_verifiability | 0.333 | 0.111 | 0.556 | 0.333 | 0.111 | 0.556 | 1.000 | 1.000 | 1.000 |
| JURY | inconsistency | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| claude | ambiguity | 0.500 | 0.250 | 0.750 | 0.417 | 0.167 | 0.667 | 0.750 | 0.500 | 1.000 |
| claude | incompleteness | 0.667 | 0.417 | 0.917 | 0.583 | 0.333 | 0.833 | 0.833 | 0.583 | 1.000 |
| claude | non_verifiability | 0.250 | 0.000 | 0.500 | 0.250 | 0.083 | 0.500 | 1.000 | 1.000 | 1.000 |
| claude | inconsistency | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| gemini | ambiguity | 0.389 | 0.167 | 0.639 | 0.389 | 0.139 | 0.611 | 0.556 | 0.278 | 0.833 |
| gemini | incompleteness | 0.639 | 0.389 | 0.889 | 0.639 | 0.389 | 0.889 | 0.833 | 0.583 | 1.000 |
| gemini | non_verifiability | 0.472 | 0.194 | 0.750 | 0.472 | 0.222 | 0.750 | 0.944 | 0.833 | 1.000 |
| gemini | inconsistency | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| gpt-oss-120b | ambiguity | 0.222 | 0.056 | 0.417 | 0.222 | 0.056 | 0.417 | 0.333 | 0.111 | 0.583 |
| gpt-oss-120b | incompleteness | 0.639 | 0.389 | 0.861 | 0.639 | 0.389 | 0.861 | 0.806 | 0.583 | 1.000 |
| gpt-oss-120b | non_verifiability | 0.028 | 0.000 | 0.083 | 0.028 | 0.000 | 0.083 | 0.722 | 0.472 | 0.944 |
| gpt-oss-120b | inconsistency | 0.944 | 0.833 | 1.000 | 0.944 | 0.833 | 1.000 | 1.000 | 1.000 | 1.000 |
| openai | ambiguity | 0.806 | 0.667 | 0.944 | 0.806 | 0.639 | 0.944 | 0.944 | 0.833 | 1.000 |
| openai | incompleteness | 0.667 | 0.417 | 0.889 | 0.667 | 0.444 | 0.889 | 0.917 | 0.750 | 1.000 |
| openai | non_verifiability | 0.417 | 0.167 | 0.667 | 0.417 | 0.167 | 0.667 | 1.000 | 1.000 | 1.000 |
| openai | inconsistency | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## 02_especificidade_e_F1 (RQ1)

| model | specificity_accept_originals | spec_lo | spec_hi | false_positive_rate | false_negative_rate | macro_F1_5classes |
|---|---|---|---|---|---|---|
| JURY | 0.861 | 0.694 | 1.000 | 0.139 | 0.083 | 0.677 |
| claude | 0.917 | 0.750 | 1.000 | 0.083 | 0.104 | 0.636 |
| gemini | 1.000 | 1.000 | 1.000 | 0.000 | 0.167 | 0.683 |
| gpt-oss-120b | 0.944 | 0.861 | 1.000 | 0.056 | 0.285 | 0.488 |
| openai | 0.083 | 0.000 | 0.167 | 0.917 | 0.035 | 0.558 |

## 03_queda_de_nota_no_criterio_afetado (RQ1, RQ4)

| model | defect | criterion | mean_drop | drop_lo | drop_hi | effect_size_dz |
|---|---|---|---|---|---|---|
| JURY | ambiguity | unambiguity | 1.306 | 0.819 | 1.764 | 1.427 |
| JURY | incompleteness | completeness | 1.861 | 1.194 | 2.444 | 1.606 |
| JURY | non_verifiability | verifiability | 2.889 | 2.528 | 3.181 | 4.813 |
| JURY | inconsistency | consistency | 3.875 | 3.653 | 4.000 | 11.339 |
| claude | ambiguity | unambiguity | 1.111 | 0.750 | 1.472 | 1.654 |
| claude | incompleteness | completeness | 1.500 | 0.917 | 2.000 | 1.500 |
| claude | non_verifiability | verifiability | 2.889 | 2.556 | 3.194 | 4.882 |
| claude | inconsistency | consistency | 3.583 | 3.167 | 3.917 | 5.360 |
| gemini | ambiguity | unambiguity | 1.444 | 0.833 | 2.056 | 1.287 |
| gemini | incompleteness | completeness | 2.139 | 1.472 | 2.722 | 1.846 |
| gemini | non_verifiability | verifiability | 3.111 | 2.722 | 3.500 | 4.349 |
| gemini | inconsistency | consistency | 3.972 | 3.917 | 4.000 | 41.281 |
| gpt-oss-120b | ambiguity | unambiguity | 0.750 | 0.194 | 1.389 | 0.704 |
| gpt-oss-120b | incompleteness | completeness | 2.417 | 1.611 | 3.083 | 1.734 |
| gpt-oss-120b | non_verifiability | verifiability | 2.278 | 1.528 | 3.000 | 1.637 |
| gpt-oss-120b | inconsistency | consistency | 3.639 | 3.111 | 3.972 | 4.240 |
| openai | ambiguity | unambiguity | 0.861 | 0.417 | 1.333 | 1.032 |
| openai | incompleteness | completeness | 1.361 | 0.806 | 1.833 | 1.453 |
| openai | non_verifiability | verifiability | 2.167 | 1.750 | 2.556 | 2.907 |
| openai | inconsistency | consistency | 3.667 | 3.222 | 4.000 | 4.424 |

## 04_erro_em_relacao_a_faixa_esperada

| model | band_MAE | lo | hi | MAE_completeness | MAE_unambiguity | MAE_verifiability | MAE_consistency |
|---|---|---|---|---|---|---|---|
| JURY | 0.250 | 0.160 | 0.349 | 0.333 | 0.583 | 0.076 | 0.007 |
| claude | 0.205 | 0.125 | 0.295 | 0.292 | 0.444 | 0.042 | 0.042 |
| gemini | 0.319 | 0.243 | 0.403 | 0.444 | 0.764 | 0.069 | 0.000 |
| gpt-oss-120b | 0.476 | 0.340 | 0.635 | 0.292 | 1.097 | 0.431 | 0.083 |
| openai | 0.312 | 0.205 | 0.424 | 0.417 | 0.597 | 0.139 | 0.097 |

## 05_estabilidade_entre_repeticoes (RQ2, RQ3)

| model | n_items | same_decision_across_reps | lo | hi | same_defect_type_across_reps | mean_score_SD_across_reps | alpha_across_reps |
|---|---|---|---|---|---|---|---|
| JURY | 60 | 0.967 | 0.917 | 1.000 | 0.833 | 0.097 | 0.974 |
| claude | 60 | 1.000 | 1.000 | 1.000 | 0.983 | 0.031 | 0.984 |
| gemini | 60 | 0.967 | 0.917 | 1.000 | 0.867 | 0.094 | 0.965 |
| gpt-oss-120b | 60 | 0.883 | 0.817 | 0.950 | 0.750 | 0.272 | 0.832 |
| openai | 60 | 0.933 | 0.883 | 0.983 | 0.717 | 0.172 | 0.901 |

## 06_robustez_a_mudancas_superficiais (RQ2, RQ3)

| model | comparison | n_pairs | mean_abs_score_change | mean_abs_score_change_lo | mean_abs_score_change_hi | decision_flip_rate | decision_flip_rate_lo | decision_flip_rate_hi | defect_type_change_rate | defect_type_change_rate_lo | defect_type_change_rate_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|
| JURY | ruido_P0rep1_vs_P0rep2 | 60 | 0.140 | 0.104 | 0.175 | 0.033 | 0.000 | 0.083 | 0.150 | 0.067 | 0.233 |
| JURY | P0_vs_P1_formatacao | 60 | 0.165 | 0.121 | 0.212 | 0.000 | 0.000 | 0.000 | 0.050 | 0.000 | 0.117 |
| JURY | P0_vs_P2_ordem_contexto | 60 | 0.202 | 0.146 | 0.269 | 0.083 | 0.033 | 0.133 | 0.150 | 0.067 | 0.250 |
| claude | ruido_P0rep1_vs_P0rep2 | 60 | 0.050 | 0.025 | 0.079 | 0.000 | 0.000 | 0.000 | 0.017 | 0.000 | 0.050 |
| claude | P0_vs_P1_formatacao | 60 | 0.129 | 0.100 | 0.158 | 0.017 | 0.000 | 0.050 | 0.117 | 0.050 | 0.200 |
| claude | P0_vs_P2_ordem_contexto | 60 | 0.196 | 0.129 | 0.263 | 0.083 | 0.017 | 0.167 | 0.117 | 0.067 | 0.167 |
| gemini | ruido_P0rep1_vs_P0rep2 | 60 | 0.125 | 0.083 | 0.167 | 0.033 | 0.000 | 0.083 | 0.117 | 0.050 | 0.184 |
| gemini | P0_vs_P1_formatacao | 60 | 0.142 | 0.096 | 0.192 | 0.033 | 0.000 | 0.083 | 0.100 | 0.033 | 0.183 |
| gemini | P0_vs_P2_ordem_contexto | 60 | 0.142 | 0.100 | 0.183 | 0.017 | 0.000 | 0.050 | 0.083 | 0.033 | 0.133 |
| gpt-oss-120b | ruido_P0rep1_vs_P0rep2 | 60 | 0.438 | 0.283 | 0.638 | 0.100 | 0.033 | 0.183 | 0.217 | 0.100 | 0.350 |
| gpt-oss-120b | P0_vs_P1_formatacao | 60 | 0.471 | 0.354 | 0.604 | 0.067 | 0.017 | 0.117 | 0.150 | 0.067 | 0.267 |
| gpt-oss-120b | P0_vs_P2_ordem_contexto | 60 | 0.450 | 0.354 | 0.546 | 0.117 | 0.067 | 0.167 | 0.183 | 0.133 | 0.233 |
| openai | ruido_P0rep1_vs_P0rep2 | 60 | 0.225 | 0.146 | 0.300 | 0.050 | 0.000 | 0.100 | 0.217 | 0.133 | 0.317 |
| openai | P0_vs_P1_formatacao | 60 | 0.254 | 0.179 | 0.333 | 0.033 | 0.000 | 0.083 | 0.217 | 0.133 | 0.317 |
| openai | P0_vs_P2_ordem_contexto | 60 | 0.267 | 0.188 | 0.379 | 0.033 | 0.000 | 0.083 | 0.200 | 0.100 | 0.300 |

## 07_concordancia_entre_modelos

| criterion | alpha_between_models |
|---|---|
| completeness | 0.667 |
| unambiguity | 0.572 |
| verifiability | 0.710 |
| consistency | 0.894 |
| ALL | 0.740 |
| decision_pairwise_agreement | 0.789 |

## 08_custo_e_tempo

| model | calls | tokens_in | tokens_out | mean_latency_s | extra_attempts |
|---|---|---|---|---|---|
| claude | 300 | 169245.000 | 63210.000 | 2.288 | 1 |
| gemini | 300 | 120121.000 | 44971.000 | 3.164 | 0 |
| gpt-oss-120b | 300 | 134560.000 | 54849.000 | 1.541 | 26 |
| openai | 300 | 115515.000 | 42088.000 | 2.989 | 0 |

## 10_efeito_pareado_perturbacoes (RQ2)

| model | perturbation | n_pairs | n_bases | score_change_minus_noise | score_change_minus_noise_lo | score_change_minus_noise_hi | decision_flip_minus_noise | decision_flip_minus_noise_lo | decision_flip_minus_noise_hi |
|---|---|---|---|---|---|---|---|---|---|
| JURY | P1 | 60 | 12 | 0.025 | -0.015 | 0.067 | -0.033 | -0.083 | 0.000 |
| JURY | P2 | 60 | 12 | 0.062 | 0.021 | 0.106 | 0.050 | -0.017 | 0.117 |
| claude | P1 | 60 | 12 | 0.079 | 0.054 | 0.108 | 0.017 | 0.000 | 0.050 |
| claude | P2 | 60 | 12 | 0.146 | 0.092 | 0.204 | 0.083 | 0.017 | 0.167 |
| gemini | P1 | 60 | 12 | 0.017 | -0.042 | 0.075 | 0.000 | 0.000 | 0.000 |
| gemini | P2 | 60 | 12 | 0.017 | -0.025 | 0.058 | -0.017 | -0.050 | 0.000 |
| gpt-oss-120b | P1 | 60 | 12 | 0.033 | -0.079 | 0.154 | -0.033 | -0.100 | 0.033 |
| gpt-oss-120b | P2 | 60 | 12 | 0.012 | -0.175 | 0.188 | 0.017 | -0.067 | 0.100 |
| openai | P1 | 60 | 12 | 0.029 | -0.071 | 0.137 | -0.017 | -0.067 | 0.033 |
| openai | P2 | 60 | 12 | 0.042 | -0.050 | 0.142 | -0.017 | -0.067 | 0.033 |

## 11_inconsistencias_decisao_rotulo (auditoria)

| model_label | requirement_id | perturbation | repetition | defeito_injetado | defect_type | decision |
|---|---|---|---|---|---|---|
| claude | B03-INC | P0 | 1 | incompleteness | incompleteness | accept |
| claude | B03-INC | P0 | 2 | incompleteness | incompleteness | accept |
| claude | B03-INC | P0 | 3 | incompleteness | incompleteness | accept |
| claude | B03-INC | P1 | 1 | incompleteness | incompleteness | accept |
| claude | B07-O | P2 | 1 | none | incompleteness | accept |
| claude | B08-AMB | P0 | 1 | ambiguity | ambiguity | accept |
| claude | B08-AMB | P0 | 2 | ambiguity | ambiguity | accept |
| claude | B08-AMB | P0 | 3 | ambiguity | ambiguity | accept |
| claude | B08-O | P1 | 1 | none | incompleteness | accept |
| claude | B10-O | P0 | 1 | none | incompleteness | accept |
| claude | B10-O | P0 | 3 | none | incompleteness | accept |
| gemini | B04-AMB | P0 | 2 | ambiguity | incompleteness | accept |
| gemini | B04-AMB | P1 | 1 | ambiguity | incompleteness | accept |
| gemini | B07-O | P0 | 3 | none | incompleteness | accept |

## 09_dificuldade_por_dimensao (RQ4: menor queda = dimensão mais difícil de avaliar)

| defect | criterion | mean_drop |
|---|---|---|
| ambiguity | unambiguity | 1.042 |
| incompleteness | completeness | 1.854 |
| non_verifiability | verifiability | 2.611 |
| inconsistency | consistency | 3.715 |

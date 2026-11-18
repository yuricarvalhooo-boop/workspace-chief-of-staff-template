# Avaliações comportamentais dos agentes

Os casos determinísticos protegem a presença das regras críticas nas fontes canônicas e são executados localmente:

```
python scripts/run_behavior_evals.py --mode deterministic
```

`model.json` contém cenários e rubricas para avaliar a aplicação das regras por um modelo. O runner não chama API, modelo, serviço externo ou recurso pago; ele registra o estado dos casos existentes. Para inspecioná-los:

```
python scripts/run_behavior_evals.py --mode list-model
```



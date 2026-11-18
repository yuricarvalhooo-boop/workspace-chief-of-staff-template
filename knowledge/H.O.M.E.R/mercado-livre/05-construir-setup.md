---
{
  "id": "HOMER-mercado-livre-05",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "mercado-livre",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "b15f5b88e79a951bb2145b968a0d523ef3234e95c1ebd0fc60938f251411b25c",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 05-construir-setup — mercado-livre

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** mercado-livre. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

## Recomendacao pratica pro App Promos ML

```
~/Projetos/
├── app-promos-ml-cloud/      ← clone do repo Cloud (so olhar codigo, nao mexe)
└── app-promos-ml-prod/       ← clone do repo externo (mexe migrations via CLI aqui)
```

Pelos clones voce:
- Le o codigo gerado pelo Lovable em ambos
- Aplica migrations via CLI no externo
- Compara diferencas reais no codigo entre Cloud vs externo (otimo pra slide)

```bash
# Em ~/Projetos
diff -r app-promos-ml-cloud/src app-promos-ml-prod/src | less
```

---

## Visao do App Promos ML (exemplo de referencia)

- **Vibe**: Midas-inspired — preto profundo + ouro saturado, modern SaaS com peso operacional
- **Contexto**: Mercado Livre BR (amarelo + azul) — preto+ouro contrasta e diferencia, sem competir
- **Tema**: Dark default (jornada longa da pessoa operacional do exemplo). Toggle pra light disponivel
- **Accent variavel**: usuario escolhe entre 3 cores manter mesma logica, trocar so o tom:
  - **Ouro** (default Midas)
  - **Verde fluo** (esmeralda saturado)
  - **Azul fluo** (cyan-eletrico)
- **Personalidade**: tipografica Inter (clean, denso), tabelas como protagonistas, cards elevados sutis, hover discreto

---

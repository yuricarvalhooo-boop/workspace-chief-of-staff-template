---
{
  "id": "HOMER-mercado-livre-06",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "mercado-livre",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "d1124971c5553965535f1be600c24063bc621c5d9ab7caeb9a1732756ed42bdf",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 06-warnings-e-evoluir — mercado-livre

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** mercado-livre. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

## Casos pedagogicos do App Promos ML (gold pro evento)

### Caso 1 — security_invoker na view

**Avisou**: View criada com SECURITY DEFINER por padrao.
**Significa**: pode bypassar RLS das tabelas embaixo.
**Decisao**: corrigir pra `security_invoker = true`.
**Ensina**: builder bom **detecta o aviso e corrige sozinho** — observe o que ele faz na conversa.

### Caso 2 — policy_always_true (4x)

**Avisou**: 4 policies com `USING(true) WITH CHECK(true)`.
**Significa**: qualquer authenticated le/escreve qualquer linha.
**Decisao**: manter, e intencional pra app interno fechado.
**Ensina**: linter avisa, voce decide, documenta. NAO altera por reflexo.

### Caso 3 — RLS sem policy (hipotetico)

**Avisaria**: tabela X com RLS habilitada mas sem policy pra SELECT.
**Significa**: ninguem consegue ler nada. App quebra.
**Decisao**: criar policy ou desabilitar RLS (e isso e bug se o app precisa ler).
**Ensina**: RLS sem policy = quebra silencioso. Sempre testa com `SET ROLE authenticated`.

---

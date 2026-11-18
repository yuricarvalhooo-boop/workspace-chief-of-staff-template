---
{
  "id": "HOMER-lovable-06",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "lovable",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "d1124971c5553965535f1be600c24063bc621c5d9ab7caeb9a1732756ed42bdf",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 06-warnings-e-evoluir — lovable

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** lovable. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

## Tres camadas de aviso (saiba o que cada uma pega)

| Camada | Roda quando | Pega o que | Onde aparece |
|---|---|---|---|
| **Wiz** (Lovable, mai/2026) | Builder gera codigo | Pacote vuln/malicioso, API key hardcoded, misconfig de infra, CVE | Security view do Lovable + Wiz Code/Build scans |
| **Supabase Advisors** | On-demand, no Dashboard | RLS desligada, policy fraca, view SECURITY DEFINER, index faltando, query lenta | Dashboard → Database → Advisors |
| **ESLint + TS + Console** | Build do frontend + browser | unused var, any, hook deps, hydration, key prop, runtime errors | Build output Lovable + DevTools (F12) |

**Como isso muda o Reactive Learning**: voce NAO precisa decorar lista de pacotes ruins, regex de secret, ou tipos de CVE. Wiz pega antes. Voce foca em:

1. Ler o que cada camada **avisou** (nao ignorar so porque "passou no build")
2. Decidir bug vs intencional **no seu contexto**
3. Pegar o que **nenhuma camada pega**: logica de negocio, fluxo end-to-end, RLS de regra de negocio

---

## Onde ver os warnings

### Lovable Cloud
- Painel do projeto → Logs / Issues / Diagnostics (varia por versao Lovable)
- Frequentemente Lovable mostra inline na conversa quando aplica migration

### Supabase externo
- **Dashboard → Database → Advisors** (Performance, Security, Postgres)
- **SQL Editor**: alguns warnings aparecem ao executar
- **Authentication → Policies**: ve quais policies sao "always true"
- **CLI**: `supabase db lint` (roda local antes de aplicar)

### Frontend (ambos)
- Console do browser (F12)
- Build output do Lovable
- IDE local (Cursor, VS Code) com extensions ESLint + TypeScript

---

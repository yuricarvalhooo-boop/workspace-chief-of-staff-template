---
{
  "id": "HOMER-geral-06",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "d1124971c5553965535f1be600c24063bc621c5d9ab7caeb9a1732756ed42bdf",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 06-warnings-e-evoluir — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# LINTER & WARNINGS — Bateu na trava? Pede pra IA explicar

> Modulo do evento (~10 min). Sentado entre PROMPT_3 e PROMPT_4.
> **Filosofia**: voce NAO precisa decorar tipos de warning. Quando aparecer um, copia o erro e pergunta pra IA.

---

## A regra de ouro do "Reactive Learning"

```
1. Ve um warning ou erro                    → calma, e normal
2. Copia a mensagem inteira                 → ctrl+c
3. Cola pra IA (Claude/ChatGPT/Lovable)
   "O que esse aviso significa em palavras
    simples? E bug ou intencional? Como
    conserto se for bug?"
4. IA traduz + sugere fix                   → leia, decide
5. Aplica fix ou documenta a decisao        → segue
```

Esse fluxo e **mais valioso que decorar teoria**. Voce vai topar
warnings em apps que ainda nem existem, com tecnologias que ainda
nao foram inventadas. O que persiste e a **habilidade de pedir
explicacao boa**.

---

## Por que isso importa

Builder bom (Lovable, v0) gera codigo que **passa por validacao automatica** — linters de SQL, ESLint, TypeScript, Supabase Advisors, **e desde mai/2026, Wiz scanning dentro do Lovable**. Cada warning conta uma de duas historias:

1. 🐛 **Bug que voce nao percebeu** — ignora e o app vai quebrar em producao
2. ✅ **Decisao consciente que precisa documentacao** — o linter alerta porque a regra **geralmente** e bug, mas no SEU contexto e intencional

A diferenca entre **junior vibe-coder** e **dev real**: junior ignora os avisos. Dev real le, decide, documenta.

---

## Os 5 tipos de aviso que voce vai bater

### 1. Linter SQL / Supabase Advisor

Roda automaticamente no Supabase Dashboard → Database → Advisors. Categorias:

- **Performance**: indexes faltando, queries lentas
- **Security**: RLS desligada, policies fracas, views inseguras
- **Postgres**: features deprecated, sintaxe nao recomendada

**Exemplo real do App Promos ML (Lovable Cloud)**:
```
WARNING: 4 policies use USING(true) WITH CHECK(true)
HINT: Policy `authenticated full access` on `promo_scenarios` allows
      any authenticated user to read/write all rows
```

→ **Decisao**: app interno fechado, 2 users, e intencional. Documenta no proprio arquivo de migration.

### 2. RLS warnings

Os mais comuns:

| Warning | O que significa | Quando ignorar |
|---|---|---|
| "RLS disabled in public" | Tabela sem RLS habilitada | Nunca — sempre habilita |
| "policy_always_true" | `USING(true)` em uma policy | Se app interno fechado e voce documentou |
| "no_policy_for_action" | RLS habilitada mas faltou policy pra alguma operacao | Se voce quis bloquear de proposito |
| "auth_users_exposed" | Coluna `auth.users.email` exposta | Nunca — esconde com view filtrada |

### 3. View Security

```
WARNING: View `promo_current_state` was created with SECURITY DEFINER
HINT: Use `WITH (security_invoker = true)` to respect RLS of underlying tables
```

**O que e**:
- View padrao Postgres = `SECURITY DEFINER` (executa com permissao do criador)
- Bypassa RLS das tabelas embaixo
- `security_invoker = true` = view executa com permissao de **quem chama**, respeita RLS

**Quando ignorar**:
- Quase nunca. `security_invoker = true` e quase sempre o que voce quer
- Excecao real: view de admin que precisa ver tudo (raro)

**Como corrigir**:
```sql
ALTER VIEW promo_current_state SET (security_invoker = true);
```

### 4. ESLint / TypeScript warnings (frontend)

Builder gera codigo que pode ter:
- `unused variable` — variavel declarada mas nao usada
- `any type` — tipo TypeScript generico (preguica)
- `missing dependency in useEffect` — bug clasico de React
- `accessibility (a11y)` — botao sem aria-label, imagem sem alt

**Quando ignorar**: quase nunca em codigo que vai pra producao. `any` as vezes e ok em tipo de payload externo.

### 5. Console / runtime warnings

Aparecem no DevTools do browser quando voce roda o app:
- "Hydration mismatch" — server e client renderizaram diferente
- "Each child in a list should have a unique key prop" — bug de re-render React
- "Maximum update depth exceeded" — loop infinito de re-render
- "Failed to load resource: 401" — API rejeitou request

**Quando ignorar**: nunca. Esses sao bugs reais que vao quebrar pro user.

---

## Como ler bem um warning

Estrutura mental:

```
┌─────────────────────────────────────────┐
│ 1. O que esta avisando?                 │ → ler a mensagem completa
│ 2. Por que isso e geralmente ruim?      │ → entender a regra
│ 3. No MEU contexto, isso e bug ou OK?   │ → decisao consciente
│ 4. Se OK, documenta o por que           │ → comentario no codigo
│ 5. Se bug, conserta                     │ → ajusta e re-valida
└─────────────────────────────────────────┘
```

**Pergunta-chave**: "se eu mostrar isso pra um dev senior, ele aceitaria minha justificativa?"

---

## Templates de prompt pra "perguntar pra IA"

Cole no Claude / ChatGPT / chat do Lovable conforme o caso:

### Template 1 — Erro com mensagem tecnica
```
Estou recebendo o erro abaixo no [Supabase / Lovable / app]. Por
favor:
1. Explica o que significa em palavras simples (sem jargao tecnico)
2. Diz se isso e bug ou comportamento intencional pro meu caso
3. Se for bug, me da o passo-a-passo pra corrigir

Contexto do meu app: [1 linha — ex: "app interno de promocoes ML"]

Erro:
[COLA AQUI A MENSAGEM INTEIRA]
```

### Template 2 — Warning do linter (cinza, nao vermelho)
```
O linter do Supabase/builder esta alertando o seguinte aviso. Pra
cada warning:
1. Explica em 2 linhas o que e
2. Diz se vale corrigir agora ou se posso seguir
3. Se valer corrigir, me da o SQL ou o codigo pronto

Avisos:
[COLA AQUI OS WARNINGS]
```

### Template 3 — App nao funciona, sem erro claro
```
Meu app esta com comportamento estranho: [descreve]. Esperava [X]
mas acontece [Y]. Nao aparece erro vermelho, mas tem warnings amarelo
no console. Por favor:
1. Sugere o que pode estar acontecendo
2. Lista 3 coisas pra eu testar pra descobrir
3. Se precisar, me pede mais info

Contexto: [1-2 linhas do app]
```

---

## Como ensinar esse modulo no evento

```
0:00 — "Quem aqui ja viu uma luz amarela no painel do carro e ignorou?"
       (provoca rir + conexao com o tema)

0:30 — "Builder e seu painel do carro. Linter e o sensor."
       Mostra na tela os 4 warnings do App Promos ML.

2:00 — "Vamos analisar cada um."
       Caso 1: security_invoker → corrigiu = bom
       Caso 2: policy_always_true → mantem = decisao consciente

5:00 — "Agora um teste: olha esse outro warning [mostra outro de exemplo].
       Bug ou feature? Discutam em duplas."
       (interativo — alunos discutem 2 min)

7:00 — Discussao aberta. Mostra como dev senior reage a warnings.

9:00 — "Regra de ouro do framework Elo: NUNCA aceite o aviso sem
       perguntar 'no meu contexto, isso e bug ou intencional?'.
       Se nao souber responder, ainda nao sabe o suficiente."
```

---

## Pitfalls comuns ao ignorar warnings

| Voce ignorou | O que pode acontecer |
|---|---|
| RLS disabled | Vazamento de dados, qualquer user le tudo |
| security_invoker false em view | View bypassa RLS, vazamento parcial |
| policy_always_true em SaaS multi-tenant | Cliente A ve dados do cliente B |
| Hydration mismatch | UI quebra em producao, parece bug aleatorio |
| Missing useEffect dep | Estado fica stale, bugs estranhos no UI |
| 401 em API call | Feature simplesmente nao funciona pra alguns users |
| `any` type em payload critico | Bug em runtime que TypeScript pegaria |
| Index missing em tabela grande | Query lenta, app trava com >10k rows |
| Placeholder `<KEY>` nao substituido em SQL | Cron schedulado mas EF retorna 401, voce so descobre olhando `net._http_response` (P-36) |
| Drift UI×Schema (UI consulta `kind`, migration usou `trigger_kind`) | Tela vazia silenciosa, supabase-js retorna null sem erro (P-40) |
| Cron `succeeded` no pg_cron sem checar `net._http_response` | "Cron funciona", mas EF retorna 4xx ha dias — voce so notar quando faltar dado (P-36, P-39) |

---

## Categoria nova: Drift silencioso

Apos sessao 13/05, surgiram 3 padroes de drift que **nao aparecem em linter nenhum** — voce so percebe via observacao ativa:

### Drift de Placeholder
Voce cola SQL com `Bearer <KEY>` literal e esquece de substituir. SQL **aceita**, schedula. Cron roda. EF retorna 401. **Nenhum linter pega isso** porque sintaticamente esta correto. Catch: imediatamente apos schedule, valida JWT format via `regexp_match` + `length + jwt_parts == 3`.

### Drift UI×Schema
Plano original usa nomes A. Builder aplica migration com nomes B. Tela consulta nomes A. **Supabase JS retorna `null` em coluna inexistente sem warning**. Linter TypeScript nao pega porque tipo da resposta e `any` ou inferido vazio. Catch: roda `\d <tabela>` ou `SELECT column_name FROM information_schema.columns` antes de codar tela.

### Drift de Env Var
EF lê `Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")` mas o valor injetado no runtime pode estar dessincronizado com Dashboard (rotacao silenciosa). **Nenhum linter pega isso** porque a leitura do env e sintaticamente correta. Catch: pra HTTP outbound chained, prefira **Bearer pass-through** em vez de env var (ver `BEARER_PASSTHROUGH.md` (`BEARER_PASSTHROUGH.md`, no material original)).

**Heuristica geral**: warnings cobrem **codigo errado**. Drift cobre **codigo certo + estado errado**. Diferentes camadas, diferentes ferramentas.

| Camada | Ferramenta |
|---|---|
| Codigo errado (tipo, sintaxe, sem await) | Linter (ESLint, tsc) |
| RLS / security errada | Supabase Advisors |
| Estado errado em runtime (drift) | Smoke + observabilidade (sweep_tick_log, net._http_response) |
| Performance ruim | Supabase Performance Advisor + Lighthouse |

---

## Checklist antes de declarar "feature pronta"

```
☐ Migration aplicada sem erro
☐ RLS habilitada nas tabelas tocadas
☐ Cada tabela com policy ativa
☐ View com security_invoker=true (se acessa tabelas com RLS)
☐ Linter Supabase Advisors revisado (Security + Performance)
☐ Frontend sem warnings no build
☐ Console do browser limpo (F12 → Console)
☐ Testou com user authenticated real
☐ Testou refresh / logout / login de novo
☐ Decisoes consciente sobre warnings restantes documentadas
```

Aluno que segue esse checklist faz **codigo real**, nao "vibe code de demo".

---

## Conexao com framework Elo

Este modulo cobre uma parte da **Fase 03 (Evoluir)** do framework — sair do builder pra dev real **passa por dominar warnings**. Ate dominar, o aluno fica preso na Fase 02. Esse modulo e a ponte entre 02 e 03.

---

## Apos este modulo

1. ✅ Aluno sabe ler warnings (Supabase Advisors + ESLint + Console)
2. ✅ Aluno sabe diferenciar bug vs decisao consciente
3. ✅ Aluno sabe documentar decisoes (no codigo + commit message)
4. → Pode prosseguir pra construir features (PROMPT_4 e seguintes) com confianca de que aplicacao **nasce com qualidade**, nao "tudo verde por sorte"

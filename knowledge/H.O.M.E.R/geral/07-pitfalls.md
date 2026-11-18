---
{
  "id": "HOMER-geral-07",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "928e1cb3369e8a8c318b3852b7de5a9705e727ca7847e2d359332e4cd002b376",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 07-pitfalls — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# Pitfalls — 56 armadilhas reais (P-01 a P-56)

> Catálogo de pitfalls do build do App Promos ML. Aluno colou um erro? Procure aqui primeiro.
> Consolidado de 4 arquivos incrementais (P-01..41, P-42..50, P-51..54, P-55..56) — sem duplicação entre eles.

---

## Índice por categoria

1. [OAuth & Secrets](#oauth--secrets)
2. [RLS, Policies & Permissões](#rls-policies--permissões)
3. [Build & Deploy](#build--deploy)
4. [Stack & Tech Choice](#stack--tech-choice)
5. [Editor Lovable & Preview](#editor-lovable--preview)
6. [Schema & Migrations](#schema--migrations)
7. [API & Semantica do Provider Externo](#api--semantica-do-provider-externo)
8. [Prompt Engineering](#prompt-engineering)
9. [Princípios de Prevenção](#princípios-de-prevenção)

---

## OAuth & Secrets

### 🚩 P-01 — Whitespace invisível em secrets ⭐⭐⭐ (top trauma)

**Sintoma**: provider externo (ML, Google, Stripe) rejeita com erro genérico tipo "aplicativo não está pronto" ou "invalid configuration", mesmo com tudo aparentemente certo.

**Causa**: o secret (`ML_REDIRECT_URI`, `OAUTH_CALLBACK_URL`, etc.) tem espaços, tabs ou newlines invisíveis no fim. Veio do clipboard "sujo" — auto-format de editor, paste de doc, copy parcial.

**Como diagnosticar**: olha a URL final do request real (no navegador, durante o redirect OAuth). Procura `+` ou `%20` no fim de algum parâmetro:
```
redirect_uri=https%3A%2F%2F.../ml-oauth-callback++
                                                  ^^ 2 espaços codificados como ++
```

**Fix**:
1. Abre o painel de secrets (Supabase Dashboard → Settings → Edge Functions → Secrets, ou o equivalente do Lovable Cloud)
2. Edita o secret problemático → **apaga TUDO** → **digita à mão** (não paste)
3. Confere visualmente que não há espaço/cursor depois do último caractere
4. Salva

**Prevenção**:
- Sempre que possível, setar secrets via CLI com `printf %s 'valor'` (não `echo`, que adiciona newline)
- Em UI, digitar à mão em vez de paste
- Após salvar, fazer um teste mínimo (ex: `curl` simples) ou olhar a URL real numa inspeção

**Template pro aluno usar com IA**:
> *"Cola a URL exata do erro OAuth. Decodifica os parâmetros e me diz se algum tem espaço, newline, ou caractere invisível no final. Esses são bugs comuns em secrets pasteados."*

#### Variantes deste mesmo pitfall (vivenciadas)

**Variante A — Empresa Externo, 08/05/2026**
- Secret: `ML_REDIRECT_URI` no Supabase Dashboard
- Tinha 2 espaços invisíveis no fim
- Sintoma: ML rejeita "aplicativo não está pronto"
- URL real: `redirect_uri=...callback++` (2 espaços codificados como `++`)
- Fix: editar no Supabase Dashboard, apagar, digitar à mão

**Variante B — Empresa Cloud, 08/05/2026**
- Secret: `ML_REDIRECT_URI` no Lovable Cloud Secrets
- Provavelmente espaço/newline (no nome ou valor)
- Sintoma: ML redirecionou pra `lovable.app/undefined` — JS lê env como undefined → string literal
- Fix: editar no Lovable Cloud Secrets, apagar, digitar à mão. **OU** deletar e recriar o secret do zero

**Conclusão**: este pitfall acontece em **qualquer plataforma de secrets** quando aluno paste de clipboard sujo. Lovable Cloud Secrets, Supabase Dashboard, Vercel Env Vars — todos vulneráveis. **Sempre digitar à mão, nunca paste.**

---

### 🚩 P-19 — OAuth scope mudou no código mas token salvo continua com scope antigo ⭐⭐ (caso real)

**Sintoma**: provedor externo (ML) retorna 403 / "unauthorized" ao chamar endpoint que exige scope que tu **acabou de adicionar** ao authorize_url. Mas a conta está conectada e tokens válidos.

Caso real Empresa 08/05/2026:
- POST `/seller-promotions/promotions/PRICE_DISCOUNT/items` retornou 403:
- `{"code":"PA_UNAUTHORIZED_RESULT_FROM_POLICIES","blocked_by":"PolicyAgent"}`
- Tela /configuracoes mostrava SCOPE: `offline_access read urn:global:admin:info:/r...` — **sem `write`**

**Causa**: refresh_token **não atualiza scopes**. Quando tu adiciona um scope novo (ex: `write`) no authorize_url, novos OAuth flows pegam, mas tokens **já salvos** ficam com scopes antigos pra sempre. Refresh apenas renova access_token, mantém scopes da autorização original.

**Fix**: 
1. Desconectar conta no app (deleta row em `auth_tokens`)
2. Reconectar — vai abrir tela de consent do provider novamente, com scopes atualizados
3. Confirmar novo scope na UI

**Pré-requisito esquecido**: o **app no painel do provider** (DevCenter ML, Google Console, etc) precisa ter o scope habilitado **na configuração do app**. Se app só permite `read`, requisitar `write` no authorize_url retorna scope reduzido (só `read`) — sem erro visível. Resultado: tu autoriza com `read+write+offline_access`, recebe só `read+offline_access`, e descobre só quando uma chamada falha 403.

**Caso real Empresa 08/05/2026 (continuação)**: ao investigar P-19, descobrimos que **DevCenter ML separa permissões por categoria com nível independente**:
- "Usuários": Leitura e escrita ✅
- "Promoções, cupons e descontos": **Leitura** apenas ⚠️ ← causa do 403
- "Publicação e sincronização": Leitura
- (etc)

Pra criar promo via `POST /seller-promotions/...`, a categoria **"Promoções..."** precisava estar em **"Leitura e escrita"** específicamente. Mudar essa única categoria + reconectar resolveu.

**Insight didático**: "OAuth scope tem 2 camadas" — vira slide do evento:

| Camada | Onde mora | Quem controla |
|---|---|---|
| App declara o que quer fazer | DevCenter ML → "Permissões" (por categoria, Leitura/Leitura+Escrita) | Dono do app |
| Request pede ao usuário | `?scope=read+write` no authorize_url | Código |
| Token recebe o que app pode ∩ user concede | Resposta do provider | ML/Google/etc |

Pedir `write` no authorize_url quando app declara só `read` na categoria → ML **silenciosamente reduz** scope concedido, **não retorna erro**. Bug aparece só quando a operação rola e PolicyAgent rejeita.

**Ordem de diagnóstico**:
1. Olha o scope na UI do app (campo SCOPE) — falta o que tu pediu?
2. Se sim: confere DevCenter/Console se app tem esse scope habilitado
3. Se app tem mas teu token não: **desconectar + reconectar**
4. Se reconectado e scope ainda incompleto: app não tem permissão concedida pelo provider (pedir aprovação ou usar tipo diferente)

**Prevenção**:
- Sempre confere scope salvo após primeiro OAuth (campo SCOPE na UI ou query em `auth_tokens.scope`)
- Quando alterar scope no código, **descarta tokens antigos** automaticamente OU força reconexão
- Pro evento, apresenta como princípio: *"Token guarda os scopes do momento que foi gerado. Mudou scope no código? Token velho está obsoleto."*

**Template pro aluno usar com IA**:
> *"Recebo 403 unauthorized chamando [endpoint X] mas app está conectado e token válido. Acabei de adicionar scope `write` no authorize_url. O token salvo no banco tem o scope novo? Como verifico e como forço reconexão?"*

---

### 🚩 P-03 — Refresh token rotation esquecido

**Sintoma**: OAuth funciona na primeira conexão. Algumas horas depois, ao tentar renovar, ML retorna `invalid refresh_token`. Conexão quebra silenciosamente.

**Causa**: ML (e outros providers) **rotaciona refresh_token a cada uso**. O response do `grant_type=refresh_token` inclui um `refresh_token` **NOVO**. Se o código preserva o antigo no UPDATE, próxima renovação quebra.

**Fix**: na EF de refresh, ao fazer UPDATE em `auth_tokens`, **substituir** `refresh_token` pelo novo retornado:
```ts
const { access_token, refresh_token: newRefresh, expires_in } = await response.json();
await sb.from("auth_tokens").update({
  access_token,
  refresh_token: newRefresh, // <- crítico
  expires_at: new Date(Date.now() + expires_in * 1000),
}).eq("ml_user_id", ml_user_id);
```

**Prevenção**: sempre que builder propor código de refresh, verificar manualmente se o `refresh_token` novo é gravado (nem todo provider rotaciona, mas ML sim).

---

### 🚩 P-04 — `APP_URL` derivado de Origin/Referer no callback OAuth

**Sintoma**: callback OAuth funciona, salva token, mas o redirect final pra `${APP_URL}/configuracoes?connected=true` cai em URL errada ou em branco.

**Causa**: callback é chamado pelo redirect do provedor OAuth (ex: ML → callback). Os headers `Origin` e `Referer` nessa request **vêm do provedor**, não do teu app. São inúteis ou enganosos pra reconstruir a URL do app.

**Fix**: forçar `APP_URL` como secret obrigatório, sem fallback de Origin/Referer:
```ts
const appUrl = Deno.env.get("APP_URL");
if (!appUrl) throw new Error("APP_URL not configured");
return Response.redirect(`${appUrl}/configuracoes?connected=true`, 302);
```

**Prevenção**: ao revisar plano de OAuth gerado por builder, sempre buscar a frase "derivar de Origin/Referer" — se aparecer, pedir mudança pra secret obrigatório.

---

## RLS, Policies & Permissões

### 🚩 P-06 — Builder propõe lock-down RLS prematuro ⭐⭐ (armadilha didática)

**Sintoma**: depois de criar Design System ou Skeleton, builder mostra um SQL "Modify database" com policies multi-tenant tipo `ml_user_id = current_ml_user_id()`. Aluno aceita por reflexo (parece "mais seguro"). Depois `/cenarios` aparece **vazia** mesmo com dados no banco.

**Causa**: a função `current_ml_user_id()` lê de `auth_tokens`, que está **vazia** (OAuth ainda não rodou). Retorna NULL. Policy `ml_user_id = NULL` = false pra qualquer linha. UI bloqueada.

Builder está sendo "secure by default" demais pra estágio de MVP single-tenant.

**Fix**: rejeitar o lock-down. Manter `USING(true) WITH CHECK(true)` enquanto MVP é single-tenant.

**Prevenção** — regra de bolso pro aluno:
> *"Se o builder sugerir mudança de segurança e você ainda é a única conta usando o app, recuse. Aceita o lock-down só quando tiver mais de 1 conta/usuário real."*

**Template pro aluno usar com IA**:
> *"O builder está sugerindo essas policies novas: [cola SQL]. Meu app está em MVP, sou o único usuário ainda. Vale a pena aplicar agora ou posso adiar pra quando tiver mais de 1 conta usando?"*

---

### 🚩 P-07 — `permission denied` mesmo com login correto

**Sintoma**: usuário logado, RLS habilitada, policy "authenticated full access" criada — mas SELECT/INSERT retorna `permission denied`.

**Causa**: além de RLS, Postgres tem **GRANTs** por role. Se a tabela não tem `GRANT ... TO authenticated`, RLS nem chega a ser avaliada — Postgres bloqueia antes. Acontece quando o setup do Supabase tem "Automatically expose tables" desligado.

**Fix**:
```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON public.<tabela> TO authenticated;
```

**Prevenção**: ao criar tabela manualmente (ou via migration que esqueceu de grant), sempre adicionar grants explícitos pra `authenticated`.

---

### 🚩 P-08 — View `SECURITY DEFINER` por padrão bypassa RLS

**Sintoma**: Supabase Advisors avisa "View created with SECURITY DEFINER. Use security_invoker=true to respect RLS".

**Causa**: por padrão, view Postgres executa com permissão de **quem criou** (geralmente `postgres`/superuser) — bypassa RLS das tabelas subjacentes.

**Fix**:
```sql
ALTER VIEW <view> SET (security_invoker = true);
```

**Prevenção**: sempre `security_invoker = true` em apps com RLS. Builder bom corrige sozinho — se não, pede.

---

## Build & Deploy

### 🚩 P-09 — Build warning vira erro fatal em produção ⭐⭐ (caso real)

**Sintoma**: preview funciona perfeitamente. Tu clica "Publish" / "Deploy". Build falha com:
```
build failed with exit status 1: <pacote>" from "src/.../client.ts".
This is most likely unintended because it can break your application at runtime.
If you do want to externalize this module explicitly add it to
`build.rollupOptions.external`
```

**Causa**: pacote (ex: `@supabase/supabase-js`) sendo "externalizado" pelo Rollup no build SSR. Vite em dev é tolerante (warning), mas build de produção é fatal. Cloudflare Workers/edge runtimes não conseguem resolver o módulo em runtime → quebra.

**Fix**: pedir builder pra adicionar `noExternal` no vite config (caso TanStack Start + `@lovable.dev/vite-tanstack-config`):
```ts
export default defineConfig({
  tanstackStart: { server: { entry: "server" } },
  vite: {
    ssr: {
      noExternal: [
        '@supabase/supabase-js',
        '@supabase/auth-js',
        '@supabase/realtime-js',
        '@supabase/postgrest-js',
        '@supabase/storage-js',
        '@supabase/functions-js',
      ],
    },
  },
});
```

**Prevenção**: **sempre tentar publish antes de assumir que tá tudo OK**. Build de prod é mais rigoroso que dev. Preview pode mentir.

**Template pro aluno**:
> *"O build de publish falhou com [erro]. O preview funcionava. Provavelmente é warning que virou erro em produção — explica em palavras simples e me dá o fix."*

---

## Stack & Tech Choice

### 🚩 P-11 — TanStack Start vs Vite SPA: stack frontend é eixo independente do backend

**Confusão comum**: aluno acha que "Lovable Cloud não suporta Edge Functions" porque ao criar projeto novo viu o builder propor "server routes" em vez de EFs.

**Verdade**: a partir de **20/04/2026**, projetos novos no Lovable nascem com `tanstack_start_ts` (TanStack Start, SSR). Antes era `vite_react_shadcn_ts` (Vite SPA, client-only).

Matriz real:

| Backend | Frontend | Onde mora "código de servidor" |
|---|---|---|
| Cloud + Vite SPA | client-only | Supabase Edge Functions |
| **Cloud + TanStack Start** | SSR | Server routes (`src/routes/api/*`) ← idiomático |
| Externo + Vite SPA | client-only | Supabase Edge Functions |
| **Externo + TanStack Start** | SSR | Pode escolher: server routes OU EFs Supabase |

**TanStack Start NÃO bloqueia Supabase EFs** — só não é idiomático pra rotas internas. **Pra OAuth, EF Supabase é melhor mesmo em TanStack** (URL estável, callback público).

**Prevenção**: sempre confere o `tech_stack` do projeto no Lovable (campo na config). Se for `tanstack_start_ts`, espera arquitetura SSR. Se for `vite_react_shadcn_ts`, espera SPA.

---

### 🚩 P-11b — "Server routes ou Edge Functions?" — capabilities equivalentes pra 95% dos casos

**Confusão comum**: aluno cria projeto TanStack Start, builder pergunta *"Server routes do TanStack ou Edge Functions Supabase?"* e ele trava — não sabe se Server routes têm o mesmo poder que EFs.

**Verdade**: capability-wise, **são equivalentes pra 95% dos casos**:

| Capability | Server routes | Edge Functions |
|---|---|---|
| Acesso DB (bypass RLS) | ✅ supabaseAdmin | ✅ service_role |
| Chamar APIs externas | ✅ fetch | ✅ fetch |
| Webhooks públicos | ✅ rota pública | ✅ EF pública |
| Validar JWT | ✅ middleware | ✅ verify_jwt |
| Retornar JSON/HTML/redirect | ✅ | ✅ |
| Streaming/SSE | ✅ Web Streams | ✅ Web Streams |

**Os 5% onde EF Supabase ganha**:

1. **Cron jobs** — `pg_cron` é nativo Postgres, EF é o callback dele. Pra cron mensal/diário, EF é mais limpo.
2. **URL estável pra webhook externo** — `*.supabase.co/functions/v1/*` não muda quando trocas de preview/branch/custom domain. Server route depende do domínio do app.
3. **Long-running** — Edge Runtime tem limites mais generosos que Cloudflare Workers padrão.
4. **OAuth callback** — beneficia da URL estável (mesma razão do webhook).

**Os 5% onde Server routes ganham**:

1. **Idiomático** ao stack TanStack — não duplica runtime
2. **Visibilidade no editor** — código aparece em `src/routes/api/`, junto com o resto
3. **Deploy unificado** — junto com frontend, sem step separado
4. **Sem cold start de outro runtime**

**Frase pronta pro slide do evento**:
> 🎯 *"Server routes do TanStack e Edge Functions Supabase têm capacidade equivalente pra quase tudo. A diferença real está em CRON e WEBHOOKS COM URL FIXA. Pra o resto — OAuth, autenticação, chamadas API, mutations no banco — escolhe o que for idiomático ao seu stack."*

**Decisões que valem regra simples**:

| Caso | Escolhe |
|---|---|
| OAuth callback (URL deve ficar estável) | EF Supabase (mesmo em TanStack) |
| Webhook que provider externo manda repetidamente | EF Supabase |
| Cron mensal/diário | EF Supabase + pg_cron |
| Mutation chamada do frontend logado | Server route (idiomático) |
| API pra dashboard/SPA | Server route |
| Lógica que precisa rodar em cada navegação | Server route (já está lá) |

---

## Schema & Migrations

### 🚩 P-15 — PROMPT_3 Foundation não é idempotente

**Sintoma**: tu recria projeto Lovable e vincula no mesmo Supabase de antes. Roda PROMPT_3 → erro `relation "promo_scenarios" already exists`.

**Causa**: PROMPT_3 atual usa `CREATE TABLE` puro (não `IF NOT EXISTS`). Roda 2x = quebra.

**Fix**: ao recriar app contra Supabase populado, **pular PROMPT_3**. Lovable lê o schema existente automaticamente ao vincular e gera os tipos TypeScript. Vai direto pro PROMPT_4.

**Prevenção** (pro evento): aluno cria Supabase do zero junto com app — sem conflito. Pra V2 do material, vale tornar PROMPT_3 idempotente.

---

### 🚩 P-18 — Frontend tenta SELECT direto em tabela protegida (`auth_tokens`)

**Sintoma**:
- Externo (Supabase): toast `permission denied for table auth_tokens`
- Cloud: query retorna vazio silencioso, toast "Conecte conta ML primeiro" mesmo com conta conectada

**Causa**: a tabela `auth_tokens` é intencionalmente super protegida — RLS habilitada, **zero policies pra authenticated/anon**, GRANTs **só pra service_role**. Foi assim que decidimos manter (P-06: rejeitar lock-down RLS prematuro nos `promo_*`, mas `auth_tokens` deve ser fortaleza). Frontend authenticated não pode SELECT direto.

Se o código do frontend tenta:
```ts
const { data } = await supabase.from('auth_tokens').select('ml_user_id')...
```
→ Postgres bloqueia antes mesmo da RLS rodar (sem GRANT pra authenticated).

**Fix**: usar o endpoint sancionado `ml-account-status` (já existe desde PROMPT_5) que roda server-side com service_role e retorna apenas `{ connected, ml_user_id, expires_at, created_at }` — nunca tokens.

```ts
// Externo (EF Supabase):
const { data } = await supabase.functions.invoke('ml-account-status');
const ml_user_id = data?.ml_user_id;

// Cloud (server fn TanStack):
const data = await getMLAccountStatus();
const ml_user_id = data?.ml_user_id;
```

**Caso real Empresa, 08/05/2026**: PROMPT_4B (CRUD de cenários) instruiu erradamente o frontend a ler `auth_tokens` direto pra pegar `ml_user_id` na hora de inserir cenário novo. Bateu permission denied. Fix em 1 linha — trocar pela chamada `ml-account-status` que já existia.

**Prevenção**: regra de ouro — *"Frontend nunca toca em `auth_tokens` direto. Tudo passa por endpoint que fala com service_role."* Essa regra é a razão de termos `ml-account-status`/`ml-account-disconnect` em vez de RLS scoped. **Mantém a separação.**

**Template pro aluno usar com IA**:
> *"Tô recebendo `permission denied for table auth_tokens` quando frontend tenta ler. Essa tabela é intencionalmente bloqueada. Como eu acesso esse dado via endpoint que rode server-side com service_role?"*

---

## API & Semantica do Provider Externo

> Categoria criada apos sessao 10/05 — testes empiricos da API ML revelaram 4 pitfalls de **semantica** (mesma palavra, significados diferentes) e **comportamento** (range invertido, multiplas adesoes). Cada um foi pego trazendo evidencia (UI, GET real, print) — padrao documentado em `THINKING_WITH_AI.md` (`THINKING_WITH_AI.md`, no material original).

### 🚩 P-25 — Doc oficial bloqueia WebFetch (403) — usar GET na API real

**Sintoma**: agente IA nao consegue ler doc oficial do ML via WebFetch — retorna 403 Forbidden.

**Causa**: muitos provedores (ML, Google, Meta) protegem doc oficial atras de Cloudflare ou auth + rate limit pesado. WebFetch generico falha.

**Workarounds**:
1. **GET na API real** com token valido — listar tipos, IDs, exemplos vivos
2. **MCP tools especificas** se houver (alguns provedores tem)
3. **Buscar versao em cache** (web.archive.org, mirrors)
4. **Pedir pro usuario colar o trecho** se for puntual
5. **Doc em outro idioma** (es-AR vs pt-BR) — as vezes 1 esta bloqueada e outra nao

**Como descobrimos**: pesquisa do tipo "compartilhado com ML" tentou doc oficial (`developers.mercadolivre.com.br/...promociones-y-acciones-promocionales`) → 403. Tentou variante `.com.ar` → 403 tambem. Pivotou pra `GET /seller-promotions/users/{id}` → retornou 9 promos da conta + tipos descobertos (DOD, LIGHTNING).

**Prevencao**: ao pesquisar API de provider, sempre considerar **2 caminhos paralelos**: doc + endpoint vivo. Endpoint vivo geralmente tem dado mais relevante pro caso especifico.

---

### 🚩 P-35 — Unique constraint em campo "metadata" quebra cenarios reais (caso real 12/05)

**Sintoma**: upload em massa de cenarios falha com `duplicate key value violates unique constraint "promo_scenarios_user_sku_uniq"` (ou similar). Schema gerado pelo builder ML/ai-builder assumiu que SKU e identificador unico.

**Causa**: SKU em e-commerce real **nao e unico por anuncio**. 1 familia de produtos (ex: "Masseira Basculante 25kg") pode ter:
- 5 MLBs diferentes (variantes de cor, ML re-publica, anuncio antigo + novo)
- Mesmo SKU base "90238-27477" em todos os 5

PROMPT_3 (foundation) ou builder default cria constraint `UNIQUE (ml_user_id, sku)` assumindo 1 SKU = 1 anuncio. Quebra no upload real.

**Caso real Empresa 12/05/2026**:
- Externo: `promo_scenarios_user_sku_uk` (UNIQUE CONSTRAINT)
- Cloud: `promo_scenarios_user_sku_uniq` (UNIQUE INDEX avulso, sem constraint correspondente)
- Cloud teve sintoma extra: `DROP CONSTRAINT IF EXISTS` nao removeu (porque era INDEX avulso). Precisou `DROP INDEX IF EXISTS`.

**Fix**:
```sql
ALTER TABLE promo_scenarios DROP CONSTRAINT IF EXISTS promo_scenarios_user_sku_uk;
DROP INDEX IF EXISTS promo_scenarios_user_sku_uniq;  -- caso seja index avulso
```

SKU vira metadata informativa. MLB e a chave real de identidade.

**Prevencao**:
- Pra cada campo "opcional/metadata", questione: "esse campo se REPETE no mundo real?". Se sim, **nao** crie unique constraint.
- Distingua **chave de identidade** (PK, MLB, ID externo unico) de **chave de busca** (CPF, telefone, email) de **metadata** (SKU, codigo interno, descricao).
- Quando builder propor migration com unique constraint, valide com 3 exemplos reais antes de aceitar.

**Template prompt pra IA**:
> *"Builder propos unique constraint em coluna X (tabela Y). No meu dominio, X pode repetir entre diferentes registros — exemplo: [cite 2-3 casos reais]. Re-avalie: essa constraint precisa existir, ou X e metadata? Se precisa, qual constraint composta seria correta?"*

---

## Infra & Cron

> Categoria criada apos sessao 13/05 — setup de batch sweep + pg_cron expos 6 pitfalls reais em ~3h. Auth de cron, placeholder em SQL, drift de env var, URL preview vs publish, drift UI×schema, extensions Postgres faltando. Tudo coisa que aparece em qualquer app com background job real.

### 🚩 P-36 — Placeholder `<KEY>` nao substituido em SQL → JWT invalido silencioso ⭐⭐ (caso real 13/05)

**Sintoma**: cron schedulado, `cron.job_run_details` mostra `status='succeeded'`, mas EF retorna 401 a cada invocacao com `UNAUTHORIZED_INVALID_JWT_FORMAT`. App nao processa nada e voce demora a notar porque pg_cron diz "succeeded" (o que de fato refere-se so a "request enfileirado", nao "request respondido OK").

**Causa**: voce colou o SQL do cron com `Bearer <SERVICE_ROLE_KEY>` e nao substituiu o placeholder pelo valor real antes de rodar. SQL aceita, cron schedula, mas o Bearer literal `Bearer <SERVICE_ROLE_KEY>` nao e JWT.

**Caso real Empresa 13/05**:
- responsável pelo exemplo rodou `cron.schedule(... 'Bearer <SERVICE_ROLE_KEY>' ...)`
- pg_cron disparou minutely, return_message="1 row" (sucesso do net.http_post)
- 2 invocacoes seguidas em `net._http_response`: `status_code=401, body='{"code":"UNAUTHORIZED_INVALID_JWT_FORMAT"}'`
- Validacao via MCP: `SELECT command FROM cron.job` mostrava `Bearer <SERVICE_ROLE_KEY>` literal

**Fix**: `cron.unschedule(...)` + re-schedule substituindo o placeholder pelo valor real.

**Prevencao**:
1. Imediatamente apos schedule, valida: `SELECT length(...), array_length(string_to_array(token, '.'), 1)` na key extraida. JWT valido tem **3 partes** (header.payload.signature) e length **~200-250 chars**. Se length<50 OR parts!=3, e placeholder.
2. Sempre olha `net._http_response` 2-3min apos schedule. `status_code=200` = OK. `4xx` = bug.
3. Mensagem mental: **"cron schedulado != cron funcionando"**. `succeeded` no pg_cron significa "request enfileirado", nao "request respondido com sucesso".

**Template SQL de auto-validacao** (cola depois de cada schedule):
```sql
-- valida JWT format imediatamente apos schedule
WITH bearer AS (
  SELECT (regexp_match(command, 'Bearer ([^''\s]+)'))[1] AS k
  FROM cron.job WHERE jobname='<seu-job>'
)
SELECT length(k) AS len,
       array_length(string_to_array(k, '.'), 1) AS jwt_parts,
       substring(k, 1, 12) AS first_chars
FROM bearer;
-- esperado: len > 100, jwt_parts = 3, first_chars comeca com 'eyJ'
```

---

### 🚩 P-37 — `ALTER DATABASE postgres SET app.*` bloqueado em Supabase managed ⭐ (caso real 13/05)

**Sintoma**: `ERROR: 42501: permission denied to set parameter "app.service_role_key"` ao tentar guardar secret via custom GUC.

**Causa**: Supabase Cloud restringe custom GUCs com namespace `app.*` em planos managed (free/pro). Apenas superuser pode, e voce nao tem esse role.

**Caso real Empresa 13/05**: tentei usar `ALTER DATABASE postgres SET app.service_role_key = '...'` pra esconder service_role do cron.job. Quebrou. Fallback: hardcode inline mesmo no `cron.schedule(...)`. Cron.job armazena em plain text, mas so role `postgres` (superuser do projeto) consegue ler — role `authenticated` nao acessa schema `cron`.

**Fix**: aceita inline no cron SQL e mitiga sabendo que so superuser ve. Tradeoff aceitavel pra MVP. Se for ambiente compartilhado com varios postgres-roles humanos, usa **Supabase Vault** (`vault.create_secret()` + `vault.decrypted_secrets`).

**Prevencao**:
- Antes de propor solucao com `current_setting('app.X')`, valida: roda `SELECT current_setting('app.test', true)` + `ALTER DATABASE postgres SET app.test='hello'`. Se erro 42501, vai direto pro fallback inline.
- Pro evento didatico: deixa o aluno saber que `ALTER DATABASE` so funciona em Postgres self-hosted ou em Supabase Vault. Em managed, hardcode no cron e regra RBAC + Vault sao os caminhos.

---

### 🚩 P-38 — `SUPABASE_SERVICE_ROLE_KEY` no env da EF != key visivel no Dashboard ⭐⭐ (caso real 13/05)

**Sintoma**: EF A chama EF B com `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}` e recebe 401. Mas se voce extrair a key do `cron.job` (que pegou do Dashboard) e chamar EF B via pg_net manual, retorna 200. **A mesma key funciona "de fora" e falha "de dentro".**

**Causa**: a key injetada em `Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")` no runtime do Supabase Edge pode estar **dessincronizada** com a key atual do Dashboard. Possiveis razoes:
- Rotacao silenciosa do JWT secret do projeto
- Migracao do sistema de keys (JWT legacy → publishable/secret format)
- EF deployada com key antiga que ficou cached

**Caso real Empresa 13/05**:
- `sweep-tick` (EF) chamava `promo-activate` (EF) com `Bearer ${SERVICE_ROLE}` → todas chamadas 401
- Invocacao manual de `promo-activate` via `pg_net` com a key extraida do `cron.job` → 200 OK
- Confirma: a key "do Dashboard" funciona. A key "do env da EF" nao.

**Fix idiomatico**: **Bearer pass-through**. EF A pega o Authorization que JA entra no request e repassa pra EF B:
```ts
// antes (bug)
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
fetch(url, { headers: { Authorization: `Bearer ${SERVICE_ROLE}` }});

// depois (resiliente)
const incomingAuth = req.headers.get("Authorization")!;
fetch(url, { headers: { Authorization: incomingAuth }});
```

Mantem `SERVICE_ROLE` apenas pro `createClient` interno (que conecta no Postgres via JWT secret consistente do projeto). HTTP outbound reusa o Bearer entrante.

**Prevencao**:
- Default arquitetural pra **qualquer chained EF**: pass-through > env var lookup.
- Auditoria: se uma EF lê `SUPABASE_SERVICE_ROLE_KEY` pra fazer HTTP outbound, isso e flag amarela. Ver `BEARER_PASSTHROUGH.md` (`BEARER_PASSTHROUGH.md`, no material original) pro padrao completo.
- Triangulacao 3 snapshots resolve esse bug em 5min: (1) key esperada (Dashboard) (2) key no env (decode JWT no log temporario) (3) key que cron envia (regexp_match no cron.job).

---

### 🚩 P-40 — Drift UI × Schema: tela consulta colunas que nao existem mais ⭐⭐ (caso real 13/05)

**Sintoma**: tela carrega sem erro visivel, lista esta vazia ou cards estao incompletos, mas o dado existe no DB. `SELECT * FROM table` direto via SQL retorna rows. Browser console mostra warnings ou silencio.

**Causa**: o **plano** original especificou colunas com nomes A (ex: `kind`, `totals.done`, `row_total`). A **migration aplicada pelo builder** usou nomes B (ex: `trigger_kind`, contadores diretos `total/done/failed`). A **tela** foi codada esperando A. Supabase client retorna `null` ou erro silencioso pras colunas inexistentes — UI fica vazia sem feedback.

**Caso real Empresa 13/05**:
- Plano original PROMPT_10 usava `sweep_jobs.kind` + `totals jsonb`
- Lovable Externo aplicou: `sweep_jobs.trigger_kind` + contadores diretos `total/done/failed/cancelled`
- Tela `/sweeps` consultando `kind` e `totals.done` retornou vazio
- Validacao via MCP: row existia no DB, mas com nomes diferentes do que UI esperava

**Fix**: peça pro builder mostrar diff entre **nomes propostos no plano** vs **nomes aplicados na migration** ANTES de codar a tela. Se divergiu, decide qual padronizar.

**Prevencao**:
1. **Adicione "9. CONSISTENCY UI×SCHEMA" na rubrica de revisao**: a UI consulta exatamente as colunas que a migration criou? Se nao, qual padronizar?
2. Sempre roda `\d <tabela>` (ou `SELECT column_name FROM information_schema.columns`) antes de codar tela que consulta tabela nova
3. **Pro evento**: quando aluno fizer 2 apps em paralelo (Cloud + Externo), MOSTRE o diff de schemas antes de mexer em UI. Drift e silencioso, voce so percebe quando tela aparece vazia

**Template prompt pra IA**:
> *"Antes de codar a tela /X, mostra o output de `\d <tabela>` da migration aplicada. Quero confirmar que os nomes de coluna que a UI vai consultar batem 1-pra-1 com o schema real. Aponta qualquer divergencia entre o plano original e a migration final."*

---

### 🚩 P-41 — `schema "cron" does not exist`: pg_cron/pg_net precisam migration, nao SQL editor (caso real 13/05)

**Sintoma**: `cron.schedule(...)` no SQL editor retorna `ERROR: 3F000: schema "cron" does not exist`. Mesmo em projeto novo Supabase. Tentativa de `CREATE EXTENSION pg_cron` no editor tambem falha por permissao.

**Causa**: `pg_cron` e `pg_net` exigem privilegios de superuser pra serem criadas. Supabase managed nao expõe esse privilegio no SQL editor comum. Habilita-las requer:
1. Migration (que roda com role elevado), ou
2. UI Supabase Dashboard → Database → Extensions (toggle ON)

**Caso real Empresa 13/05**:
- responsável pelo exemplo rodou `cron.schedule(...)` direto no SQL editor → erro 3F000
- Lovable Cloud propos migration: `CREATE EXTENSION IF NOT EXISTS pg_cron WITH SCHEMA extensions; CREATE EXTENSION IF NOT EXISTS pg_net WITH SCHEMA extensions; GRANT USAGE ON SCHEMA cron TO postgres;`
- Migration rodou OK, dai schedule funcionou

**Fix**:
```sql
-- via migration (precisa superuser, builder/Supabase CLI tem)
create extension if not exists pg_cron with schema extensions;
create extension if not exists pg_net with schema extensions;
grant usage on schema cron to postgres;
```

OU via Dashboard → Database → Extensions → habilitar pg_cron + pg_net.

**Prevencao**:
- Antes de planejar qualquer feature com cron, valida: `SELECT extname FROM pg_extension WHERE extname IN ('pg_cron','pg_net');` deve retornar 2 rows. Se nao, primeiro passo da migration e habilitar.
- Pro evento: tem alunos em Supabase Cloud (extensoes habilitaveis) e potencialmente em Lovable Cloud (que tambem usa Supabase mas pode ter extensoes diferentes ativadas por default). Default: assume **nao habilitado** ate provar.

---

## Prompt Engineering

> Categoria criada apos sessao 10/05 (parte 2). Foco: o builder nao "lê e infere" do mesmo jeito que voce — ele completa lacunas com palpite. Quando voce constroi 2 versoes em paralelo (Cloud + Externo, igual App Promos ML), as divergencias entre plans **revelam as lacunas do prompt**. Ver detalhe e exemplos em `THINKING_WITH_AI.md` (`THINKING_WITH_AI.md`, no material original) — secao "Escrevendo prompt que minimiza inferencia divergente".

### 🚩 P-26 — UI descrita em prosa vira inferencia divergente entre builders ⭐⭐ (caso real 10/05)

**Sintoma**: 2 builders (Cloud + Externo) recebem mesmo prompt, retornam plans com componentes UI diferentes (ex: 1 inclui sidebar+badge, outro nao).

**Causa**: prompt usa frase como "tela /aprovacoes com lista". Cada builder infere os componentes que **acha que voce quer** (sidebar item, badge contador, estado vazio, paginacao, ordenacao). Inferencias divergem.

**Caso real PROMPT_6 v2**: Cloud incluiu sidebar com badge contador refetch 30s. Externo nao mencionou sidebar. Mesma tela, mesmo proposito, UX divergente.

**Fix**: descreva UI em **bullets atomicos**, 1 elemento por linha. Header, campos, ordenacao, paginacao, estados (vazio/loading/erro), sidebar, badges, refetch — tudo explicito.

**Prevencao**: regra de ouro — se ler o bullet em voz alta nao reproduz a tela na cabeca, esta vago. Ver heuristica 2 em THINKING_WITH_AI (`./THINKING_WITH_AI.md#2-ui-atomica-em-bullets-nao-prosa`, referência do material original não incluída como arquivo local).

---

### 🚩 P-27 — Builder afirma endpoint "publico" que de fato exige auth ⭐⭐⭐ (caso real 10/05)

**Sintoma**: plan diz "endpoint X é publico, chama direto do browser sem token". Em runtime, retorna 403 — quebra a feature.

**Causa**: prompt mencionou endpoint sem declarar **contrato** (auth/request/response). Builder palpita com base em padrao comum ("GET /items é geralmente publico"), pode estar errado pro provider especifico.

**Caso real PROMPT_6 v2**: Externo afirmou que `/items/{mlb}?attributes=title,thumbnail` era publico. Validei via curl: 403 sem Bearer token. Browser do user nao tem token (esta server-side).

**Fix**: pra cada chamada externa, declare no prompt:
```
GET https://api.mercadolibre.com/items/{mlb}?attributes=title,thumbnail
  Auth: Bearer (precisa access_token)
  Response: { title: string, thumbnail: string }
  Erros: 403 sem token, 404 se MLB nao existe
```

**Prevencao**: 1 curl por endpoint antes de aplicar o plan. Se vc nao validou, nao confie no builder. Ver heuristica 1 em THINKING_WITH_AI (`./THINKING_WITH_AI.md#1-contrato-explicito-por-chamada-externa`, referência do material original não incluída como arquivo local) + nova pergunta CONTRACTS na rubrica de 8.

---

### 🚩 P-28 — Variavel sem fonte explicita gera implementacoes divergentes ⭐ (caso real 10/05)

**Sintoma**: plans diferem em **de onde** uma variavel vem. Ex: "stock = clamp(estoque_disponivel, ...)". Cloud assume que vem do candidate. Externo busca via GET separado.

**Causa**: prompt usa termo derivado (`estoque_disponivel`, `desconto_efetivo`) sem rastrear ate a fonte. Builder palpita.

**Caso real PROMPT_6 v2**: estoque LIGHTNING — Cloud nao explicitou de onde vem `available_quantity`. Externo explicitou (1 GET /items?attributes=available_quantity por MLB no inicio). Sem essa explicitacao, cada builder podia inferir lugar diferente (do candidate? do response_raw da promo? de uma tabela local?).

**Fix**: pra cada `X = ...` no fluxo, anote fonte:
```
stock_disponivel = response.available_quantity
  ← vem de GET /items/{mlb}?attributes=available_quantity
  ← chama 1x no inicio do varredor por MLB, reusa pros candidates LIGHTNING
```

**Prevencao**: leia o prompt de tras pra frente — pra cada variavel, pergunte "de onde vem?". Se nao consegue responder em 1 frase, falta rastreabilidade. Ver heuristica 3 em THINKING_WITH_AI (`./THINKING_WITH_AI.md#3-rastreabilidade-de-cada-variavel`, referência do material original não incluída como arquivo local).

---

### 🚩 P-29 — Trade-off escondido vira pergunta bloqueante ou decisao silenciosa ⭐ (caso real 10/05)

**Sintoma**: builder para no plan e pergunta detalhe tecnico ("usar webhook ou bot token?"), OU pior — decide silenciosamente sem avisar.

**Causa**: prompt pede comportamento **X** mas X tem mais de uma forma de implementar. Builder ou decide solo (problema futuro) ou pergunta (round perdido).

**Caso real PROMPT_6 v2**: prompt pediu `slack_message_ts` (pra editar mensagem pos-decisao). Webhook simples nao retorna ts; so chat.postMessage retorna. Cloud decidiu silenciosamente null. Externo perguntou bloqueante. **Mesmo bug, manifestacoes diferentes**.

**Fix**: trade-offs sao **decididos no prompt**, nao deixados implicitos:
```
slack_message_ts: tipo text, NULL no MVP.
  Razao: usar incoming webhook (nao retorna ts). Edit pos-decisao
  fica TODO no PROMPT seguinte. Migra pra bot token se virar dor.
```

**Prevencao**: antes de colar o prompt, pergunte a si mesmo "que decisoes tecnicas o builder vai precisar fazer aqui?". Cada uma vira nota explicita no prompt. Ver heuristica 4 em THINKING_WITH_AI (`./THINKING_WITH_AI.md#4-trade-offs-resolvidos-com-nota-explicita`, referência do material original não incluída como arquivo local).

---

### 🚩 P-30 — Smoke test vago = "feature funciona" sem criterio mensuravel ⭐ (padrao geral)

**Sintoma**: feature roda sem erro, mas comportamento real diverge do esperado. Voce so descobre dias depois quando alguem reclama.

**Causa**: criterio de aceite escrito como "deveria funcionar" / "botao Varrer funciona". Builder testa contra ideia geral, nao contra criterio mensuravel.

**Fix**: criterio de aceite **com numero/string/comportamento exato**:

| Ruim | Bom |
|---|---|
| "Botao Varrer funciona" | "Click Varrer em MLB com >=1 candidate FLEXIBLE elegivel pelo teto → POST registra HTTP 201 → toast aparece em <3s mostrando 'Aderiu N · M pendentes · K skip' → linha em promo_actions_log com `status_apos_post=started` e `deal_price=<calculado>`" |
| "Login funciona" | "Email valido + senha valida → redirect /dashboard em <1s. Email valido + senha errada → erro 'Credenciais invalidas' visivel < 500ms. Email invalido → validacao client-side antes de submit" |

**Prevencao**: cada criterio de aceite tem 3 partes — **input** + **acao** + **output mensuravel** (numero, texto exato, latencia, row em DB). Se falta alguma, smoke test e vago. Ver heuristica 5 em THINKING_WITH_AI (`./THINKING_WITH_AI.md#5-smoke-test-concreto-nao-deveria-funcionar`, referência do material original não incluída como arquivo local).

---

## Princípios de Prevenção

### 🛡️ A rubrica de 5 perguntas (revisão de Plan do builder)

Antes de aceitar **qualquer** Plan/SQL/diff que o builder propõe, passa pelos 5 critérios:

```
1. SECRETS — Algum valor pode chegar null/undefined no caminho real?
   (Origin/Referer em callback OAuth, env vars não-setadas)

2. ROTATION — Algum token/state que muda a cada uso e a gente está
   preservando o antigo? (refresh tokens, CSRF state, session ids)

3. EXPOSURE — Frontend acessa algum dado sensível que devia estar
   só no servidor? (access_token no response, service_role na UI,
   secrets em bundle client)

4. PROTECTION — Alguma EF/rota pública que devia exigir JWT?
   (verify_jwt errado, endpoint sem auth check)

5. SCHEMA — Algum SQL não-idempotente, RLS faltando em tabela
   nova, GRANT esquecido?
```

Se a resposta for **SIM** em qualquer uma, é **bloqueante** — pede correção.
Se for **NÃO** em todas — aprova e segue.

> Não confunde aluno com purismo arquitetural. Foco no que vira **bug em runtime real**.

---

### 🛡️ Caminho C — Reactive Learning aplicado preventivo

Quando o builder propõe algo que tu não pediu, **vire e pergunte pra IA antes de clicar Aceitar**.

**Template universal**:
> *"O builder está sugerindo isso: [cola Plan/SQL/diff]. Meu app está nessa fase: [X — MVP, beta, prod]. Aplicar agora faz sentido ou posso adiar?"*

Aluno aprende o reflexo certo: **se for só estética, deixa o builder fazer do jeito dele. Se for bug-prevention real, pede correção.**

---

### 🛡️ Onde pegar cada URL/Secret (referência rápida)

| Valor | Onde pegar |
|---|---|
| `APP_URL` | Lovable editor → preview URL (ícone "Open in new tab"). Após publish: URL estável `<project>.lovable.app` |
| `SUPABASE_URL` (project URL) | Supabase Dashboard → Settings → API → Project URL |
| `<EF>_URL` (callback OAuth, etc) | `<SUPABASE_URL>/functions/v1/<nome-da-EF>` |
| `CLIENT_ID`/`CLIENT_SECRET` ML | DevCenter ML → Suas Aplicações → app → Credenciais |
| `auth.users.id` (no callback OAuth) | Codificar no `state` antes de gerar (pra multi-tenant) |

---

### 🛡️ Onde clicar "Allow" e onde clicar "Cancel" (regrinha)

Builder mostrou "Modify database" com botão Allow/Cancel:

- **GRANT idempotente pra service_role** → Allow
- **CREATE TABLE com `IF NOT EXISTS`** → Allow
- **DROP POLICY ... CREATE POLICY** afetando tabela com dados → ⚠️ pergunta pra IA antes
- **CREATE FUNCTION SECURITY DEFINER** → ⚠️ pergunta pra IA antes
- **Mudança de RLS pra "scoped por user"** em MVP single-tenant → Cancel

Sempre clica **"View SQL"** antes de Allow.

---

## Como esse doc evolui

Cada novo pitfall vivido durante build de projeto vira entrada aqui:
1. Anota no calor da batalha (sintoma exato + URL/erro/log)
2. Descobre causa raiz (com IA ou sozinho)
3. Adiciona aqui com formato P-NN: sintoma → causa → fix → prevenção → template

Esse doc **não é teoria**, é diário de tropeços. Quanto mais entradas reais, mais útil pro aluno do evento Elo.

---

# Pitfalls — Sessão 14/05/2026

> 9 pitfalls catalogados em 1 sessão de operacionalização do App Promos ML (PROMPT_11 + PROMPT_12 + gating Slack + skip cupom + limit Supabase). Maior densidade de tropecos em produção ate hoje. Categorias: ML API, RLS/Auth, Cron/Infra, Supabase JS, UX.

Referência cruzada: o doc principal PITFALLS.md (`PITFALLS.md`, no material original) tem P-01 a P-41. Esses P-42 a P-50 vivem aqui pra manter sessões grandes auto-contidas (anti-pattern: arquivo monolítico de 1500+ linhas).

---

## P-45 — Tabela com RLS habilitada **SEM policy** e **SEM GRANT SELECT** pra authenticated

**Categoria**: RLS, Policies & Permissões

**Sintoma**: client autenticado faz `GET /rest/v1/auth_tokens?select=ml_user_id&limit=1` e recebe **403** silencioso. App traduz pra toast genérico "ML não conectado" (misleading).

**Causa raiz**: 2 problemas combinados:
1. RLS habilitado sem nenhuma policy criada (PostgreSQL bloqueia tudo por default)
2. Role `authenticated` **sem GRANT SELECT** (só TRUNCATE/REFERENCES/TRIGGER, que são inúteis)

Confirma via:
```sql
SELECT policyname FROM pg_policies WHERE tablename='auth_tokens';
-- vazio: sem policies

SELECT grantee, privilege_type FROM information_schema.role_table_grants WHERE table_name='auth_tokens';
-- authenticated tem só TRUNCATE, REFERENCES, TRIGGER (sem SELECT)
```

**Caso real Empresa 14/05**: GET retornava 403 em todo request authenticated. Front interpretava como ML disconnect. Confundimos diagnóstico por 2h — só achamos por curl com anon key + REST direto + leitura de `pg_policies` / `role_table_grants` lado a lado.

**Fix** (grant + policy, ambos necessários):
```sql
-- GRANT seletivo (NÃO expor access_token nem refresh_token)
GRANT SELECT (id, ml_user_id, user_id, expires_at, scope, created_at, updated_at)
  ON auth_tokens TO authenticated;

CREATE POLICY "user reads own auth_tokens row" ON auth_tokens
  FOR SELECT TO authenticated
  USING (user_id = auth.uid());
```

**Prevencao**: ao adicionar policy RLS, sempre confirma que role tem GRANT também. **Policy controla rows; GRANT controla colunas/operations**. Ambos precisam estar OK pra acesso funcionar. Heurística: depois de criar policy, rode `\dp <table>` no psql pra ver GRANT.

---

## P-47 — Pause/cancel UI: schedule vs job — semantica diferente, mesma palavra

**Categoria**: Editor Lovable & Preview (UX)

**Sintoma**: user clica "Pausar" achando que pausou um job em execução, mas pausou o **schedule** (impede execuções futuras). Job atual continua rolando.

**Causa**: agendamento tem 2 entidades:
- `sweep_schedules` (configuração de cron) com flag `active`
- `sweep_jobs` (execução) com `status` (`running`/`paused`/`done`/`cancelled`/`failed`)

UI tem botão "Pausar" em 2 telas:
- `/agendamento` (linha do schedule) afeta `active`
- `/sweeps` (linha do job) afeta `status`

User confundiu.

**Caso real Empresa 14/05**: responsável pelo exemplo queria cancelar job de varredura em curso pra revisar adesões. Clicou pause na tela `/agendamento` → schedule virou `active=false`. Mas job `49a5239e` continuou rodando. Perguntou "pausei, certo?" — diagnóstico via SQL mostrou `job.status='running'` ainda.

**Fix**:
- **UX**: labels distintos.
  - Schedule: "Desativar agendamento" (não vai mais disparar)
  - Job: "Pausar execução" (interrompe agora)
  - "Cancelar" (X) só pra job, irreversível
- **Implementação**: status `'paused'` no `sweep_jobs` (reversível). sweep-tick filtra `.eq('status', 'running')` → ignora paused. Pra retomar, status volta pra `'running'`.

**Validado em produção 14/05**: pause UI → SQL confirmou `status='paused'` + tick picked=0. Retomar UI → SQL confirmou `status='running'` + tick voltou a picked=5.

**Prevencao**: quando 2 entidades têm "estado" diferente mas o mesmo verbo de UI ("pausar"), separa nos labels. Diferenças sutis viram bugs operacionais.

---

## P-48 — PostgREST nested select falha com PGRST201 quando há 2+ FKs entre tabelas

**Categoria**: API & Semantica do Provider Externo (Supabase como provider)

**Sintoma**: `.select("a, b(c)")` retorna `PGRST201: Could not embed because more than one relationship was found for 'a' and 'b'`. Em código Supabase JS, o erro pode passar despercebido — `data` fica `null`, query "funciona" mas sem dados, código que depende delega tudo pra default falsy.

**Causa**: PostgREST não sabe qual FK usar pro embed quando há > 1 entre as tabelas. Hint sugere `b!fk_name(c)`, mas é frágil (depende do nome exato da FK no schema).

**Caso real Empresa 14/05**: sweep-tick v7 fazia
```ts
.select("id, schedule_id, sweep_schedules(notify_slack)")
```

Existem 2 FKs entre `sweep_jobs` e `sweep_schedules`:
- `sweep_jobs.schedule_id → sweep_schedules.id` (many-to-one)
- `sweep_schedules.last_job_id → sweep_jobs.id` (one-to-many)

PostgREST recusou. Bug **silencioso** em JS — `jobsMeta` ficou null, `notifyByJob` map vazio, **85 adesões reais aconteceram sem disparar Slack** antes de identificar.

**Fix robusto**: separa em 2 queries + Map manual:
```ts
const { data: jobs } = await sb.from('sweep_jobs')
  .select('id, schedule_id').in('id', jobIds);
const scheduleIds = jobs.map(j => j.schedule_id).filter(Boolean);
const { data: schedules } = await sb.from('sweep_schedules')
  .select('id, notify_slack').in('id', scheduleIds);
const map = new Map(schedules.map(s => [s.id, s.notify_slack === true]));
```

**Fix curto (frágil)**: `select("..., sweep_schedules!sweep_jobs_schedule_id_fkey(notify_slack)")` — quebra se FK for renomeada.

**Prevencao**: nested select é açúcar — quando há > 1 relação entre tabelas, **sempre prefira queries separadas + Map**. Anti-padrão usar embed em queries com side effects (notify, audit, etc.) porque erro silencioso vira bug em produção. Em PRs, code review deve grepar `\.select\([^)]*[a-z_]+\([^)]+\)` e checar se há > 1 FK.

---

## P-49 — Supabase JS `.select()` trunca em 1000 rows silenciosamente (server-side cap)

**Categoria**: Schema & Migrations / Pagination

**Sintoma**: query retorna no máximo 1000 rows mesmo quando há mais. Sem erro, sem warning. UI mostra dados "incompletos" sem indicação. **Pior**: `.range(0, 9999)` no client NÃO sobrescreve — o cap é do **servidor PostgREST** (`db-max-rows`), não do client.

**Causa**: PostgREST aplica `db-max-rows=1000` por default no Supabase managed. Mesmo pedindo `Range: 0-9999` no header, response volta `HTTP 206 Partial Content` com `Content-Range: 0-999/1167`. Client recebe 1000 rows e o total real fica escondido (a não ser que cheque o header `content-range`).

**Caso real Empresa 14/05**: `sweep-create-job` fazia
```ts
sb.from('promo_scenarios').select('id, mlb').eq('ativo', true)
```
sem range. Resultado: job criado com `total=1000` quando existiam **1167** ativos. 167 cenários ficaram silenciosamente fora da varredura. responsável pelo exemplo notou pelo número e perguntou "por que só 1000?".

**Fix CORRETO** (loop paginado — `.range()` sozinho NÃO basta):
```ts
async function paginatedSelect(sb, queryBuilder, PAGE = 1000, MAX = 10000) {
  const all = [];
  let from = 0;
  while (from < MAX) {
    const { data, error } = await queryBuilder().range(from, Math.min(from + PAGE - 1, MAX - 1));
    if (error) throw error;
    if (!data?.length) break;
    all.push(...data);
    if (data.length < PAGE) break;
    from += PAGE;
  }
  return all;
}

// uso: queryBuilder retorna nova query (PostgrestFilterBuilder é single-use)
const scenarios = await paginatedSelect(sb, () =>
  sb.from('promo_scenarios').select('id, mlb').eq('ativo', true).not('mlb', 'is', null)
);
```

**Fix INCORRETO** (acreditávamos que resolvia, NÃO resolve):
```ts
.range(0, 9999) // só pede header Range, server-side ainda corta em 1000
```

OU loop paginado convencional quando esperar > 10k:
```ts
const all = [];
let from = 0;
const PAGE = 1000;
while (true) {
  const { data } = await sb.from('promo_scenarios').select('*').range(from, from + PAGE - 1);
  if (!data?.length) break;
  all.push(...data);
  if (data.length < PAGE) break;
  from += PAGE;
}
```

**Prevencao**: TODO `.select()` em código de produção precisa cap explícito (`.range()` ou `.limit()`). Code review heurística:
```bash
grep -nE "from\(.*\)\.select\(" src/
# pra cada hit, confirma .range( ou .limit( na chain
```

**Observação**: feedback global do user (responsável pelo exemplo) já tinha esse pitfall anotado em memory ("Supabase: paginar com `.range()` (max 1000 rows)"). Mordeu de novo num app diferente — sinal que vale ter linter automático na esteira CI.

**Atualização 14/05 18:05** (corrigido in-flight): o fix inicial v6 de `sweep-create-job` usou só `.range(0, 9999)` achando que resolveria. **Não resolveu** — schedule disparou às 18h, criou job com `total=1000` igual antes. Bug confirmado via curl direto: `Content-Range: 0-999/1167` mesmo com `Range: 0-9999`. Fix real (v7) precisa **loop paginado de verdade**: enquanto response.length === PAGE, incrementa offset e re-consulta. Sem isso, `db-max-rows` server-side trunca silenciosamente toda chamada.

---

## Aprendizados-chave da sessão

1. **Diagnóstico cego via toast genérico custa caro**: 2h gastos no P-43/P-44/P-45 porque app traduzia 403 em "ML não conectado". Lição: instrumentação. Toast deve incluir codigo HTTP + endpoint quando erro real é silenciado.

2. **Erros silenciosos da Supabase JS são a maior fonte de bugs em produção** dessa sessão: P-48 (PGRST201 → data null), P-49 (limit 1000 → dados truncados). Defensivo: sempre `console.error(error)` + cap explícito.

3. **"Succeeded" em infra raramente significa "funcionou de verdade"** (P-46 com cron + reflexo 6 do doczao). Sempre olhar o output real (body, response), não só o status do pipeline.

4. **Auto-propagação do ML é poderosa mas não-documentada** (P-50). Cupom auto + race condition de propagação engana sistemas que assumem "candidate = preciso aderir". Lição: empirismo > inferência.

5. **Drift entre spec escrita e schema gerado pelo builder** (P-43 — spec dizia "TO public", builder gerou "TO authenticated"). Validação pós-builder via SQL é obrigatória pra policies. Não confiar.

## Cross-link com reflexos do framework Elo (doczao)

- Reflexo 6 (Bearer pass-through > env): consolidado por P-46
- Reflexo 7 (Triangulação 3 snapshots): aplicado em P-43/P-44/P-45 (esperado vs DB vs ML response)
- **Reflexo 9 NOVO**: "Idempotência defensiva por status, não por inferência" — confiar no `status` retornado pelo GET do provider em vez de inferir adesão por tabela local. Base de P-50 (cupom auto) + status check (P-XX já existente).
- **Reflexo 10 NOVO**: "Erro silencioso da Supabase JS é o adversário invisível". `data: null` ≠ "vazio" ≠ "erro". Sempre logar `error` antes de tratar `data`. Base de P-48 + P-49.

---

# Pitfalls — Sessão 15-18/05/2026

> 3 pitfalls catalogados na sessão de validação pós-deploy do App Promos ML (hotfix P-49/P-50 no Cloud + debug de job travado + pesquisa modo agressivo). Tema central: **a diferença entre "o código foi corrigido" e "a correção está rodando"** — staleness de deploy e locks órfãos são dois rostos do mesmo problema.

Referência cruzada: PITFALLS.md (`PITFALLS.md`, no material original) tem P-01 a P-41, PITFALLS_2026-05-14.md (`PITFALLS_2026-05-14.md`, no material original) tem P-42 a P-50. Esses P-51 a P-53 vivem aqui.

---

## P-51 — Worker queue sem stale lock recovery: job trava permanentemente

**Categoria**: Cron/Infra & Worker Queue

**Sintoma**: job de varredura `all_active` (1168 cenários) fica `running` pra sempre. UI mostra progresso congelado (ex: `868/1168`). O cron `sweep-tick` roda a cada 1min e retorna `{"ok":true,"jobs":1,"rows":0}` — vê o job mas processa zero linhas.

**Causa**: o `sweep-tick` locka um batch de linhas (`sweep_queue.status='running'` + `locked_at`), processa e marca `done`. Se o Worker serverless é reciclado/timeout **no meio** do batch, as linhas lockadas ficam `running` com `processed_at=NULL` — **órfãs**. O tick seguinte:
- Acha 0 linhas `pending` (todas done/failed/running).
- Conta as órfãs no check `stillBusy` (status in `pending,running`) → `stillBusy≠0` → **nunca marca o job `done`**.
- Sem `pending`, não há o que processar. Deadlock permanente.

**Caso real Empresa (job `3fe0816f`)**: 1168 cenários → `1103 done + 2 failed + 63 running(órfãs) + 0 pending`. As 63 tinham `locked_at` de 3 dias antes, `processed_at` null. Job preso 63h.

**Diagnóstico — como achar**: agregação por status na `sweep_queue` revela a assinatura na hora:
```sql
SELECT status, COUNT(*), MIN(locked_at), MAX(processed_at)
FROM sweep_queue WHERE job_id = '<id>' GROUP BY status;
```
Linhas `running` com `locked_at` velho e `processed_at` NULL = órfãs. Se `pending=0` e `running>0`, o job está deadlockado.

**Fix**: stale lock recovery. Função SQL chamada no início de cada tick, **antes** de buscar trabalho:
```sql
CREATE OR REPLACE FUNCTION recover_stale_locks() RETURNS void
LANGUAGE sql SECURITY DEFINER SET search_path = public AS $$
  UPDATE sweep_queue SET status='pending', locked_at=NULL, attempts=attempts+1
  WHERE status='running' AND locked_at < now()-interval '5 minutes' AND attempts < 5;
  UPDATE sweep_queue SET status='failed', error_message='stale_lock_max_retries'
  WHERE status='running' AND locked_at < now()-interval '5 minutes' AND attempts >= 5;
$$;
```
O cap `attempts < 5` evita loop infinito se uma linha "venenosa" sempre matar o worker. O incremento `attempts=attempts+1` **precisa** ser SQL — o Supabase JS builder não faz expressão de coluna (`col + 1`); por isso vira RPC, não `.update()`.

**Prevenção**: **toda fila de worker precisa de timeout de lock.** Sem stale recovery, qualquer worker que morre no meio do ciclo deixa lixo permanente. É invariante de design, não opcional. Destravar manualmente (`UPDATE ... running→pending`) resolve o job atual mas é gato-e-rato — sem o recovery automático, trava de novo no próximo recycle.

**Desfecho (validado 18/05)**: fix `recover_stale_locks()` publicado às ~13:34. O job `3fe0816f` (travado 63h) fechou sozinho às 13:42 — `status=done`, queue real `1166 done + 2 failed = 1168`. Recovery re-enfileirou as órfãs em ondas (28 → depois 5 residuais), e ticks saudáveis as drenaram. As 2 `failed` finais são legítimas (`Item status is not allowed (under_review)` no ML). Confirmado: o sintoma "5 linhas que nunca processam, `log_entries=0`" **não** era cenário venenoso — GETs ML dessas eram 200/normais; era só o ciclo de recovery levando alguns minutos. Lição: `log_entries=0` num momento prova só que ainda não processou, não que é impossível processar.

---

## P-53 — Batch size maior que o wall-time do worker serverless

**Categoria**: Cron/Infra & Worker Queue

**Sintoma**: jobs grandes deixam um resíduo de linhas órfãs (`running` sem `processed_at`) a cada execução. Pequenos terminam limpos; grandes quase sempre sobram alguns.

**Causa**: o `sweep-tick` processa `BATCH=50` cenários **síncronos numa única request HTTP**, com `THROTTLE_MS=500` entre cada. 50 × (~2-4s por cenário + 0,5s throttle) ≈ **2,5-4min por tick**. Workers serverless (Cloudflare, Vercel, Supabase EF) têm wall-time limitado por invocação. Quando o batch excede esse limite, o worker é morto no meio → linhas lockadas viram órfãs (ver P-51).

**Caso real Empresa**: dos 24 ticks (~50 cada) necessários pra 1168 cenários, a maioria completava, mas 1-2 morriam por wall-time, deixando 28-63 órfãs por job. P-51 (stale recovery) cura o sintoma; P-53 é a causa raiz.

**Fix**: dimensionar o batch pra caber **com folga** numa invocação. Se o limite é ~30s e cada cenário leva ~3s, `BATCH` máximo seguro é ~8-10, não 50. Alternativa: lock-and-process incremental (lockar 1, processar 1, repetir) — elimina o conceito de batch.

**Prevenção**: **batch de worker deve ser função do wall-time da plataforma, não um número redondo arbitrário.** `BATCH=50` é cômodo de ler mas não tem relação com a realidade do runtime. Calcular: `BATCH_max ≈ (wall_time_limit × margem_segurança) / tempo_por_item`. Com stale recovery (P-51) o sistema "funciona" mesmo com batch errado — mas vira ineficiente (locka 50, processa 30, recicla, re-enfileira 20, repete). Os dois fixes são complementares: P-51 garante correção, P-53 garante eficiência.

**Desfecho (validado 18/05)**: `BATCH` baixado pra 20 (commit `0ab131e8`). Job de teste de 30 cenários lockou em lotes de **exatamente 20 + 10** — confirmado pelos `locked_at` distintos na `sweep_queue`. Job fechou em 2 ticks, zero linhas órfãs.

---

## P-54 — `sweep_jobs.totals` (jsonb agregado) diverge da `sweep_queue` real

**Categoria**: Worker Queue & Estado Derivado

**Sintoma**: job com `status='done'` mas a UI mostra progresso parcial — ex: job `3fe0816f` fechou 100% (`1166 done + 2 failed` na queue) mas `sweep_jobs.totals` mostra `{done:885, failed:1}`. O usuário vê "886/1168" num job concluído.

**Causa**: `totals` é um contador jsonb mantido **incrementalmente** — o tick soma `done`/`failed` em memória e grava o jsonb ao fim de cada batch. Dois furos: (1) quando o worker morre no meio do batch, o update do `totals` é perdido (P-51); (2) a finalização do job (marca `done`) **não recalcula** `totals` — usa o último valor agregado, que pode estar defasado dezenas/centenas de linhas.

**Caso real Empresa**: `3fe0816f` fechou com `totals.done=885` enquanto a `sweep_queue` tinha 1166 `done`. Divergência de 281 linhas. O job está correto; o contador exibido, não.

**Fix**: parar de materializar `totals` incrementalmente. A `sweep_queue` é a fonte da verdade — `totals` deve ser **derivado por COUNT** a cada leitura/finalização:
```sql
SELECT status, COUNT(*) FROM sweep_queue WHERE job_id = $1 GROUP BY status;
```
No mínimo: recalcular `totals` da queue no momento de marcar o job `done`. Ideal: recalcular a cada tick (COUNT é barato, indexado por `job_id`).

**Prevenção**: **estado derivável não deve ser materializado de forma incremental quando a fonte canônica existe.** Um contador agregado mantido à mão diverge da realidade em qualquer falha parcial — e falha parcial é certeza em worker serverless. `COUNT(*)` numa tabela indexada é barato; a "otimização" de manter o agregado em jsonb custou um bug de UX silencioso. Materializar só se a fonte for cara de varrer — não é o caso aqui.

**Desfecho (validado 18/05)**: helper `recalcTotalsFromQueue()` deriva `done`/`failed` por `COUNT` real na `sweep_queue` (commit `0ab131e8`). Job de teste fechou com `sweep_jobs.totals = {done:29, failed:1, total:30}` — idêntico à contagem real da queue. O `totals` agora sobrevive a reciclagem de Worker no meio do batch.

---

## Reflexos novos pro doczao Elo

- **R15 — Diagnóstico de staleness é específico da infra**: "o código está certo, por que não funciona?" tem caminhos de verificação diferentes em cada plataforma. Edge Function: cheque `version`. Worker via Lovable Publish: cheque timestamp de publish. Saber *onde* o runtime mora é pré-requisito pra diagnosticar.
- **R16 — Agent orquestra agent**: Claude Code pilotou o Lovable agent por linguagem natural (MCP `send_message`), leu o código-fonte (`read_file`), validou no banco (`query_database`) e revisou o diff (`get_diff`) — loop fechado sem transporte humano de prompts. O humano vira aprovador de iteração e dono do publish, não o copista entre as duas IAs.
- **R17 — A assinatura do bug aponta a versão**: quando um valor que só existe em código deletado aparece em dado novo, o runtime está stale. Procurar "strings impossíveis" é uma técnica de diagnóstico — mais rápida que comparar timestamps.

# Pitfalls — Sessão 18/05/2026 (tarde): execução do Modo Agressivo

> 2 pitfalls catalogados na sessão de execução do Plano 1 (Modo Agressivo, App Externo). Diferente das sessões anteriores — foi uma execução limpa de plano, 15/15 tasks, validada end-to-end (upgrade real 10%→40% no MLB4445429611). Os tropeços não foram bugs de implementação; foram sobre **propagação de schema até a camada que a UI lê** e sobre **o alcance real de um modo "mais agressivo"** diante de um provedor externo.

Referência cruzada: PITFALLS.md (`PITFALLS.md`, no material original) tem P-01 a P-41, PITFALLS_2026-05-14.md (`PITFALLS_2026-05-14.md`, no material original) P-42 a P-50, PITFALLS_2026-05-18.md (`PITFALLS_2026-05-18.md`, no material original) P-51 a P-54. Esses P-55 e P-56 vivem aqui.

---

## P-55 — Coluna nova não chega na view que a UI lê

**Categoria**: Schema & Camada de Apresentação

**Sintoma**: migration aplicada, coluna nova existe na tabela base, o backend grava nela — mas a UI nunca enxerga o valor. No caso: `aggressive` foi adicionada a `sweep_jobs`/`sweep_schedules`, as Edge Functions gravavam certo, mas o badge "Agressivo" nunca apareceria e o formulário de agendamento sempre mostraria o toggle desligado.

**Causa**: o frontend não lê das tabelas base — lê de **views** (`sweep_jobs_view`, `sweep_schedules_view`) que agregam/derivam campos pra UI. Uma view definida com `SELECT` de colunas explícitas (não `SELECT *`) **não herda** colunas novas da tabela. A migration que adiciona a coluna na tabela base deixa a view intacta — e a UI consome a view.

**Caso real Empresa**: o plano do Modo Agressivo só previa `ALTER TABLE ... ADD COLUMN aggressive` nas duas tabelas. As 4 telas novas (badge em /sweeps e /agendamento, toggle no form de schedule) leem das views. Sem `aggressive` na view, o campo chegava `undefined` no componente → badge nunca renderiza, `useState(initial?.aggressive ?? false)` sempre cai no `false`. O builder Lovable pegou isso sozinho e gerou uma 2ª migration `CREATE OR REPLACE VIEW` pras duas views.

**Fix**: junto com a migration que adiciona a coluna, recriar (`CREATE OR REPLACE VIEW`) toda view que a UI consome, incluindo a coluna nova. `CREATE OR REPLACE` exige que as colunas antigas permaneçam na mesma ordem — só dá pra **acrescentar** no fim. Recriar a definição a partir do `pg_get_viewdef` real (não da reconstruída de memória) evita quebrar consumidores.

**Prevenção**: **uma coluna nova precisa ser rastreada até a camada que a consome — tabela base ≠ contrato da UI.** Ao planejar um `ADD COLUMN`, pergunte: "a UI lê essa tabela direto ou via view?" Se via view, a migration tem 2 partes. Vale também pros tipos gerados (`types.ts` do Supabase) — regenerar depois da view, senão o TypeScript não conhece o campo. Checklist: tabela → view → tipos gerados → componente.

**Desfecho (validado 18/05)**: `pg_get_viewdef` confirmou `aggressive` em `sweep_jobs_view` e `sweep_schedules_view` no Supabase do Externo — a migration de view do builder foi aplicada. A verificação visual do badge fica pendente do Publish do frontend.

---

## Reflexos novos pro doczao Elo

- **R18 — Transporte cai ≠ ação falhou (orquestração agent-a-agent)**: refina o R16. Quando a chamada de um agent pro outro cai no meio (transporte MCP dropado, socket), a ação pode ter completado mesmo assim — o agent-alvo segue trabalhando do lado dele, independente do canal de resposta. Antes de retransmitir, **verifique o estado do agent-alvo** (histórico de edições, diff, versão), não retransmita cego — arrisca duplicar o trabalho. Caso real: o `send_message` pro builder Lovable perdeu a resposta no meio; o `list_edits` mostrou que a edição "Adicionou modo agressivo UI" já tinha sido commitada — o trabalho estava feito, só a resposta se perdeu. O 2º `send_message` (de confirmação) achou tudo no lugar e não duplicou nada.
- **R19 — Evoluir sem medo: o caminho conservador continua sendo o default (Fase 03)**: a feature inteira do Modo Agressivo foi pra produção sem feature-flag e sem branch — porque cada caminho de código novo é gated numa coluna booleana `aggressive` com `DEFAULT false`. Todo job e agendamento que já existia continua `false` → comportamento byte-idêntico ao anterior, garantido por testes de regressão verdes. Princípio de Fase 03: uma evolução é segura de soltar quando o estado herdado cai no comportamento antigo *por construção*, não por sorte. A pergunta "como solto isso sem quebrar o que funciona?" tem uma resposta de design — faça o novo ser opt-in no nível do dado (a coluna default-false), não no nível da torcida.

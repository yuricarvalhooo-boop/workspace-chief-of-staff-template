---
{
  "id": "HOMER-geral-08",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "cd6d31e82d33c4c94a86968448a8d6af4df6919142628c7e7ced51e697ff1a24",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 08-infra-avancada — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# 08 — Infraestrutura Avancada

> Tópicos para quando o app cresce além de um MVP simples.  
> **Nao leia tudo de uma vez.** Navegue por topico quando bater a necessidade real:
>
> - [Cron / background jobs](#1-setup-de-cron-job-background-jobs) — processa fila, avisa usuario as 9h, sincroniza com API parceira, limpa rows antigas
> - [Bearer pass-through](#2-bearer-pass-through-em-chained-edge-functions) — encadeia Edge Functions sem travar em 401
> - [Slack Webhook](#3-slack-webhook-como-criar-e-onde-guardar) — notifica humano sem depender de clique no app
> - [Lovable via MCP](#4-prompt-via-mcp-lovable-controlado-por-agente) — agente AI controla o Lovable (research preview)

---

---

## 1. Setup de Cron Job (background jobs)

> Playbook end-to-end pra subir um worker periodico que processa fila no Supabase. Cobre os 2 caminhos didaticos (Cloud sem auth + advisory lock, Externo com service_role Bearer pass-through) com pitfalls reais documentados.

---

### Quando voce precisa de cron

App tem:
- **Fila de tarefas** que processa em background (varredor, sync, batch operations)
- **Acoes recorrentes** (notificar usuarios as 9h, agregar metricas a cada hora)
- **Cleanup** (apagar rows antigas, expirar tokens)
- **Polling externo** (checar API parceira a cada N min)

Sem cron, voce depende de clique humano. Com cron, app vira autonomo.

---

### Arquitetura comum (motor batch + tick)

```
+----------+      a cada 1min        +-----------+
|  pg_cron |  ---------------------> | sweep-tick|
+----------+                          +-----------+
                                            |
                                            | processa N rows
                                            v
                                      +-----------+
                                      | sweep_queue|
                                      +-----------+
                                            |
                                            | chama (pass-through)
                                            v
                                      +-----------+
                                      |  worker-EF |
                                      +-----------+
```

Componentes:
1. **`pg_cron`**: dispara `sweep-tick` a cada minuto
2. **`sweep-tick`** (EF): pega ate N rows pending da `sweep_queue`, chama worker pra cada
3. **`worker-EF`** (ex: `promo-activate`): executa a logica da tarefa
4. **Tabelas de estado**: `sweep_jobs` (header) + `sweep_queue` (rows) + `sweep_tick_log` (auditoria)

---

### Pre-requisitos

#### Extensions Postgres

```sql
CREATE EXTENSION IF NOT EXISTS pg_cron WITH SCHEMA extensions;
CREATE EXTENSION IF NOT EXISTS pg_net WITH SCHEMA extensions;
GRANT USAGE ON SCHEMA cron TO postgres;
```

⚠️ **Pitfall P-41**: nao funciona pelo SQL editor (precisa superuser). Roda via **migration** (builder/CLI tem privilegio).

Valida apos:
```sql
SELECT extname FROM pg_extension WHERE extname IN ('pg_cron','pg_net');
-- esperado: 2 rows
```

---

### Caminho A — Cloud (sem auth no tick + advisory lock)

**Quando usar**: stack TanStack Start (Lovable Cloud). Rotas em `/api/public/*` sao publicas por design — auth e via outras camadas.

#### 1. Endpoint da EF

```ts
// src/routes/api/public/sweep-tick.ts
import { createFileRoute } from "@tanstack/react-router";
import { supabaseAdmin } from "@/integrations/supabase/client.server";

export const Route = createFileRoute("/api/public/sweep-tick")({
  server: {
    handlers: {
      POST: async () => {
        // Sem auth. Defesas em profundidade abaixo.

        // 1. Advisory lock previne overlap
        const { data: lockOk } = await supabaseAdmin.rpc("try_sweep_tick_lock");
        if (!lockOk) {
          return new Response(JSON.stringify({ skipped: true, reason: "already_running" }), {
            headers: { "Content-Type": "application/json" }
          });
        }

        // 2. Tick log start
        const { data: tickRow } = await supabaseAdmin
          .from("sweep_tick_log")
          .insert({ status: "running" })
          .select("id").single();

        try {
          // ... processa queue, chama worker ...
          await supabaseAdmin.from("sweep_tick_log")
            .update({ status: "done", finished_at: new Date(), jobs_processed: N, rows_processed: M })
            .eq("id", tickRow.id);
        } catch (e) {
          await supabaseAdmin.from("sweep_tick_log")
            .update({ status: "error", error_message: String(e), finished_at: new Date() })
            .eq("id", tickRow.id);
        }

        return new Response(JSON.stringify({ ok: true }), { headers: { "Content-Type": "application/json" }});
      }
    }
  }
});
```

#### 2. RPC pro advisory lock

```sql
CREATE OR REPLACE FUNCTION try_sweep_tick_lock()
RETURNS boolean LANGUAGE sql SECURITY DEFINER AS $$
  SELECT pg_try_advisory_lock(hashtext('sweep-tick'));
$$;
GRANT EXECUTE ON FUNCTION try_sweep_tick_lock TO service_role;
```

#### 3. Schedule do cron

Apos Publish do app (P-39!):

```sql
SELECT cron.schedule('sweep-tick-1min', '* * * * *', $$
  SELECT net.http_post(
    url := 'https://project--<seu-uuid>.lovable.app/api/public/sweep-tick',
    headers := '{"Content-Type":"application/json"}'::jsonb,
    body := '{}'::jsonb
  );
$$);
```

⚠️ **Pitfall P-39**: a URL `project--<uuid>.lovable.app` so responde apos primeiro Publish. Se schedular antes, `net._http_response` mostra 404 sistematico.

#### 4. Validacao

```sql
-- cron schedulado?
SELECT jobname, schedule, active FROM cron.job WHERE jobname='sweep-tick-1min';

-- responses dos primeiros ticks?
SELECT id, status_code, LEFT(content, 200) AS body, created
FROM net._http_response
ORDER BY created DESC LIMIT 5;
-- esperado: status_code=200, body com ok:true ou skipped:true

-- tick_log popula?
SELECT status, jobs_processed, rows_processed, ran_at
FROM sweep_tick_log ORDER BY ran_at DESC LIMIT 5;
```

#### Por que sem auth funciona

- Endpoint **idempotente**: sem job em `running`, retorna `{ok:true, picked:0}` e sai. Atacante nao causa amplificacao
- **Advisory lock** previne overlap (atacante nao consegue forcar processamento concorrente)
- **Caps fixos** (MAX_JOBS=5, BATCH=50, THROTTLE_MS=500) limitam custo mesmo sob flood
- **sweep_tick_log** registra cada invocacao pra auditoria

**Custo de abuso**: ~$0.0000005 por invocacao Supabase. Mil ataques = $0.0005. Negligivel.

---

### Caminho B — Externo (service_role Bearer + pass-through)

**Quando usar**: stack Supabase puro (Edge Functions com `verify_jwt=true`). Default Supabase e privado — aproveita.

#### 1. EF tick

```ts
// supabase/functions/sweep-tick/index.ts
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const sb = createClient(SUPABASE_URL, SERVICE_ROLE);

Deno.serve(async (req) => {
  // 1. Authorization deve estar presente (verify_jwt=true bloqueia se nao)
  const incomingAuth = req.headers.get("Authorization")!;

  // 2. Advisory lock
  const { data: lockOk } = await sb.rpc("try_sweep_tick_lock");
  if (!lockOk) return new Response(JSON.stringify({ skipped: true }), { headers: { "Content-Type": "application/json" }});

  // ... processa queue ...

  // 3. Chamada chained — PASS-THROUGH do Bearer entrante
  for (const row of pendingRows) {
    const resp = await fetch(`${SUPABASE_URL}/functions/v1/promo-activate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: incomingAuth,  // <-- nao usa SERVICE_ROLE do env
      },
      body: JSON.stringify({ scenario_id: row.scenario_id }),
    });
    // ...
  }

  return new Response(JSON.stringify({ ok: true }), { headers: { "Content-Type": "application/json" }});
});
```

⚠️ **Pitfall P-38**: nao chama `promo-activate` com `Bearer ${SERVICE_ROLE}` (env var). Use o Authorization entrante. Detalhes na seção [Bearer Pass-Through](#2-bearer-pass-through-em-chained-edge-functions).

#### 2. Schedule do cron

Pega service_role no Dashboard → Settings → API → service_role (sem whitespace, P-01!):

```sql
SELECT cron.schedule('sweep-tick-1min', '* * * * *', $$
  SELECT net.http_post(
    url := 'https://<seu-projeto>.supabase.co/functions/v1/sweep-tick',
    headers := jsonb_build_object(
      'Content-Type','application/json',
      'Authorization','Bearer eyJhbGc...<COLA_KEY_REAL_AQUI>...XYZ'
    ),
    body := '{}'::jsonb
  );
$$);
```

⚠️ **Pitfall P-36**: NAO cola com `<SERVICE_ROLE_KEY>` literal. Substitui pelo valor real ANTES de rodar.

⚠️ **Pitfall P-37**: tentar `ALTER DATABASE postgres SET app.service_role_key='...'` falha com 42501 em Supabase managed. Aceita inline mesmo (so superuser ve `cron.job`).

#### 3. Auto-validacao apos schedule

```sql
-- formato Bearer e JWT valido?
WITH bearer AS (
  SELECT (regexp_match(command, 'Bearer ([^''\s]+)'))[1] AS k
  FROM cron.job WHERE jobname='sweep-tick-1min'
)
SELECT length(k) AS len,
       array_length(string_to_array(k, '.'), 1) AS jwt_parts,
       substring(k, 1, 12) AS first_chars
FROM bearer;
-- esperado: len > 100, jwt_parts = 3, first_chars com 'eyJ'

-- responses sao 200?
SELECT id, status_code, LEFT(content, 100) AS body
FROM net._http_response ORDER BY created DESC LIMIT 3;
```

---

### Comparativo Cloud vs Externo

| Aspecto | Cloud (sem auth) | Externo (Bearer pass-through) |
|---|---|---|
| Setup | 1 SQL (apos Publish) | 1 SQL (+ pegar service_role do Dashboard) |
| Quantos secrets | 0 | 0 novos (reusa SUPABASE_SERVICE_ROLE_KEY) |
| `ALTER DATABASE` necessario | nao | nao (recomendado evitar) |
| Risco superficie | tick publico (mitigado por lock+caps) | tick privado (verify_jwt=true) |
| Caminho idiomatico stack | sim (`/api/public/*` e design TanStack) | sim (EF Supabase default privada) |
| Bug "esquecer publish" | sim (P-39) | nao |
| Bug "key dessincronizada" | nao | sim sem pass-through (P-38) |

**Pro evento didatico**: mostra os 2. Aluno escolhe o que combina com a stack dele.

---

### Pitfalls relacionados

- P-36 — Placeholder em SQL
- P-37 — ALTER DATABASE bloqueado
- P-38 — Drift env vs Dashboard
- P-39 — Lovable preview 404
- P-40 — Drift UI×Schema
- P-41 — Extensions faltando

---

### Smoke universal (cobre os 2 caminhos)

```
1. Schedule cron — confirma SELECT cron.job retorna 1 row
2. Aguarda 2-3min — confirma net._http_response retorna status_code=200
3. Cria job de teste (ex: 2 cenarios) via UI
4. Aguarda 1-2min — confirma sweep_jobs.status='done' + sweep_queue rows='done'
5. Drill-down — confirma result jsonb populado com dados coerentes
6. Stress test: cria job grande (50+ rows) e observa que advisory lock previne overlap nos ticks proximos
```

---

### Conexao com framework Elo

- **Fase 02 (Construir)**: ensina padrao motor batch desde o primeiro app que precisa de background
- **Fase 03 (Evoluir)**: cron + agendamento + filtros salvos sao a base de **autonomia** do usuario (pessoa operacional do exemplo nao precisa logar pra processar; vai sozinho)

---

### Checklist antes de declarar cron "em producao"

```
☐ Extensions habilitadas via migration (CREATE EXTENSION pg_cron + pg_net)
☐ App publicado (se Lovable Cloud com URL publish-stable)
☐ Cron schedulado e ativo (SELECT cron.job)
☐ Primeiros ticks retornam status_code=200 em net._http_response
☐ JWT format validado (length + jwt_parts, se Externo)
☐ sweep_tick_log popula a cada minuto
☐ Smoke real com 2 jobs completou
☐ Advisory lock testado (cria 2 ticks rapidos seguidos)
☐ Sem warnings no Supabase Advisors
```

---

---

## 2. Bearer Pass-Through em Chained Edge Functions

> Padrao arquitetural pra propagar autenticacao entre Edge Functions encadeadas, evitando drift entre env vars e tokens reais. Documentado apos pitfall P-38 (sessao 13/05/2026).

---

### O problema

Quando uma Edge Function chama outra (EF A → EF B), o reflexo natural e:

```ts
// EF A: chama EF B
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
await fetch("https://.../functions/v1/b", {
  headers: { Authorization: `Bearer ${SERVICE_ROLE}` }
});
```

Parece certo: env var injetada pelo Supabase, service_role bypassa RLS, deve funcionar.

**Mas**: o que esta em `Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")` no runtime da EF pode estar **diferente** da key visivel no Supabase Dashboard. Razoes que ja vimos:

- Rotacao silenciosa do JWT secret do projeto
- Migracao do sistema de keys (JWT legacy → new format)
- EF deployada com snapshot antigo da key
- Diferenca entre key injetada pelo Lovable Cloud vs key do Supabase underlying

**Sintoma**: chamadas internas falham com `401 UNAUTHORIZED_INVALID_JWT_FORMAT`. Mas chamadas externas (curl, pg_net manual) com a key "do Dashboard" funcionam. Voce passa horas debugando "por que da 401 se a key e a mesma".

---

### A solucao: pass-through

Em vez de **re**-autenticar com env var, **repassa** o Authorization que JA entrou no request:

```ts
// EF A: chama EF B repassando o Bearer entrante
const incomingAuth = req.headers.get("Authorization")!;
await fetch("https://.../functions/v1/b", {
  headers: { Authorization: incomingAuth }
});
```

Princípio: **se quem te chamou estava autenticado, propaga**. Voce nao precisa autenticar novamente — a credencial ja chegou correta.

---

### Quando aplicar

| Cenario | Pass-through? |
|---|---|
| EF A recebe request com Bearer e chama EF B | ✅ Sim — propaga |
| EF chamada por pg_cron com Bearer service_role | ✅ Sim — propaga pra chained EFs |
| EF webhook publico (sem auth de entrada) chamando EF interna | ❌ Nao — gera novo Bearer (env var ou service_role explicito) |
| EF cria cliente Supabase pra escrever no DB | ❌ Nao — usa SERVICE_ROLE no `createClient` |
| EF chama API externa (ML, Slack, etc) | ❌ Nao — usa token especifico daquela API |

A regra: **pass-through entre EFs do mesmo projeto Supabase**. Pra qualquer outra coisa, gera credencial apropriada.

---

### Padrao completo

```ts
// supabase/functions/sweep-tick/index.ts

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// 1. CLIENT INTERNO — usa env var pra conexao Postgres
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const sb = createClient(SUPABASE_URL, SERVICE_ROLE);

Deno.serve(async (req) => {
  // 2. EXTRAI Authorization entrante
  const incomingAuth = req.headers.get("Authorization");
  if (!incomingAuth) {
    return new Response("Unauthorized", { status: 401 });
  }

  // ... logica de processamento ...

  // 3. CHAMADAS INTERNAS — repassa Bearer
  const resp = await fetch(`${SUPABASE_URL}/functions/v1/promo-activate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: incomingAuth,  // <- pass-through
    },
    body: JSON.stringify({ scenario_id: row.scenario_id }),
  });

  // 4. CHAMADAS EXTERNAS — usa token especifico (nao pass-through)
  const mlResp = await fetch(`https://api.mercadolibre.com/...`, {
    headers: {
      Authorization: `Bearer ${mlAccessToken}`,  // <- token ML, nao Supabase
    }
  });

  return new Response(JSON.stringify({ ok: true }));
});
```

---

### Por que isso e didaticamente importante

No framework Elo (Fase 02/03), aluno vai construir features com chained EFs assim que precisar de background jobs, queues, ou orquestracao multi-step. Sem esse padrao, ele vai:

1. Ler env var
2. Bater 401 random
3. Passar horas debugando
4. Talvez resolver, talvez nao
5. Confiar menos no Supabase

Com o padrao:

1. Pass-through default
2. Zero drift
3. Bug **nao acontece**

Reflexo arquitetural: **propaga o que voce recebeu, gera so o que voce precisa do zero**.

---

### Pitfall relacionado

P-38 — caso real do drift que motivou esse doc.

---

### Conexao com framework Elo

- **Fase 02 (Construir)**: ensina padrao desde o primeiro prompt de feature com chained EF
- **Fase 03 (Evoluir)**: quando aluno tem batch jobs / agendamento / multi-step pipelines, pass-through evita ~80% dos bugs de auth

---

### Checklist antes de aplicar plan com chained EF

```
☐ EF chamadora recebe Bearer no Authorization (cron ou caller externo)?
  → SIM: usa pass-through
  → NAO: gera Bearer com env var (sem chained chain — e flag amarela)

☐ EF chamada esta no mesmo projeto Supabase?
  → SIM: pass-through funciona
  → NAO: precisa token apropriado pra essa API

☐ EF chamadora escreve no Postgres?
  → Mantem createClient(URL, SERVICE_ROLE) — pass-through e so pra HTTP outbound

☐ Adicionou validacao "if no incomingAuth → 401"?
  → Senao pass-through manda Bearer null e fica confuso
```

---

---

## 3. Slack Webhook — Como criar e onde guardar

> Modulo do evento (~10 min). Sentado entre `PRE_FLIGHT.md` e qualquer prompt que envie notificacao pra Slack (PROMPT_6 promo-activate, PROMPT_9, PROMPT_10).
> **Filosofia**: a maioria dos apps reais avisa humano em algum momento — Slack e o canal mais barato e mais rapido pra fazer isso. Voce nao precisa entender API REST nem OAuth. Precisa pegar 1 URL e guardar bem.

---

### Quando voce vai precisar

Sempre que o app precisar **avisar um humano** sem esperar ele abrir o app:
- Promo precisa aprovacao (caso real PROMPT_6)
- Erro critico em producao
- Pedido novo / lead novo
- Cron rodou e algo merece olho
- Build/deploy falhou

Slack incoming webhook = URL secreta que aceita POST com texto/Block Kit e publica no canal escolhido. **Sem API key, sem OAuth, sem nada complexo.**

---

### Decisao 1 — Webhook simples ou bot token?

| Opcao | Pro | Contra | Quando usar |
|---|---|---|---|
| **Incoming Webhook** (este doc) | 5 min pra criar, 1 URL, 1 canal fixo | 1 webhook = 1 canal. Nao da pra editar mensagem depois | MVP, alertas simples |
| **Slack App + Bot Token** (`chat.postMessage`) | Posta em qualquer canal, **edita** mensagem depois (ex: marcar "aprovado por X"), botoes interativos | Mais setup (bot user, scopes, install no workspace) | Workflows com aprovacao na propria mensagem |

**Pro App Promos ML MVP**: webhook simples. Edit pos-decisao fica TODO num PROMPT seguinte se virar dor. **Esse arquivo cobre webhook simples**. Bot token vira `SLACK_BOT_TOKEN_SETUP.md` quando precisarmos.

---

### Pre-requisitos

1. Conta Slack no workspace onde vai postar
2. Permissao pra **adicionar apps** no workspace
   - Se nao for admin, pede pro admin (~30s pra ele aprovar)
   - Como saber se voce e admin: `Workspace → Settings & administration → Workspace settings`. Se aparecer voce nao e admin nao mostra essa opcao
3. Canal criado e voce dentro dele (ex: `#promos-ml`)

---

### Passo-a-passo (~5 min)

#### 1. Cria o app Slack

- Abre **`api.slack.com/apps`** (logado na conta Slack)
- `Create New App` → `From scratch`
- **App Name**: ex `App Promos ML alerts`
- **Pick a workspace**: escolhe o workspace correto
- `Create App`

#### 2. Ativa Incoming Webhooks

- Na barra lateral do app criado, click `Incoming Webhooks`
- Toggle **Activate Incoming Webhooks** → liga (verde)
- Role pra baixo, click **Add New Webhook to Workspace**
- Escolhe o canal (ex: `#promos-ml`) — vai receber as mensagens
- `Allow`
- Slack volta pra pagina anterior — agora tem 1 webhook listado com URL

#### 3. Copia a URL

- Click `Copy` ao lado da URL — formato:
  ```
  https://hooks.slack.com/services/<SEU_TEAM>/<SEU_CHANNEL>/<SEU_TOKEN>
  ```
- **NAO compartilha essa URL em chat publico, repo publico, ou commit em codigo**. Quem tem ela posta no canal sem auth.

#### 4. Guarda em 3 lugares

Sempre nesta ordem (do mais persistente pro mais ephemero):

1. **Bitwarden / 1Password** — registro novo:
   - Nome: `Slack Webhook - <nome do canal>`
   - Username: nome do app Slack que voce criou
   - Notes: data + workspace + canal
   - Field custom: a URL completa
2. **Lovable Cloud Secret** OU **Supabase Edge Function Secret**:
   - Nome do secret: `SLACK_WEBHOOK_PROMOS_ML` (mantem padrao MAIUSCULO_COM_UNDERSCORE)
   - Valor: cola a URL **sem espaco no inicio nem no fim** (ver pitfall abaixo)
3. **`.env.example`** do projeto (se houver):
   - Adiciona linha `SLACK_WEBHOOK_PROMOS_ML=https://hooks.slack.com/services/...` pro proximo dev saber que existe — **MAS coloca o valor real apenas em `.env.local`** que nunca vai pro git

#### 5. Testa

Abre terminal e roda (substitui pela URL real):

```bash
curl -X POST https://hooks.slack.com/services/<SEU_TEAM>/<SEU_CHANNEL>/<SEU_TOKEN> \
  -H 'Content-Type: application/json' \
  -d '{"text":"teste do webhook do app promos ml"}'
```

Resposta esperada: `ok`

Abre o canal Slack — mensagem "teste do webhook do app promos ml" apareceu? **Webhook funciona**.

---

### Block Kit (mensagens ricas)

Webhook aceita Block Kit no body — em vez de so `{text: "..."}`, manda layout estruturado com header, sections, fields, botoes (link only, sem callback no webhook simples).

Exemplo do PROMPT_6 (aprovacao de promo):

```json
{
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "⚠️ Promo precisa aprovacao" }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*MLB:* MLB4184318945\n*Tipo:* MARKETPLACE_CAMPAIGN\n*Razao:* cofinanciado pelo ML — calculo margem muda"
      }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Range permitido:*\nR$ 600 - R$ 1899,98" },
        { "type": "mrkdwn", "text": "*Sugerido ML:*\nR$ 1799,98 (10%)" },
        { "type": "mrkdwn", "text": "*Teto cenario:*\nR$ 1799,97 (10%)" },
        { "type": "mrkdwn", "text": "*Delta vs teto:*\n+R$ 0,01" }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Abrir /aprovacoes" },
          "url": "https://promos-meli-supabase.lovable.app/aprovacoes"
        }
      ]
    }
  ]
}
```

Preview e testa em **`app.slack.com/block-kit-builder`** — UI oficial pra mexer no JSON e ver como fica.

---

### Pitfalls comuns

#### P-Slack-1 — URL com whitespace ou newline (comum em paste)

**Sintoma**: webhook retorna 400 ou nao publica nada.

**Causa**: ao colar a URL no campo de secret (Lovable Cloud, Supabase, .env), as vezes vem 1 espaco no fim ou newline invisivel. Slack rejeita.

**Fix**: 
- Quando colar no Bitwarden, ja confere visualmente — sem espaco no fim
- Quando setar via terminal, usa `printf %s` em vez de `echo`:
  ```bash
  printf '%s' 'https://hooks.slack.com/services/...' | vercel env add SLACK_WEBHOOK_PROMOS_ML
  ```
- Se ja setou e nao funciona, deleta o secret e recria — checa o valor depois

**Relacionado**: P-01 (caso real OAuth ML que custou 1h pra descobrir).

#### P-Slack-2 — Webhook revogado por seguranca

**Sintoma**: app de repente para de postar, log mostra `404 invalid_token` ou similar.

**Causa**: voce (ou alguem) commitou a URL em repo publico, GitHub detectou, Slack revogou automatico.

**Fix**: cria webhook novo (mesmo passo-a-passo), atualiza secret. Garbage collect: confere `git log -p` pra confirmar onde vazou e remove (BFG / git filter-repo se ja foi pra remote).

**Prevencao**: regra de ouro — webhook URL **so** em secret manager, nunca no codigo.

#### P-Slack-3 — Mensagem muito longa truncada

**Sintoma**: mensagem aparece cortada no canal.

**Causa**: Slack limita 40000 chars no body, mas blocos individuais tem limites menores (3000 chars/section, 50 blocks total).

**Fix**: divide em multiplas mensagens OU pagina (ex: "Pagina 1/3...") OU resume (3 linhas + link pra ver completo no app).

#### P-Slack-4 — Rate limit silencioso

**Sintoma**: mensagens param de chegar apos rajada (~1 por segundo aceito, mais que isso comeca a falhar).

**Causa**: Slack rate-limit incoming webhook (~1 msg/seg sustentavel).

**Fix**: pra notificacoes em batch (ex: varredor que classifica 50 candidates), agrupa numa mensagem so com sumario + link, em vez de 1 por candidate.

---

### Quando virar bot token (proximo nivel)

Se o app comecar a precisar:
- **Editar** mensagem ja postada (ex: marcar "aprovado por X" no card depois da decisao)
- **Postar em multiplos canais** dinamicos (cliente A vai pra `#cliente-a`, cliente B pra `#cliente-b`)
- **Reagir** a clicks de botao (Approve / Reject) na propria mensagem
- **Threads** (responder a mensagem original em vez de poluir o canal)

→ Migra pra Slack App com Bot User + `SLACK_BOT_TOKEN`. Custos: +30min de setup (criar bot user, dar scopes `chat:write`, `chat:write.public`, instalar no workspace, salvar token + channel ID).

PROMPT_6 (App Promos ML MVP) **NAO** precisa disso — webhook resolve.

---

### Como ensinar esse modulo no evento

```
0:00 — "Quem aqui ja recebeu notificacao do GitHub no Slack quando alguem abre PR?"
       (todos levantam mao)
       "Voces vao fazer igual em 5 minutos."

1:00 — Mostra ao vivo:
       - api.slack.com/apps → Create
       - Activate Incoming Webhooks
       - Copy URL
       - curl com a URL → mensagem aparece no canal
       (~3min total)

4:00 — "Pronto. Agora voces sabem postar mensagem do app de voces no Slack.
       Sem programar. Sem API key. So uma URL secreta."

5:00 — Mostra os 4 pitfalls com print:
       1. Whitespace na cola
       2. Revogado por commit no GitHub
       3. Mensagem truncada
       4. Rate limit batch

8:00 — Block Kit Builder ao vivo (~2min):
       - Abre app.slack.com/block-kit-builder
       - Cola exemplo
       - Mexe num campo, ve mudar
       - "Esse JSON cola no body do POST. So isso."

10:00 — "Quando virar dor (editar mensagem, multiplos canais, reagir a click),
        ai migra pra bot token. Mas primeiros 6 meses do app, webhook resolve."
```

---

### Conexao com framework Elo

Esse modulo cobre **a Fase 02 (Construir)** — toda app real precisa avisar humano em algum momento, e webhook Slack e o caminho mais curto. Tambem reaparece na **Fase 03 (Evoluir)**, quando o webhook simples vira bot token pra fluxos mais elaborados.

Combinado com `THINKING_WITH_AI.md`:
- Quando bater num pitfall do Slack (URL com whitespace, rate limit, etc), aplica Reactive Learning: copia o erro, traz evidencia (response do curl, log do app), pede pra IA traduzir e corrigir.

---

### Templates de prompt pra IA

#### Template 1 — Webhook nao funciona

```
Configurei webhook Slack pelo passo-a-passo. Testei com curl mas
recebo [HTTP code / mensagem]. Por favor:
1. Lista as 3 causas mais comuns desse erro
2. Pra cada uma, como diagnosticar em 30 segundos
3. Pra cada uma, como consertar

Erro:
[COLA AQUI O OUTPUT DO curl]
```

#### Template 2 — Quero formato bonito (Block Kit)

```
Quero postar mensagem no Slack com [descreve: header + 3 fields +
botao linkando pra meu app]. Por favor:
1. Me da o JSON Block Kit pronto
2. Explica como testar em app.slack.com/block-kit-builder antes
   de jogar no codigo
3. Lista limites a respeitar (chars por bloco, total de blocos)

Conteudo:
- Header: [...]
- Fields: [...]
- Botao: [texto, URL]
```

#### Template 3 — Migrar pra bot token

```
Meu app usa incoming webhook do Slack hoje, mas precisei de
[edit de mensagem / multiplos canais dinamicos / botao com callback].
Por favor:
1. Me da o passo-a-passo de migrar pra Slack App com bot user
2. Lista os scopes minimos necessarios pro meu caso
3. Mostra o que muda no codigo do app (1 envvar a mais? funcao
   de chamada diferente?)

Stack do app: [Lovable Cloud TanStack / Supabase EF / etc]
```

---

### Apos este modulo

1. Aluno tem webhook Slack funcionando do app dele
2. Aluno guardou a URL nos 3 lugares certos (Bitwarden + secret + .env.example)
3. Aluno testou Block Kit Builder pra mensagens ricas
4. Aluno sabe os 4 pitfalls comuns + como prevenir
5. Pode prosseguir pra qualquer prompt que dispare notificacao Slack (PROMPT_6, PROMPT_9, PROMPT_10)

---

---

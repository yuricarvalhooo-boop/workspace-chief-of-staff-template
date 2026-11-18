---
{
  "id": "HOMER-lovable-07",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "lovable",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "928e1cb3369e8a8c318b3852b7de5a9705e727ca7847e2d359332e4cd002b376",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 07-pitfalls — lovable

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** lovable. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# Pitfalls Reais — Vibe Coding com Lovable + Supabase

> Catálogo de tropeços reais que vivemos no build do **App Promos ML** (08/05/2026)
> e em sessões anteriores. Cada um vira material didático pro evento Elo:
> sintoma → causa → fix → como prevenir → template de prompt pra IA quando bater.

> **Como usar**: aluno bate num erro, busca aqui pelo sintoma, pega o caminho.
> Reactive Learning estruturado — não decora teoria, consulta quando precisa.

---

### 🚩 P-05 — Iframe do editor bloqueia OAuth

**Sintoma**: clica "Conectar conta ML" dentro do editor Lovable e o navegador (Firefox/Chrome) bloqueia com mensagem "não consegue abrir" ou simplesmente não navega.

**Causa**: o preview Lovable roda em **iframe**. Quando o app faz `window.location.href = authorize_url`, é navegação cross-origin (`lovable.app` → `auth.mercadolivre.com.br`) **dentro de iframe**, e o navegador bloqueia por política de segurança (CSP, X-Frame-Options).

**Fix**: testar OAuth sempre em **aba/janela própria** (top-level window).
1. No editor Lovable, ícone "Open in new tab" do preview (geralmente quadrado com seta)
2. Ou copia URL do preview e cola em nova aba
3. Faz tudo lá: login, navegação, "Conectar"

**Prevenção**: regra fixa — *"OAuth nunca testa dentro do iframe do editor"*. Tirar print disso pra slide.

---

### 🚩 P-10 — Domínio do preview muda entre builds

**Sintoma**: tu testou em `https://id-preview--<id>.lovable.app/...` ontem, deu OK. Hoje tudo dá 404. Secrets que apontam pra essa URL (APP_URL) param de funcionar.

**Causa**: Lovable às vezes muda o domínio do preview entre builds (ex: vira `https://preview--<name>.lovable.app/`, sem o `id-preview--` e usando nome amigável do projeto).

**Como diagnosticar**: pegar `preview_url` atual do projeto (UI Lovable, "Open in new tab" do preview, ou MCP `get_project`) e comparar com a URL que tu tava testando.

**Fix**:
1. Atualiza `APP_URL` secret pro novo domínio
2. Se OAuth provider tem allowlist de redirect_uri, atualiza lá também (callback Supabase não muda — esse é estável)

**Prevenção**: **publicar o app** (Publish no Lovable) ganha URL estável `<project>.lovable.app`. Pra produção, sempre publicar e usar URL estável.

---

### 🚩 P-12 — Lovable Cloud + Supabase externo funciona

**Crença antiga (pré-mai/2026)**: "Lovable Cloud não permite vincular Supabase externo". 

**Verdade atual**: vincula sim. SQL Editor aparece, Edge Functions deployam, secrets manageados — tudo.

**Confusão deriva de**: ML6 e outros artigos de migração que falam "Cloud é caixa preta, vai ter que migrar pra Supabase real depois". Era verdade no início, **não é mais**.

---

## Editor Lovable & Preview

### 🚩 P-13 — Sessão do editor ≠ sessão do preview standalone

**Sintoma**: dentro do iframe do editor, todas as rotas autenticadas funcionam. Abre a mesma URL em nova aba (preview standalone) → 404 ou redirect pra login.

**Causa**: cookies/sessão do editor ficam **isolados** do preview standalone (cross-domain isolation). Login feito no editor não vai junto.

**Fix**: faz login direto no preview standalone (`/login` em aba nova) **antes** de navegar pra rotas autenticadas.

---

### 🚩 P-14 — "Build failed" no chat mas preview funciona

**Sintoma**: chat do Lovable mostra `build failed with exit status 1: ...`. Tu pira. Mas o preview continua renderizando.

**Causa**: warnings de Vite/Rollup às vezes saem com exit status 1 (lint, typecheck, ou outro step menor) **sem impedir o dev server**. Lovable mostra como "build failed" sendo apenas warning.

**Diagnóstico rápido**: olha o preview no navegador. Se carrega → tá vivo, segue. Se não carrega → aí é problema real.

**Prevenção**: **olha o preview primeiro, painel de erro depois**. Não entra em pânico antes de testar.

> ⚠️ Mas tenta o **publish** também — warnings podem virar erros fatais lá (ver P-09).

---

### 🚩 P-17 — TanStack Start: fetch interceptor exige `createIsomorphicFn`

**Sintoma**: builder cria server function que faz fetch, dá erro de "import-protection" ou "module not allowed in client". Build trava ou client bundle quebra ao carregar.

**Causa**: TanStack Start é isomórfico — código server pode importar coisas server-only (Node APIs, service_role client, etc). Mas se tu **importa esse server-only direto num arquivo lido pelo client**, build protege com erro.

Acontece tipicamente quando:
- Builder cria interceptor de fetch (pra logar todas as requisições, ou injetar headers)
- Coloca o interceptor em arquivo importado de ambos lados
- Tenta importar API Node-only (ex: `@supabase/supabase-js` server-side features) no client

**Fix idiomático TanStack**: usar `createIsomorphicFn`:
```ts
import { createIsomorphicFn } from '@tanstack/react-start';

const installInterceptor = createIsomorphicFn()
  .server(() => {
    // no-op no servidor (já tem fetch nativo configurado)
  })
  .client(() => {
    // instala wrapper só no client
    const orig = window.fetch;
    window.fetch = async (...args) => {
      // ...
      return orig(...args);
    };
  });
```

**Caso real Empresa Cloud, 08/05/2026**: durante o build do app `Promos-meli-cloud` com OAuth, builder criou interceptor que importava server-only do client. Build falhou com "import-protection". Fix automático aplicado: trocou pra `createIsomorphicFn` (no-op server, instala interceptor só no client). Resolveu.

**Prevenção**:
- Convenção `*.server.ts` força bloqueio em compile-time se importado em código client
- Se erro de import-protection: pedir builder usar `createIsomorphicFn` em vez de import condicional manual

**Template pro aluno usar com IA**:
> *"Build TanStack Start falhou com erro de import-protection / module-not-allowed. O arquivo X é client/server isomórfico. Como uso `createIsomorphicFn` ou separação `.server.ts` / `.client.ts` pra resolver?"*

---

### 🚩 P-16 — Migration history conflita ao mudar de projeto Lovable

**Sintoma**: Lovable tenta aplicar migration com nome que já existe → erro de hash ou skip silencioso.

**Causa**: Supabase mantém `supabase_migrations.schema_migrations`. Migrations com nomes iguais aplicadas por projetos diferentes podem conflitar.

**Fix**: ou renomeia migration nova (timestamp diferente), ou pula a etapa.

**Prevenção**: ao recriar projeto Lovable contra Supabase existente, sempre listar `schema_migrations` antes pra ver o que já foi aplicado.

---

### 🚩 P-39 — Lovable Cloud `project--<id>.lovable.app` retorna 404 ate o primeiro Publish (caso real 13/05)

**Sintoma**: cron com URL `https://project--<uuid>.lovable.app/api/public/sweep-tick` schedulado, pg_cron rodando minutely, `net._http_response` mostra `status_code=404, body="Project not found"`. App funciona normal no editor + preview, mas a URL "publish-stable" nao responde.

**Causa**: a URL `project--<id>.lovable.app` (sem `id-preview--` no inicio, sem `-dev` no fim) so ativa **depois do primeiro Publish** do projeto Lovable. Ate la, o roteamento publico nao conhece esse projeto.

**Caso real Empresa 13/05**:
- App Cloud aplicou PROMPT_10 inteiro em preview
- Cron schedulado apontando pra URL publish-stable
- `sweep_tick_log` vazio. Investigacao via `net._http_response` revelou 404 a cada minuto

**Fix**:
- **Pro evento e producao**: clica Publish 1x. URL congelada ativa, cron passa a responder.
- **Pra preview-only smoke** (nao recomendado pra cron permanente): troca URL pra `https://project--<id>-dev.lovable.app/...` (sufixo `-dev`), que pega ultimo build de preview. Frageis — qualquer edit no editor pode quebrar tick.

**Prevencao**:
- Antes de schedular cron, valida: `curl -X POST <url>/api/public/<endpoint>` retorna 200 (ou pelo menos 405/406, indicando que a rota existe). Se 404, **publish primeiro**.
- Apos schedule, sempre olha `net._http_response` pelos primeiros 2-3 ticks. 404 sistematico = URL errada.
- **Pro evento**: didaticamente isso justifica ensinar **fluxo preview→publish→prod**, que e o que aluno vai usar no projeto real dele.

---

## P-46 — Cron `pg_net.http_post` apontando pro frontend Lovable em vez da Edge Function

**Categoria**: Infra & Cron

**Sintoma**: `cron.job_run_details.status='succeeded'` (pg_net enfileirou OK), mas EF nunca executa. `net._http_response` revela 404 com HTML SPA do frontend.

**Causa**: Lovable Cloud expõe EFs via proxy `/api/public/<nome>` na URL do app (`<project>.lovable.app`), não via `<ref>.supabase.co/functions/v1/<nome>`. Se cron foi setado com URL errada (ou rota que não existe), Lovable retorna SPA HTML 404 maquiado.

**Caso real Empresa 14/05**:
- Cron Cloud `schedule-tick-1min` apontava pra `https://sentinela-promos-demo.lovable.app/api/public/schedule-tick`
- Mas a rota `/api/public/schedule-tick` não existia (PROMPT_11 criou no source mas faltou Publish)
- Retorno: SPA HTML 404
- `cron.job_run_details.status='succeeded'` mascarou tudo (pg_net considera "succeeded" qualquer 2xx ou 4xx HTTP — não distingue 200 OK de 404 HTML)

**Fix**:
1. **Identificar**:
   ```sql
   SELECT id, status_code, LEFT(content::text, 200) AS body, created
   FROM net._http_response
   WHERE created >= NOW() - INTERVAL '15 min'
   ORDER BY id DESC LIMIT 10;
   ```
   Body começando com `<!DOCTYPE html>` é sinal forte de URL errada / Lovable 404.

2. **Resolver**: garantir que a EF/rota existe (Publish após mudança source) + URL no cron está certa. Testar manual via curl antes de schedule.

**Prevencao**:
- Pra cron `pg_net.http_post`, **sempre** validar a URL via `curl -X POST <url>` antes de schedule. Se retorna HTML → URL errada. Se retorna JSON da EF → ok.
- **Reflexo 6 do framework Elo** (já no doczao): `cron.job_run_details.status='succeeded'` ≠ "EF executou". Sempre olhar `net._http_response.status_code` + body real.

---

## P-52 — Deploy stale no Lovable Cloud: source corrigido, runtime antigo

**Categoria**: Cron/Infra & Deploy

**Sintoma**: hotfix aplicado e confirmado no código-fonte (grep mostra a mudança certa, branch removido), mas o comportamento em produção continua o antigo. No caso: cupons `SELLER_COUPON_CAMPAIGN` saíam com `decision_reason="within_teto"` (branch que **foi deletado** do classifier).

**Causa**: no Lovable Cloud, "aplicar" o código (o agent edita + commita) **não publica**. O Worker Cloudflare em produção continua servindo o build anterior até um **Publish** explícito. O apply atualiza o editor + git; o runtime é outra coisa.

**Smoking gun do diagnóstico**: um `decision_reason` que **só existe no código removido** apareceu em registros novos. Se o string não tem como ser produzido pelo source atual, o runtime está rodando outra versão. Esse tipo de evidência (string órfã de código deletado) é prova direta de staleness.

**Caso real Empresa 15/05**: hotfix P-49 (paginação) + P-50 (skip cupom) commitado, mas job rodou com `totals.total=1000` (truncamento persistiu) e cupons como `enter_auto/within_teto`. Republish resolveu os dois de uma vez.

**Fix**: republicar. Confirmar antes: comparar timestamp do "Last published" com o commit do apply. Se published < commit → stale.

**Prevenção**: **"o agent aplicou" ≠ "está em produção".** O caminho de diagnóstico de staleness **difere por infra**:
- Supabase Edge Function (app Externo): checar `version` da função (incrementa a cada deploy).
- Lovable Cloud / Cloudflare Worker (app Cloud): checar timestamp do **Publish**, não há "version" de função.

Generaliza o reflexo R6 do doczao ("succeeded ≠ funcionou de verdade") pro plano de deploy: um apply bem-sucedido num editor não diz nada sobre o que o runtime serve.

---

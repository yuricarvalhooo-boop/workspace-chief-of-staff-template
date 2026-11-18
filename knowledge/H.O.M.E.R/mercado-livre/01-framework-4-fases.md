---
{
  "id": "HOMER-mercado-livre-01",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "mercado-livre",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "bba61b35b6daf83e94fc6f1cc7be0c423be4643e79b3d3dd5e9e285c2f4cdb3d",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 01-framework-4-fases — mercado-livre

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** mercado-livre. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

### Trilha A (Caso Empresa) — sumario
- **Estado atual**: pessoa operacional do exemplo, 4-6h/mes, 1500 MLBs, planilha, R$ 119/mes custo direto
- **Question**: 80% das vendas Empresa ML vem de promo. Processo NAO da pra eliminar
- **Delete**: replicar promos manualmente (delete), planilha como source-of-truth (delete), conferencia 1x1 (delete)
- **Simplify**: bulk-edit via planilha, default "mantem o que estava" se nao tem regra nova
- **ROI**: R$ 1,2-1,3M/mes faturamento, 2% uplift = R$ 24-26k/mes + 2% margem extra com promo compartilhada = **>R$ 50k/mes potenciais**
- **Decisao**: AUTOMATIZAR

Detalhes em `2026-05-05-app-promos-ml-fase00.md`.

### Trilha A (Caso Empresa) — sumario
- **1.0**: usamos Claude Code (esta sessao)
- **1.1**: API ML `/seller-promotions` cobre todos 12 tipos. Webhook ja tem topic `candidate_id`. Rate 1500 req/min OK
- **1.2**: standalone novo (frontend) + reuso seletivo Sentinela (auth, EFs, Slack helper)
- **1.3**: web app, 3 paginas essenciais + 1 bonus, 3 crons + 1 webhook handler
- **1.4**: data model `promo_*` em 4 tabelas + view; decision tree de 5 steps
- **1.5**: PROMPT_BUILDER.md pronto

Detalhes em `2026-05-05-app-promos-ml-spec.md` e `PROMPT_BUILDER_app-promos-ml.md`.

### Trilha A (Caso Empresa) — roadmap pos-MVP
- Migrar codebase pra dentro do Sentinela (frontend + EFs)
- Regras por familia/categoria pra evitar canibalizacao interna por desconto
- Integracao com Tiamat pra calculo de teto via margem real
- Dashboard `/promos-roi` com vendas atribuidas a promo
- Multi-tenant (outras contas ML)
- Conexao com sistema de precificacao

### 5o reflexo (caso real 12/05) — "Falha do provider pode ser estado do recurso, nao overload"

Sessao 12/05: rodando adesao em massa pra campanha MAIO (1167 anuncios Empresa),
81 GETs retornaram HTTP 400 "Service temporarily overloaded". Retry generico com
throttle 5s recuperou 76 — sobraram 4 persistentes.

Em vez de continuar retry indefinido, paramos e diagnosticamos. Validacao em
1 curl revelou os 4 estavam em `under_review` no ML — moderacao do anuncio
em curso. O endpoint retornava "overloaded" enganadoramente, mas a causa
real era estado do recurso, nao infraestrutura.

**Reflexo**: quando retry com throttle nao resolve, **trocar de hipotese**.
Pode nao ser carga, pode ser estado do recurso. Pre-flight check do status
do recurso antes de chamar endpoints dependentes. P-33 no PITFALLS.md (`PITFALLS.md`, no material original).

Outros 2 aprendizados da mesma sessao:
- **P-34**: planilha de mes anterior NAO e contrato de elegibilidade do mes
  seguinte. ML decide quais items entram em cada campanha por politica
  interna opaca. 29 de 1167 items ativos nao receberam MAIO sem motivo
  visivel. Aceitar margem, nao tentar 100%.
- **P-35**: unique constraint em campo "metadata" (SKU) quebra cenarios
  reais. 1 SKU mapeia varios MLBs em e-commerce. Builder default cria
  constraint assumindo 1-pra-1, fura no primeiro upload em massa. Sempre
  validar com 3 exemplos reais antes de aceitar migration.

### 6o reflexo (caso real 13/05) — "Bearer pass-through > env var lookup em chained EFs"

Sessao 13/05: subindo motor de batch sweep nos 2 apps Lovable (Cloud + Externo).
Externo aplicou: `sweep-tick` (EF) chamava `promo-activate` (EF) com
`Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`. Resultado: **HTTP 401 a
cada chamada**, com a key "certa", a EF receptora "certa", em projeto Supabase
"certo".

Triangulacao em 5min revelou: a key injetada no env do runtime da EF estava
**diferente** da key visivel no Dashboard (que era a mesma do cron.job, e que
eu provei funcionar invocando `promo-activate` direto via `pg_net`). Drift
silencioso entre key-no-env e key-no-Dashboard.

**Fix idiomatico**: nao lê env, repassa o Authorization entrante. EF chamada
por cron com Bearer correto repassa o **mesmo Bearer** pra proxima EF:

```ts
// antes (frágil — depende de env consistente)
fetch(url, { headers: { Authorization: `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}` } });

// depois (resiliente — passa o que recebeu)
fetch(url, { headers: { Authorization: req.headers.get("Authorization")! } });
```

**Reflexo**: pra **qualquer arquitetura multi-EF/multi-service**, o caminho
idiomatico e propagar a credencial entrante, nao reautenticar do zero. Env
vars sao otimos pra clients internos (Postgres, integracao SDK); ruins pra
HTTP outbound chained. Pattern documentado em
`BEARER_PASSTHROUGH.md` (`BEARER_PASSTHROUGH.md`, no material original).

Outros 6 pitfalls da mesma sessao (P-36 a P-41 em PITFALLS.md (`PITFALLS.md`, no material original)):
- **P-36**: placeholder `<KEY>` nao substituido em SQL vira JWT invalido silencioso
- **P-37**: `ALTER DATABASE postgres SET app.*` bloqueado em Supabase managed (42501)
- **P-38**: drift `SUPABASE_SERVICE_ROLE_KEY` env vs Dashboard (esse mesmo reflexo)
- **P-39**: Lovable Cloud preview URL `project--<id>.lovable.app` retorna 404 ate primeiro Publish
- **P-40**: UI consulta colunas do plano original mas migration usou nomes diferentes → tela vazia silenciosa
- **P-41**: `pg_cron`/`pg_net` precisam migration (superuser) pra `CREATE EXTENSION`, nao SQL editor

### 7o reflexo (caso real 13/05) — "Triangulacao 3 snapshots vira debug primary em multi-service"

Sessao 13/05 aplicou a heuristica de `THINKING_WITH_AI.md` (`THINKING_WITH_AI.md`, no material original)
2 vezes pra resolver 401s opacos:

**Caso 1** (cron→EF): `cron.job_run_details.status='succeeded'` mas EF retornava
401. Triangulacao: (1) que key cron envia? `regexp_match(command, 'Bearer (.+)')`,
(2) que EF aceita? invocacao manual via `pg_net` com a mesma key, (3) que
verify_jwt requer? doc Supabase. Resultado: key estava com placeholder
`<SERVICE_ROLE_KEY>` literal, nao substituido.

**Caso 2** (EF A→EF B): `sweep-tick` chamava `promo-activate` com 401.
Triangulacao: (1) chamada direta de `promo-activate` via `pg_net` com key
do `cron.job` → **200 OK** (key + EF receptora corretas), (2) chamada via
`sweep-tick` → **401** (mesma key esperada, comportamento diferente). Isolou
em: a key e diferente "de dentro" da EF chamadora. Fix = Bearer pass-through.

**Reflexo**: pra debug de auth/4xx em arquitetura distribuida, sempre construa
**3 snapshots**: (a) o que vc esperava, (b) o que o codigo calculou, (c) o que
o servico realmente recebeu. Esse padrao funciona pra ML APIs, Supabase Edge
Functions, webhooks, qualquer coisa onde "a chamada foi feita" e diferente
de "a chamada foi aceita". Promover a **debug primary** em vez de "retry com
log generico".

### 8o reflexo (caso real 13/05) — "Plataforma managed esconde controles. Aceita ou contorna."

Sessao 13/05 deparou com 3 limites de plataforma:
- **Supabase Cloud**: bloqueou `ALTER DATABASE postgres SET app.*` (custom GUC). 1h perdida tentando "esconder" service_role do cron.job. Aceitou: inline em plain text, so superuser ve.
- **Lovable Cloud**: nao expoe `SUPABASE_SERVICE_ROLE_KEY` no painel. Aluno tem que ir no Supabase Dashboard underlying pra copiar. Contornou via Opcao A (sem auth no tick + advisory lock).
- **pg_cron sem segundos**: pg_cron padrao Supabase nao aceita `'30 seconds'` schedule. Aceitou `'* * * * *'` (1min). UX da pessoa operacional do exemplo nao muda.

**Reflexo**: cada plataforma managed tem **footguns invisiveis** documentados pelo silencio (nao tem na doc, voce descobre tropecando). Aluno do evento Elo vai bater nesses. Reacao saudavel:
1. **Reconhece o limite** (sem batalhar contra a plataforma)
2. **Pondera tradeoff** (custo da gambiarra vs cost da solucao "limpa")
3. **Aceita ou contorna** (decisao consciente, documenta o porque)
4. **Promove ao publico** se for repetivel (vira PITFALLS.md)

Esse 8o reflexo e o **anti-perfectionism** do framework Elo: dev real escolhe
trabalhar com a plataforma, nao contra ela. Saber quando recuar e parte da
maestria.

### 9o reflexo (caso real 14/05) — "Antes de POST, leia o status do GET — idempotencia por estado remoto"

Sessao 14/05: o varredor diario re-tentava aderir promocoes que ja estavam
aderidas — cada run disparava 1120+ POSTs redundantes pro ML, varios falhando
feio. O ML ainda auto-propaga cupons (`SELLER_COUPON_CAMPAIGN`) pros items
elegiveis sem o app pedir.

O fix nao foi um retry mais esperto — foi parar de POSTar o que ja estava feito.
O classifier passou a ler o `status` do candidato no GET (`started`/`pending`/
`programmed`) e pular antes de qualquer POST. Custo zero, matou 1120+ chamadas/dia.

**Reflexo**: antes de uma acao que muta um recurso externo, leia o estado atual
desse recurso e pule se ja esta no estado desejado. Idempotencia nao precisa de
transacao nem lock distribuido — frequentemente e so um GET + um `if`. Vale pra
qualquer integracao. P-50 no PITFALLS.md.

### 10o reflexo (caso real 14/05) — "Erro silencioso do SDK e o adversario invisivel"

Sessao 14/05: 85 adesoes aconteceram mas o Slack nunca avisou. A query que montava
a notificacao usava nested select com 2 FKs, o PostgREST devolveu `PGRST201` — e a
Supabase JS retornou `data: null` sem lancar excecao. O codigo tratava `data`
direto e seguia. Mesmo padrao do truncamento de 1000 linhas (P-49): a query
"funciona", retorna menos do que deveria, ninguem percebe.

**Reflexo**: num SDK que devolve `{ data, error }` em vez de lancar, o `error`
precisa ser checado e logado antes de tocar em `data`. `data: null` nao e "vazio",
que nao e "erro". Erro silencioso e a maior fonte de bug-de-producao — nao aparece
em log nenhum, voce so descobre pelo efeito que faltou. P-48 e P-49 no PITFALLS.md.

### 11o reflexo (caso real 18/05) — "Diagnostico de staleness e especifico da infra"

Sessao 18/05: hotfix commitado e confirmado no fonte, mas producao continuava com
o comportamento antigo. No Lovable Cloud, "o agent aplicou" nao publica — o Worker
serve o build anterior ate um Publish explicito.

A pergunta "o codigo esta certo, por que nao funciona?" tem caminhos de verificacao
diferentes por plataforma: Edge Function Supabase → cheque o numero de `version`;
Worker via Lovable Publish → cheque o timestamp do ultimo Publish vs o commit.

**Reflexo**: antes de diagnosticar "por que o fix nao pegou", saiba onde o runtime
mora e como aquela infra revela a versao em producao. Staleness de deploy nao tem
sintoma universal — tem um por plataforma. P-52 no PITFALLS_2026-05-18.md.

### 12o reflexo (caso real 18/05) — "Agent orquestra agent"

Sessao 18/05: o build do modo agressivo rodou com o Claude Code pilotando o agent
do Lovable por linguagem natural via MCP — manda o prompt, le o fonte, revisa o
diff, valida no banco. Loop fechado entre duas IAs, sem humano transportando
prompt de uma janela pra outra.

O humano nao saiu — mudou de papel: vira aprovador de iteracao e dono do publish,
nao o copista entre as IAs.

**Reflexo**: quando uma IA opera ferramentas que pilotam outra IA, o trabalho do
humano sobe de nivel — de executor pra revisor. Desenhe o loop com gates
explicitos nos pontos irreversiveis; deixe o resto correr agent-a-agent. E uma
narrativa central do Elo: a alavanca nao e uma IA melhor, e a orquestracao.
Ver PITFALLS_2026-05-18.md.

### 13o reflexo (caso real 18/05) — "A assinatura do bug aponta a versao"

Sessao 18/05: cupons saiam de producao com `decision_reason="within_teto"` — um
valor que so existe num branch de codigo que foi deletado. Se um dado novo carrega
uma string que o codigo atual nao tem como produzir, o runtime esta rodando outra
versao. Achar essas "strings impossiveis" foi diagnostico mais rapido que comparar
timestamps de deploy.

**Reflexo**: quando suspeitar de staleness, procure no dado recente um valor que so
o codigo antigo produzia. A presenca dele e prova direta de qual versao esta no ar
— o dado carrega o codigo que o gerou. P-52 no PITFALLS_2026-05-18.md.

### 14o reflexo (caso real 18/05) — "Transporte cair nao quer dizer acao falhou"

Sessao 18/05 (execucao do modo agressivo): o `send_message` que mandava a UI pro
agent do Lovable perdeu a resposta no meio — transporte MCP dropado. Parecia que
nao tinha chegado. Mas o `list_edits` mostrou a edicao "Adicionou modo agressivo
UI" ja commitada: o agent recebeu, trabalhou e terminou — so a resposta se perdeu
na volta.

**Reflexo**: numa orquestracao agent-a-agent, o canal de resposta cair nao e o
mesmo que a acao nao ter acontecido. Antes de retransmitir, verifique o estado do
agent-alvo (historico de edicoes, diff, versao) — retransmitir cego arrisca
duplicar o trabalho. E o complemento do 12o reflexo: orquestrar agent inclui saber
consultar o estado do outro, nao so mandar comando. Ver PITFALLS_2026-05-19.md.

### 15o reflexo (caso real 18/05) — "Evoluir sem medo: o conservador continua sendo o default"

Sessao 18/05: a feature inteira do modo agressivo foi pra producao sem feature-flag
e sem branch — porque cada caminho de codigo novo e gated numa coluna booleana
`aggressive` com `DEFAULT false`. Todo job e agendamento que ja existia continua
`false` → comportamento byte-identico ao anterior, garantido por testes de
regressao verdes.

**Reflexo**: uma evolucao e segura de soltar quando o estado herdado cai no
comportamento antigo por construcao, nao por sorte. A pergunta de Fase 03 "como
solto isso sem quebrar o que ja funciona?" tem resposta de design: faca o novo ser
opt-in no nivel do dado (a coluna default-false), nao no nivel da torcida. Quem ja
existe nem percebe que mudou algo. Ver PITFALLS_2026-05-19.md.

> **Nota de consolidacao (numeracao)**: os reflexos 1-8 nasceram na Fase 02 e
> inicio da Fase 03 (07-13/05). Os 9-15 vieram das sessoes seguintes — estavam
> catalogados crus nos logs `PITFALLS_2026-05-14.md` / `_18.md` / `_19.md`, la com
> numeracao de sessao "RNN" (com saltos). Esta e a sequencia canonica 1-15 pro
> evento. Reflexo novo daqui pra frente: pega o proximo numero desta lista.

---

### Specs do Caso (App Promos ML)
- `2026-05-05-app-promos-ml-fase00.md` — Diagnostico Fase 00
- `2026-05-05-app-promos-ml-spec.md` — Spec funcional Fase 01
- `PROMPT_BUILDER_app-promos-ml.md` — Input pronto pra Fase 02

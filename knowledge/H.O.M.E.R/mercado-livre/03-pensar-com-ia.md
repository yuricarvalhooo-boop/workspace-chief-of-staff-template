---
{
  "id": "HOMER-mercado-livre-03",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "mercado-livre",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "8a98e60c344836af7b2f4c5bbf7a14ffe030d1fa8f69d819061c55dbd92475a7",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 03-pensar-com-ia — mercado-livre

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** mercado-livre. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

## 3 casos reais da sessao App Promos ML

Cada caso = momento exato onde responsável pelo exemplo trouxe evidencia, IA recalibrou, fluxo melhorou.

### Caso 1 — "MAIO1 nao aderiu nesse MLB"

**Contexto**: app testou aderir promos em 3 MLBs. Pra MLB4149113708, IA esperava que todas elegiveis aderissem.

**IA achava**:
> Algoritmo: `deal_price = min(suggested_discounted_price, teto_price)`. Pega o **menor** preço dentro do permitido.

**responsável pelo exemplo foi conferir**: abriu UI ML do anuncio, viu botao "Participar" (= ainda nao aderido) ao lado de MAIO1.

**responsável pelo exemplo trouxe**:
> "ML sugere R$ 11 de desconto, temos teto de 10%. Ele aceita menos? Em alguns tipos pode aceitar mais ou menos do que sugere — temos que validar."

**IA recalibrou**:
- Re-leu o range: `min_discounted_price` = **menor preço final** = MAIOR desconto
- Inverteu o algoritmo: `deal_price = max(suggested, teto_price)`
- Logica: se sugerido ja da MENOS desconto que teto, usa sugerido (preserva margem). Se sugerido fura teto, usa teto exato.

**Validacao empirica**: POST com `deal_price=148.34` (sugerido = 5% off, dentro do teto 10%) → HTTP 201 + status=started. Algoritmo confirmado.

**Aprendizado**: a IA tinha **estrutura certa** (compara sugerido com teto), mas **operador errado** (min vs max). Voce pegou isso so porque foi olhar a UI e perguntou.

---

### Caso 2 — "Lightning ficou pending = aprovacao humana?"

**Contexto**: app POSTou adesao em LIGHTNING (Oferta Relâmpago). API retornou 201 mas com `status: pending`.

**IA achava**:
> `pending` = aguardando aprovacao do ML. App precisa fluxo humano (tela `/aprovacoes` + Slack) **antes** de POST em LIGHTNING.

**responsável pelo exemplo foi conferir**: abriu UI ML do anuncio, tirou print mostrando:
- Badge azul **PROGRAMADA**
- Texto: "14/maio das 18h às 21h"
- Sem indicacao de "aguardando aprovacao"

**responsável pelo exemplo trouxe** (anexando a imagem):
> "ele ficou programado (ou seja nao carece de revisao) pq inicia dia 14, temos que considerar isso nessas promos, confirma que ficou ativa mas programada por conta da data, vai ser diferente do que de fato precisar de revisao"

**IA recalibrou**:
- `pending` = data futura, **nao** revisao humana
- Logica de diferenciacao: `status === "pending" && start_date > now()` → PROGRAMADA. So vira revisao real se start_date <= now() e ainda `pending`
- Removeu fluxo humano antes do POST em LIGHTNING (deixou auto)
- Reservou tela `/aprovacoes` so pra casos genuinos: `MARKETPLACE_CAMPAIGN` cofinanciado, override manual, casos de tolerance overflow

**Aprendizado**: a IA inferiu o significado de `pending` por **convencao de API generica**. A UI mostrou o que o sistema realmente faz nesse caso especifico. **Convencao ≠ implementacao**.

---

### Caso 3 — "Tem um tipo cofinanciado que nao lembro o nome"

**Contexto**: discutindo regra de adesao por tipo de promo. responsável pelo exemplo mencionou que ML banca parte do desconto em algumas campanhas, mas nao lembrava o nome.

**responsável pelo exemplo trouxe** (sem palpite, deixou IA pesquisar):
> "tem um tipo de promo que existe mas nao temos na nossa conta que sao as compartilhadas com o meli, nao lembro o nome, pesquise na api, essas sao legais pra esses casos pq parte do valor é bancado pelo meli"

**IA pesquisou** em sequencia (caminhos que falharam viram aprendizado):
- `WebFetch` na doc oficial ML → 403 (autenticacao requerida)
- `GET /seller-promotions/promotion-types` → 404 (endpoint nao existe)
- `GET /seller-promotions/users/<SELLER_ID_EXEMPLO>` → ✅ retornou 9 promos da conta Empresa

**O GET trouxe achados extras**:
- Conta Empresa ja tem `DOD-MLB1000` (Deal of the Day) e `LGH-MLB1000` (Lightning) — tipos novos pra catalogar
- `MARKETPLACE_CAMPAIGN` **nao aparece** na conta — Empresa nao foi convidada

**Decisao consciente**: como nao tem dado real, MARKETPLACE_CAMPAIGN sempre vai pra tela `/aprovacoes` ate aparecer e poder testar. **Nao vale especular sobre payload/comportamento sem amostra real**.

**Aprendizado**: a IA pode pesquisar ativamente e voce nao precisa lembrar de tudo. Mas a **decisao do que fazer com a falta de informacao** e sua — IA tende a inventar default. Voce limita: "ate testar, manda pra humano".

---

### Caso 4 — "Bug do classifier furou teto, mas como descobrir sem MCP/Claude?"

**Contexto**: smoke do PROMPT_6 v2 aplicou `deal_price=1385.97` (16.51% off) num cenario com teto 10%. Furou teto silenciosamente. responsável pelo exemplo perguntou: "como descobrir esse bug sem voce, so com Lovable AI / ChatGPT, especialmente em projetos Cloud sem MCP do Supabase?".

**Resposta curta**: a vantagem que o Claude teve nao foi inteligencia — foi **3 fontes em paralelo**: (a) MCP do Supabase pra rodar SQL, (b) curl direto na API ML, (c) leitura do codigo. Aluno do Elo NAO tem MCP, mas tem **substitutos gratuitos pra todas as 3**.

**Substitutos das 3 fontes**:

| O que o Claude usou | Substituto sem MCP/Claude |
|---|---|
| `mcp__supabase__execute_sql` | **Cloud SQL editor** (Lovable Cloud → Database → SQL) ou **Supabase Dashboard SQL Editor** |
| `curl https://api.mercadolibre.com/...` | **Postman / Insomnia / curl no terminal** |
| Ler codigo do classifier | **Lovable AI assistant** (no chat do builder, "le X.ts e me explica") |

**A heuristica geral — Triangulacao de 3 Snapshots**

Quando algo nao bate (X foi aplicado mas voce esperava Y):

```
1. O que voce ESPERAVA?     (matematica manual no papel)
2. O que o CODIGO calculou? (le DB + le codigo do classifier)
3. O que o SERVICO retornou? (curl direto na API)

Comparacao:
  Se 1 ≠ 2  → bug de codigo (algoritmo errado, campo errado)
  Se 2 ≠ 3  → comportamento externo (servico esta sobrescrevendo)
  Se 1 = 2 = 3 → nao e bug, e interpretacao errada sua
```

No caso real:
- (1) Esperado: teto 10% → `deal_price=1493.98`
- (2) Codigo aplicou: `1385.97` (cap silencioso pelo `min(deal, maxP)`)
- (3) ML aceitou: `1385.97`

`1 ≠ 2` mas `2 = 3`. **Conclusao**: bug de codigo (cap silencioso furando teto). Sem precisar adivinhar.

**Templates de prompt pra ChatGPT/Lovable AI**:

Template "calculo nao bate":
```
Estou debugando uma funcao que aplicou X em vez de Y. Tenho:

[1] Snapshot do que a funcao recebeu (response_raw->candidate do log):
<COLA JSON>

[2] Cenario configurado:
<COLA row de promo_scenarios>

[3] Codigo da funcao:
<COLA classifier inteiro>

[4] Resultado real aplicado:
<COLA deal_price + discount_pct do log>

[5] O que eu esperava:
<COLA seu raciocinio: "teto 10% deveria virar X">

Por favor:
1. Refaz o calculo passo a passo com os inputs reais
2. Identifica em qual linha o calculo divergiu do esperado
3. Diz se e bug de codigo (qual fix) OU comportamento externo
4. Se for bug, me da o trecho corrigido
```

Template "API mudou comportamento":
```
A API <ML/Stripe/etc> esta retornando dados diferentes pro mesmo
recurso. Snapshots:

ANTES (funcionava):
<COLA o GET de antes>

AGORA (mudou):
<COLA o GET atual>

Hipotese: <"fizemos N tentativas falhas, API pode ter recalibrado">.

Por favor:
1. Confirma o que mudou entre os 2 snapshots
2. Explica se e comportamento documentado ou anomalia
3. Sugere como o app deveria reagir
```

**Aprendizado pedagogico**: a diferenca entre **junior vibe-coder** e **dev assistido por IA**:

- Junior: testa, falha, **assume bug do builder**, pede fix sem dados, builder palpita, novo bug
- Dev assistido: testa, falha, **traz 3 snapshots reais + matematica esperada**, IA debuga com contexto

Sem os 3 snapshots, IA inventa fix. Com os 3, IA debuga em 1 round. **Triangulacao reduz iteracoes em 5-10x**.

**Pre-requisito do app pra triangulacao funcionar**: salvar TUDO em `response_raw` (request enviado + response recebido + http_status + snapshot do candidate). Sem dados auditaveis, voce nao consegue triangular nada. Por isso o Fix 3 do PROMPT_7 e tao importante quanto os outros — sem ele, debug futuro fica adivinhacao.

**Heuristica meta**: pro evento Elo, ensinar antes de codar a primeira EF: **"Salva tudo em jsonb. Em algum momento voce vai precisar fazer arqueologia. O que nao foi salvo, voce nao recupera."**

---

### Caso 5 — "401 fantasma: a mesma key funciona aqui, falha ali"

**Contexto**: sessao 13/05 subindo motor de batch sweep no Supabase Externo. EF `sweep-tick` chamava EF `promo-activate` com `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`. **Toda chamada retornava 401.** Strange — a EF receptora foi a mesma que funcionava no PROMPT_6 (smoke do varrer individual). A key parecia certa. Por que falhava agora?

**O que NAO funcionou**: a primeira hipotese do builder Lovable foi "promo-activate tem verify_jwt=true e nao aceita service_role". Plausivel mas nao verificado. Plus: poderiamos ter aceitado essa explicacao e gastado 1h refatorando autenticacao.

**Triangulacao em 3 snapshots resolveu em <5min**:

```
Snapshot 1 — Que key cron envia?
  regexp_match(command, 'Bearer ([^'\\s]+)') no cron.job
  → length=219, jwt_parts=3, role=service_role, ref=projeto-certo
  → key valida, formato JWT correto

Snapshot 2 — Que key funciona "de fora"?
  Invocacao manual via pg_net usando a mesma key extraida:
  net.http_post('https://.../promo-activate', headers={Bearer <key>}, body={scenario_id})
  → status_code=200, body={"success":true, "aderidas":4, "skipped":2}
  → promo-activate ACEITA essa key

Snapshot 3 — Que key sweep-tick envia "de dentro"?
  sweep-tick lê SUPABASE_SERVICE_ROLE_KEY do env e chama promo-activate
  → status_code=401, body={"code":"UNAUTHORIZED_INVALID_JWT_FORMAT"}
  → A key "do env" e DIFERENTE da key "do Dashboard"
```

`Snapshot 1 = Snapshot 2 = OK` e `Snapshot 3 = falha`. **Conclusao**: a hipotese do builder estava errada (`promo-activate` aceita service_role). O bug e drift entre **key visivel no Dashboard** (que esta no cron.job) e **key injetada no env do runtime da EF**.

**Fix idiomatico** (em vez de refatorar promo-activate, propagacao):

```ts
// EF A nao precisa re-autenticar — repassa o Bearer que JA entrou
const incomingAuth = req.headers.get("Authorization")!;
fetch(`${SUPABASE_URL}/functions/v1/promo-activate`, {
  headers: { Authorization: incomingAuth }  // pass-through
});
```

Documentado em `BEARER_PASSTHROUGH.md` (`BEARER_PASSTHROUGH.md`, no material original) e P-38 em `PITFALLS.md` (`PITFALLS.md`, no material original).

**Aprendizado pedagogico**: a primeira hipotese do builder e palpite com base em padrao comum ("verify_jwt = true bloqueia algo"). Sem triangulacao voce aceita e refatora errado. Com triangulacao, voce isola **exatamente** onde divergiu — frequentemente em lugar inesperado (env var, propagacao, encoding).

**Template prompt pra ChatGPT/Lovable AI**:

```
EF A esta chamando EF B e recebendo 401, mas a mesma key funciona quando 
invoco EF B diretamente via curl/pg_net. Snapshots:

[1] Key que EF A LE do env (decode JWT pra mostrar role/ref/exp):
<COLA>

[2] Key que esta no cron.job/painel (decode JWT pra mostrar role/ref/exp):
<COLA>

[3] Codigo da EF A onde monta o Bearer:
<COLA>

[4] Codigo da EF B onde valida JWT (ou config verify_jwt):
<COLA>

Por favor:
1. Compara key [1] vs [2] — sao iguais? Se nao, qual a diferenca?
2. Identifica se o problema e (a) env dessincronizado, (b) verify_jwt bloqueando, 
   ou (c) outra causa
3. Sugere fix. Se for env drift, prefira pass-through em vez de "atualizar key 
   no env" (que pode rotacionar de novo)
```

**Reflexo arquitetural derivado**: pra chained EFs no mesmo projeto Supabase, **pass-through > env var lookup**. Detalhes em `BEARER_PASSTHROUGH.md` (`BEARER_PASSTHROUGH.md`, no material original).

---

### 6a heuristica (sessao 13/05) — Triangulacao 3 snapshots vira debug primary

Apos aplicar triangulacao 2x na mesma sessao (caso 4 da sessao 10/05 e caso 5 acima da 13/05), e oficial: pra qualquer **divergencia entre o que voce esperava e o que o sistema faz**, triangulacao supera "retry com log generico" em 5-10x.

**Promoção pedagogica**: nao e mais "tecnica avancada". E o **default**. Quando aluno do Elo bater em qualquer bug opaco (401 sem motivo claro, calculo errado, status estranho), o primeiro reflexo a ensinar e:

1. **Para de retry** (retry repetido sem nova hipotese e desperdicio)
2. **Para de pedir fix sem dados** (builder vai palpitar)
3. **Constroi 3 snapshots**: (a) esperado matematicamente, (b) o que o codigo calculou, (c) o que o servico retornou
4. **Compara**, isolando o ponto de divergencia
5. **Pede fix com 3 snapshots colados** (builder debuga com contexto)

Esse loop e o **antidoto pra "vibe debug"** — onde aluno tenta 5 fixes random ate acertar. Triangulacao faz aluno acertar com 1 fix, na 1a tentativa.

---

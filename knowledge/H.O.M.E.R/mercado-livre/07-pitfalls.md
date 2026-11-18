---
{
  "id": "HOMER-mercado-livre-07",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "mercado-livre",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "928e1cb3369e8a8c318b3852b7de5a9705e727ca7847e2d359332e4cd002b376",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 07-pitfalls — mercado-livre

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** mercado-livre. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

### 🚩 P-02 — DevCenter ML/Google com múltiplos apps confunde

**Sintoma**: ML rejeita autorização com "aplicativo não está pronto". Tu confere e o redirect_uri **TÁ** cadastrado no app que tu acessou. Mas continua rejeitando.

**Causa**: tu tem múltiplos apps no DevCenter (ex: 1 pro Sentinela, 1 pro Product Ads, 1 novo pro Promos ML). Adicionou redirect_uri num app, mas copiou `CLIENT_ID`/`SECRET` de outro app. ML recebe request com `client_id=B`, procura redirect no app B, não acha (foi adicionado em A).

**Como diagnosticar**: olha o `client_id` na URL do erro:
```
auth.mercadolivre.com.br/authorization?...&client_id=<ID>&...
```
Vai no DevCenter → lista de aplicações → procura o app com **esse exato App ID** → confirma que o redirect_uri novo está nessa lista.

**Fix**: ou move o redirect pro app certo, ou troca `CLIENT_ID`/`SECRET` no Supabase pelos do app onde a URL ESTÁ cadastrada.

**Prevenção**: sempre confirma `client_id` e `redirect_uri` no MESMO app DevCenter. Ao copiar credenciais, abre **uma única aba** do DevCenter focada no app certo.

---

### 🚩 P-20 — "ML criar promoção vs aderir a promoção" — modelo errado retorna sucesso silencioso ⭐⭐ (caso real)

**Sintoma**: app POST `/seller-promotions/promotions/PRICE_DISCOUNT/items`, ML responde 200 OK, log mostra "promo ativada", mas **nada aparece no painel ML do seller**.

**Causa**: Mercado Livre tem 2 modelos completamente diferentes:

1. **Modo CRIAR** (PRICE_DISCOUNT, SELLER_CAMPAIGN): vendedor define a promo do zero (preço, prazo). ML aceita o POST mas pode silenciosamente rejeitar se categoria/seller não permite, sem erro 4xx claro.

2. **Modo ADERIR** (MARKETPLACE_CAMPAIGN, DEAL, e outros): ML oferece promoções disponíveis pro MLB. Vendedor lista, escolhe, adere. ML calcula desconto.

Empresa usa **Modo ADERIR**. Código que tenta CRIAR retorna sucesso aparente mas não produz efeito visível.

**Caso real Empresa 08/05/2026**: PROMPT_6 inicial implementou Modo CRIAR. Toast verde "Promo ativada". Painel ML vazio. Diagnóstico veio do responsável pelo exemplo notando o vazio + relembrando que Empresa normalmente "adere" a promoções, não cria.

**Fluxo correto (Modo ADERIR)**:
```
1. GET /seller-promotions/items/{mlb}
   → lista de promoções disponíveis (com promotion_id, type, deal_price, net_proceeds proposto pra cada)
2. Pra cada promoção:
   - Calcula discount_pct
   - Compara com cenário (teto_pct/net_target/tolerance)
   - Se cabe: POST /seller-promotions/promotions/{type}/items com promotion_id
   - Loga ação
3. Retorna { promos_avaliadas, promos_aderidas, detalhes }
```

**Prevenção**: antes de implementar OAuth + promo na primeira vez, **lê 1 GET de listagem** do provider pra entender o shape de dados real. ML, Stripe, Shopify — todos têm "criar" vs "aderir/processar" como conceitos diferentes.

**Template pro aluno usar com IA**:
> *"App POST pra criar promo retorna 200 OK mas nada aparece no painel do provider. Esse provider tem modo 'criar' vs 'aderir a promo existente'? Como diagnostico qual modelo ele espera pra meu caso?"*

**Update 10/05**: Modo ADERIR validado empiricamente em 4 POSTs reais (SELLER_CAMPAIGN, COUPON, DEAL, LIGHTNING — todos 201). Algoritmo final em spec secao 5 (`../2026-05-05-app-promos-ml-spec.md#5-algoritmo-de-adesao-modo-aderir--versao-final-pos-sessao-1005`, referência do material original não incluída como arquivo local). Pitfalls relacionados pos-validacao: [P-21](#-p-21--pending-na-api--aguardando-aprovacao-pode-ser-programada-por-data---caso-real-1005), [P-22](#-p-22--algoritmo-de-deal_price-invertido-min-vs-max---caso-real-1005), [P-23](#-p-23--ml-aceita-qualquer-deal_price-entre-min-e-max--escolha-de-design-e-do-app-nao-da-api---caso-real-1005), [P-24](#-p-24--multiplas-promos-podem-coexistir-como-started-no-mesmo-mlb---caso-real-1005).

---

### 🚩 P-21 — `pending` na API ≠ "aguardando aprovacao". Pode ser PROGRAMADA por data ⭐⭐ (caso real 10/05)

**Sintoma**: POST adesao em LIGHTNING retorna 201 + `status: pending`. Codigo assume "aguardando revisao humana", manda pra fila de aprovacao.

**Causa real**: na API ML, `status: pending` em LIGHTNING significa **promo programada por janela de horario futura** (ex: "14/maio das 18h às 21h"). Vira `started` automaticamente quando chega a data. NAO precisa intervencao humana.

**Como descobrimos**: responsável pelo exemplo tirou print da UI ML mostrando badge "PROGRAMADA 14/maio das 18h às 21h" + texto "Deixar de participar". Convencao da palavra `pending` (que em APIs genericas significa "aguardando algo manual") nao bate com a implementacao especifica do ML.

**Diagnostico**:
```sql
-- depois do POST, GET status atual
-- Se status = "pending" e start_date > now() → PROGRAMADA, espera a data
-- Se status = "pending" e start_date <= now() → revisar caso a caso
```

**Fix no codigo**:
```ts
function classifyPostStatus(candidate, response) {
  if (candidate.status === 'pending' && new Date(candidate.start_date) > new Date()) {
    return { state: 'scheduled', show: `Programada ${candidate.start_date}` };
  }
  if (candidate.status === 'pending') {
    return { state: 'review', show: 'Pendente de revisao ML' };
  }
  return { state: candidate.status };
}
```

**Prevencao**: pra cada status retornado pela API, **sempre validar na UI do servico** o que aquele estado significa concretamente. Convencao ≠ implementacao. UI > doc > convencao.

**Template prompt pra IA**:
```
Voce assumiu que [status retornado] significa [interpretacao A].
Eu fui na UI do [servico] e vi [evidencia: badge, texto, comportamento].
Isso muda sua hipotese? Qual e a logica nova considerando essa evidencia?
```

---

### 🚩 P-22 — Algoritmo de deal_price invertido (min vs max) ⭐⭐⭐ (caso real 10/05)

**Sintoma**: app esperava aderir promo X, item nao aderiu. UI ML continuou mostrando botao "Participar".

**Causa raiz**: algoritmo proposto inicial era `deal_price = min(suggested, teto_price)`. Operador errado. A semantica do range:
- `min_discounted_price` = MENOR preço final permitido = MAIOR desconto
- `max_discounted_price` = MAIOR preço final permitido = MENOR desconto

Pegar **min** = pegar o **maior desconto possivel**, oposto do objetivo "melhor margem dentro do teto".

**Algoritmo correto** (validado em 4 POSTs reais, todos 201):
```
teto_price = original_price * (1 - teto_pct/100)

Se min_discounted_price > teto_price → SKIP (campanha exige + desconto)

deal_price = max(suggested_discounted_price, teto_price)
deal_price = min(deal_price, max_discounted_price)  // safeguard

Interpretacao:
- Sugerido ja da MENOS desconto que teto → usa sugerido (preserva margem, ganha curadoria ML)
- Sugerido fura teto → usa teto exato (max desconto que aceito)
```

**Como descobrimos**: responsável pelo exemplo foi na UI ML, viu MAIO1 ainda como "Participar" no MLB4149113708. Trouxe evidencia: "ML sugere R$ 11 (5%), temos teto 10%. Em alguns tipos pode aceitar mais ou menos do que sugere — temos que validar."

IA recalibrou. POST com `deal_price=148.34` (sugerido = 5%, dentro do teto 10%) → 201 + `status=started`.

**Prevencao**: ao trabalhar com **range numerico** retornado por API, sempre **printar** os valores e mapear semantica (min/max ≠ sempre o que voce acha). Anote uma frase explicita: "min = preço menor = mais desconto" antes de codar.

**Template prompt pra IA**:
```
Voce escreveu deal_price = funcao (`sugerido, teto`, referência do material original não incluída como arquivo local). Eu testei na pratica
com sugerido=[X] e teto=[Y] e [resultado real]. Isso confirma sua logica
ou inverte? Re-le o range e me explica qual valor representa qual ponta.
```

---

### 🚩 P-23 — ML aceita qualquer `deal_price` entre min e max — escolha de design e do app, nao da API ⭐ (caso real 10/05)

**Sintoma**: confusao se ML aceita preço diferente do `suggested_discounted_price`.

**Realidade**: API ML aceita **qualquer** `deal_price` no intervalo `[min_discounted_price, max_discounted_price]`. O `suggested` e dica do ML pra otimizar performance (badge, destaque, ranking de campanha) — nao e piso nem teto, e referencia.

**Implicacao**: a regra de "qual deal_price aplicar" e **regra de negocio do seu app**. Estrategias:

| Estrategia | Logica | Quando usar |
|---|---|---|
| `max(suggested, teto_price)` | Aproveita ML quando ja conservador, limita quando agressivo | Default — melhor margem com curadoria |
| `teto_price` exato | Sempre usa teto | Previsibilidade total, ignora curadoria |
| `min_discounted_price` | Maior desconto possivel | Eventos de venda/queima, max alcance |
| `suggested_discounted_price` | Sempre usa o sugerido | Confia 100% no algoritmo ML |

**Como descobrimos**: responsável pelo exemplo perguntou explicitamente "ML aceita menos de 1?" (= mais desconto que o sugerido). Validacao empirica: POST com 148.34 (5% off, sugerido) e antes POST com 1799.98 (10% off, teto) — ambos 201.

**Prevencao**: documentar **qual estrategia o app usa e por que** num comentario no codigo. Caso a estrategia mude (ex: epoca de Black Friday), eh decisao de produto, nao de API.

---

### 🚩 P-24 — Multiplas promos podem coexistir como `started` no mesmo MLB ⭐ (caso real 10/05)

**Sintoma**: confusao se aderir em ABRIL "subscreve" MAIO1 (= ML escolhe so 1) ou se podem coexistir.

**Realidade**: API ML aceita **varias promos `started` simultaneas** no mesmo MLB. O algoritmo do ML decide qual exibir na vitrine (geralmente o maior desconto efetivo no momento). Ter varias = anuncio entra em todos os filtros/abas/badges relevantes.

**Combinacoes coexistentes validadas em campo (10/05)**:
- 2 SELLER_CAMPAIGN FLEXIBLE (ABRIL + MAIO1) no mesmo MLB
- DEAL + SELLER_CAMPAIGN no mesmo MLB
- ABRIL + cupom FIXED + LIGHTNING programada no mesmo MLB

**Implicacao no codigo**: app **nao precisa** "escolher a melhor" entre candidates concorrentes. Adere em todas elegiveis pelo teto. ML faz o resto.

**Excecao**: cuidado com cupons FIXED + desconto direto — comprador acumula no checkout (cupom aplica sobre preço promocional). Isso *pode* furar o teto efetivo se voce nao considerar. Pra MVP: ignora, monitora resultado real depois.

**Como descobrimos**: testes empiricos em sequencia. Apos aderir MAIO1 no MLB4184318945, tentou ABRIL no mesmo → 201 + ambas viraram started. GET subsequente confirmou as 2 simultaneamente.

**Prevencao**: nao assumir exclusividade entre promos sem validar. Cada API tem politicas diferentes de coexistencia.

---

### 🚩 P-31 — `ERROR_CREDIBILITY_DISCOUNTED_PRICE` rejeita o desconto que o proprio ML sugeriu ⭐⭐⭐ (caso real 10/05)

**Sintoma**: app POSTou adesao com `deal_price` = `suggested_discounted_price` (valor que veio do GET de candidates do proprio ML). ML retornou 400:
```
{"cause":[{"error_code":"ERROR_CREDIBILITY_DISCOUNTED_PRICE","error_message":"The discounted price is not credible."}],"error":"bad_request","message":"...","status":400}
```

**Causa**: ML tem politica anti-dumping/credibility separada do range visivel em `min/max_discounted_price`. O `suggested_discounted_price` e dica de UI, **nao garantia de aceite**. Politica considera:
- Historico de preço do item (descida muito agressiva em curto periodo)
- Item sincronizado com catalogo (ML aplica regras do catalogo pai)
- Estoque baixo (anti-baixa-de-estoque suspeita)
- Comportamento do seller (apos N falhas, ML pode endurecer mais)

**Caso real Empresa 10/05/2026**: smoke do PROMPT_6 v2 no MLB3441655001 (Misturela Panela, sincronizado com catalogo #<ID>). Cenario teto 10%, sugerido pelo ML = 10% off. POST com 1493.98 → ML rejeitou. Tentou 5% → rejeitou. ML "endureceu" o range apos as tentativas: `max_discounted_price` desceu de R$ 1576.98 (5% off) pra R$ 1385.97 (16.51% off). Item agora **so aceita >=16.51% off**.

**Fix**: nao tem fix universal — politica e opaca do ML. Tratamento certo no app:
1. Categoriza como `rejected_ml_credibility` (nao `error` cru)
2. Joga **automaticamente** pra tela `/aprovacoes` em vez de enterrar no log
3. UI mostra alerta: "ML rejeitou X% como nao credivel pra este item. Tente desconto diferente."
4. Botao "Aprovar com sugerido" fica DESABILITADO (vai falhar igual)
5. pessoa operacional do exemplo decide se aprova com desconto custom (maior) ou nega

Implementado no PROMPT_7 (`PROMPT_7_VARREDOR_FIXES.md`, no material original) Fix 2.

**Prevencao**: nao tente "evitar" credibility errors antes de tentar — e dinamico e item-especifico. **Trate como excecao categorizada**, nao como bug do app.

**Insight didatico (vai pro evento)**: APIs nao sao deterministicas. Mesmo enviando o que a propria API sugere, o servico pode rejeitar. App deve **degradar gracefully** com fluxo manual + mensagem clara, em vez de tratar como crash.

**Template prompt pra IA quando bater**:
```
ML retornou ERROR_CREDIBILITY_DISCOUNTED_PRICE em POST que enviou
deal_price = candidate.suggested_discounted_price. Mesmo valor que
ML sugeriu, mas ML rejeitou. Por favor:
1. Confirma se ja conheco isso documentado
2. Lista 3 hipoteses pra causa especifica neste item
3. Como o app deve tratar — categorizar erro + fluxo manual?
4. Templates de mensagem pro usuario explicando sem jargao
```

---

### 🚩 P-32 — Algoritmo `min(deal, maxP)` fura teto silenciosamente quando `maxP < tetoPrice` ⭐⭐⭐ (caso real 10/05)

**Sintoma**: cenario configurado com teto 10%, classifier aplicou desconto de **16.51% off** sem alerta. Furou teto silenciosamente.

**Causa**: spec original cobria so **um lado** do conflito teto-vs-campanha:
- Se `min_discounted_price > tetoPrice` (campanha exige + desconto que aceito) → SKIP/PENDING ✓
- Mas NAO trata: `max_discounted_price < tetoPrice` (campanha NAO PERMITE preco maior que teto)

Codigo existente:
```typescript
let deal = Math.max(sugP, tetoPrice);  // OK
deal = Math.min(deal, maxP);           // VIROU BUG quando maxP < tetoPrice
```

Quando `maxP < tetoPrice`, esse `min(deal, maxP)` **silenciosamente reduz o preço final pra dentro do range da campanha** — efetivamente aplicando MAIS desconto que o teto permite. App nao alerta.

**Caso real Empresa 10/05/2026**: MLB3441655001 com teto 10%. Apos varias tentativas com credibility errors, ML "endureceu" a campanha:
- `tetoPrice` (10% off) = R$ 1493.97
- `max_discounted_price` (campanha) = R$ 1385.97 (16.51% off — campanha agora exige >=16.51%)
- Algoritmo aplicou R$ 1385.97 = **16.51% off, furando teto de 10%**

**Fix** (em PROMPT_7 (`PROMPT_7_VARREDOR_FIXES.md`, no material original) Fix 1):
```typescript
// Caso ja existia: campanha exige + desconto que aceito
if (minP > tetoPrice + tolPrice) → SKIP "campanha_min_acima_teto_tol"
if (minP > tetoPrice)            → PENDING "min_acima_teto_dentro_tol"

// NOVO: campanha NAO PERMITE preço >= teto
if (maxP < tetoPrice - tolPrice) → SKIP "campanha_max_abaixo_teto_tol"
if (maxP < tetoPrice)            → PENDING "max_abaixo_teto_dentro_tol"

// AUTO: agora seguro
let deal = Math.max(sugP, tetoPrice);
deal = Math.min(deal, maxP);
deal = Math.max(deal, minP);  // NOVO: safety floor
```

**Prevencao geral**: pra qualquer algoritmo com cap (`Math.min`/`Math.max` final), pergunta:
- "E se `cap < valor_calculado`, o que acontece?"
- Se a resposta e "aplica o cap silenciosamente", trata como caso explicito antes — **com SKIP/PENDING**, nao com cap silencioso

**Insight pedagogico**: capping silencioso e um padrao **enganoso** — parece "safety guard" mas na verdade modifica o resultado fora do que voce pediu. Sempre **separe** os 2 papeis:
1. **Validacao** (decide se vai aplicar): fora do range → SKIP/PENDING explicito
2. **Safety guard** (defensivo contra bug): se chegou aqui ja deveria estar OK, cap nao e um redirecionamento

**Template prompt pra IA**:
```
Tenho funcao que calcula deal_price com:
  let deal = Math.max(sug, teto);
  deal = Math.min(deal, max_permitido);

Recebi inputs onde max_permitido < teto. Resultado: deal acabou
sendo max_permitido, furando o teto silenciosamente. 

Por favor:
1. Confirma que isso e bug (capping silencioso fura constraint)
2. Mostra como adicionar branch explicito de SKIP/PENDING
3. Lista outros lugares no meu codigo onde esse padrao
   (cap silencioso) pode ter o mesmo bug
```

---

### 🚩 P-33 — Item `under_review` retorna HTTP 400 mascarado como overload (caso real 12/05)

**Sintoma**: GET /seller-promotions/items/{MLB} retorna HTTP 400 com mensagem `"Service temporarily overloaded, please try again later"` ou similar. Script categoriza como `fail_get` transient, faz retry indefinido, sempre falha.

**Causa real**: o item esta em estado `under_review` no ML (moderacao automatica em curso). ML rejeita TODA chamada de promotions desse item ate moderacao terminar. NAO e overload, e estado bloqueante do item.

**Como diagnosticar**:
```bash
curl "https://api.mercadolibre.com/items/{MLB}?attributes=status" \
  -H "Authorization: Bearer $ML_TOKEN"
# Se retornar { "status": "under_review" } → e isso
```

**Caso real Empresa 12/05/2026**: 4 MLBs persistiram fail_get apos 2 retries (throttle 1.5s, depois 5s). Diagnostico revelou todos como `under_review`. Mensagem real do ML:
```
HTTP 400 {"message":"Item status is not allowed (under_review)","error":"bad_request","status":400}
```

Mas em alguns endpoints o ML retorna **a mensagem generica de overload** mesmo a causa sendo `under_review` — engana o retry.

**Fix** (script `aderir_maio.py` + EF `promo-activate`):

```python
def process_item(item, token):
    # PRIMEIRO: checa status do item antes de qualquer outra chamada
    code, meta = http("GET", f"{ML_BASE}/items/{mlb}?attributes=status", token)
    if code != 200:
        return {"outcome": "fail_meta", "http": code}

    if meta["status"] != "active":
        return {"outcome": f"skip_{meta['status']}", "ml_status": meta["status"]}

    # So entao GET candidates
    code, cands = http("GET", f"{ML_BASE}/seller-promotions/items/{mlb}?app_version=v2", token)
    ...
```

**Prevencao geral**: pre-flight check do status do RECURSO antes de chamar endpoints dependentes. Padrao "fail-fast com diagnostico claro" vs "retry generico com motivo opaco".

**Template prompt pra IA**:
> *"Estou recebendo HTTP 400 'Service temporarily overloaded' do endpoint X em alguns items. Retry com throttle alto nao resolve. Como descubro se a mensagem e enganadora — se na verdade o item esta em estado bloqueante (under_review, paused, closed) e nao overload real?"*

---

### 🚩 P-34 — ML decide quais items entram em cada campanha (politica interna opaca) (caso real 12/05)

**Sintoma**: items ATIVOS com estoque NAO recebem candidate de uma campanha especifica (ex: MAIO), enquanto items aparentemente identicos da mesma loja recebem. Sem padrao obvio.

**Causa**: ML aplica politica interna pra decidir elegibilidade por campanha. Fatores possiveis (nao documentados):
- Margem historica do item
- Volume de vendas recente
- Categoria do produto
- Preco vs preco-de-mercado da concorrencia
- Status de "preco bom"/"oferta destacada"

ML nao expoe a regra. Voce simplesmente nao ve a campanha como candidate no GET.

**Caso real Empresa 12/05/2026**: 29 de 1167 MLBs (2.5%) que estavam na campanha ABRIL NAO receberam MAIO. Items ativos, com estoque (2-22 unidades), titulos similares aos que receberam. ML escolheu nao incluir esses 29.

**Fix**: aceitar. Items sem candidate da campanha ficam `skip_no_maio` no log. Varredor mensal pega outras campanhas (DEAL, LIGHTNING, MARKETPLACE_CAMPAIGN) quando aparecerem.

**Prevencao**: nunca assumir 100% de cobertura quando dependencia e provider externo. Sempre logar e relatar a margem (X aderidos / Y totais) — se margem cresce sem motivo, investigar; se estavel, aceitar.

**Insight pedagogico**: a planilha do mes anterior NAO e contrato de elegibilidade do mes seguinte. Sempre rodar varredura fresca pra ver oferta real do provider.

---

### 🚩 P-42 a P-50 — Sessão 14/05/2026 (9 pitfalls em 1 dia de operacionalização)

Densidade alta de tropecos em produção. Catalogados em arquivo separado pra manter este doc com tamanho gerenciável: **`PITFALLS_2026-05-14.md` (`PITFALLS_2026-05-14.md`, no material original)**.

Sumário rápido:
- **P-42** SMART payload requer `offer_id` derivado de `ref_id` *(API & Provider)*
- **P-43** RLS `roles=authenticated` em app só-OAuth quebra anon *(RLS)*
- **P-44** `auth_tokens.user_id` NULL no OAuth callback *(OAuth)*
- **P-45** Tabela RLS-habilitada sem policy E sem GRANT pra authenticated *(RLS)*
- **P-46** Cron `pg_net` apontando pro frontend Lovable em vez da EF *(Infra)*
- **P-47** Pause/cancel UI: schedule vs job — mesma palavra, semântica diferente *(UX)*
- **P-48** PostgREST PGRST201: nested select falha com 2+ FKs entre tabelas *(Supabase JS)*
- **P-49** Supabase JS `.select()` trunca em 1000 rows silenciosamente *(Supabase JS)*
- **P-50** SELLER_COUPON_CAMPAIGN auto-propagado pelo ML — aderir é redundante *(API)*

2 reflexos novos do framework Elo derivados:
- **Reflexo 9**: Idempotência defensiva por status remoto (não inferir por tabela local)
- **Reflexo 10**: Erro silencioso da Supabase JS é o adversário invisível — sempre logar `error` antes de tratar `data`

---

## P-42 — SMART/MARKETPLACE_CAMPAIGN payload requer `offer_id` derivado de `ref_id`

**Categoria**: API & Semantica do Provider Externo

**Sintoma**: POST `/seller-promotions/items/{mlb}` com `{promotion_id, promotion_type: "SMART"}` retorna 400 `"Offer id is required"`.

**Causa**: tipos cofinanciados (SMART, presumivelmente MARKETPLACE_CAMPAIGN) exigem `offer_id` no body. Esse `offer_id` vem do campo `ref_id` do candidate (não `id`).

**Caso real Empresa 14/05**: Mesa Inox MLB2660249138 — candidate `{id:"P-MLB17605032", type:"SMART", ref_id:"CANDIDATE-MLB2660249138-<ID>"}`. Smoke:
- Payload `{promotion_id, promotion_type}` → 400 `"Offer id is required"`
- Payload `{promotion_id, promotion_type, offer_id: ref_id}` → 400 `"NOT_CANDIDATE_FOR_PROMOTION"` (estrutura aceita, MEA não estava elegível naquele instante)

Diferença das mensagens confirmou que o payload com `offer_id` é estruturalmente válido.

**Fix**: classifier de compartilhada constrói payload:
```ts
const payloadShared = { promotion_id: id, promotion_type: type };
if (candidate.ref_id) payloadShared.offer_id = candidate.ref_id;
// SEM deal_price, SEM stock, SEM offer_type (esses são pra LIGHTNING)
```

**Prevencao**: doc oficial ML não cobre payload SMART explicitamente. Padrão: testar com curl + payload mínimo → ML diz qual campo falta → adicionar incrementalmente. ML é prolixo em mensagens de validação (use isso a favor).

---

## P-43 — RLS `roles=authenticated` quando app só usa OAuth ML (sem login Supabase)

**Categoria**: RLS, Policies & Permissões

**Sintoma**: app retorna toast genérico "ML não conectado" ao tentar criar filtro/schedule, mesmo Configurações mostrando conta conectada. Backend Supabase consegue criar via curl com service_role. Frontend nem testa o backend — guard client-side aborta antes.

**Causa**: spec PROMPT_11 previa policies abertas pra `public` com gating contra `auth_tokens` (libera anon). Builder gerou policies default Supabase com `roles={authenticated}` + `qual=true`. App não tem fluxo de login Supabase Auth (só OAuth ML) → anon nunca vira authenticated → bloqueio total. Drift entre spec escrita e schema implementado.

**Caso real Empresa 14/05**: tabelas `sweep_filters` + `sweep_schedules` com policies `auth read/write` exigindo authenticated. Schedule "teste com 2 mlbs" foi criado (sessão authenticated transitória do user logado pelo Lovable), mas tela `/filtros` em browser anon recusou silenciosamente. Confundimos diagnóstico inicial achando que era `ml-account-status` que falhava.

**Fix**:
```sql
DROP POLICY "auth read sweep_filters"  ON sweep_filters;
DROP POLICY "auth write sweep_filters" ON sweep_filters;
CREATE POLICY "ml read filters"  ON sweep_filters FOR SELECT TO public
  USING (ml_user_id IN (SELECT public.ml_user_ids_known()));
CREATE POLICY "ml write filters" ON sweep_filters FOR ALL TO public
  USING (ml_user_id IN (SELECT public.ml_user_ids_known()))
  WITH CHECK (ml_user_id IN (SELECT public.ml_user_ids_known()));
```

+ função `SECURITY DEFINER` pra expor só `ml_user_id` (sem tokens) pra anon:
```sql
CREATE OR REPLACE FUNCTION public.ml_user_ids_known()
RETURNS TABLE(ml_user_id text)
LANGUAGE sql SECURITY DEFINER STABLE
SET search_path = public
AS $$ SELECT ml_user_id FROM auth_tokens $$;
GRANT EXECUTE ON FUNCTION public.ml_user_ids_known() TO anon, authenticated;
```

**Prevencao**: ao escrever policies, distingue:
- App com login Supabase Auth → `TO authenticated` + `auth.uid() = ...` ok
- App só OAuth de terceiros (Google, ML, etc.) sem Supabase Auth → policy contra tabela de tokens, role `public`
- Misto → depende, mas anon precisa pelo menos read básico

**Sempre testa via curl com anon key antes de marcar policy como pronta.** Smoke ≠ "fiz INSERT pela UI logado, funcionou".

---

## P-44 — `auth_tokens.user_id` NULL após OAuth callback

**Categoria**: OAuth & Secrets

**Sintoma**: app que adiciona login Supabase posteriormente quebra pra users que conectaram OAuth do provider antes. Hooks tipo `if (auth_tokens.user_id !== auth.uid())` falham silenciosamente.

**Causa**: `ml-oauth-callback` grava `auth_tokens` sem vincular `user_id = auth.uid()`. Quando depois é adicionado login Supabase, rows antigas ficam órfãs.

**Caso real Empresa 14/05**: responsável pelo exemplo conectou ML em 07/05 (callback gravou row com `user_id IS NULL`). Em 14/05, app ganhou login Supabase + hook que checa `auth_tokens.user_id`. Logou com `marciano.loja00@gmail.com` (auth.uid criado naquele momento), mas `auth_tokens.user_id` continuou NULL → todos os checks falhavam.

**Fix curto (manual)**:
```sql
UPDATE auth_tokens SET user_id = '<auth-uid>' WHERE ml_user_id = '<ml-id>';
```

**Fix correto (no callback)**:
```ts
// em ml-oauth-callback, após inserir token
const { data: { user } } = await sb.auth.getUser();
if (user) {
  await sb.from('auth_tokens')
    .update({ user_id: user.id })
    .eq('ml_user_id', ml_user_id);
}
```

**Prevencao**: schema com FK opcional pra `auth.users` desde dia 1, mesmo se MVP não usa Supabase Auth. Migração futura fica trivial vs cleanup de rows órfãs.

---

## P-50 — SELLER_COUPON_CAMPAIGN é auto-propagado pelo ML — aderir manualmente é redundante

**Categoria**: API & Semantica do Provider Externo

**Sintoma**: sweep adere em N cupons (SIGA, VIP, Carrinhos) em ~28 MLBs cada → Slack inunda com `🆕 aderiu em SIGA A Empresa` repetido. responsável pelo exemplo nota e pergunta: "os cupons não estão pra todos os produtos automaticamente?"

**Causa**: SELLER_COUPON_CAMPAIGN é uma campanha do vendedor (não ML), com `fixed_percentage`. Quando criada com escopo "todos os produtos", ML propaga automaticamente nos items elegíveis. Mas há **race condition de propagação** — quando cupom é novo ou item recém-criado, GET candidates retorna `status='candidate'` por algumas horas/dias até o ML "consolidar" o item.

Sweep que adere candidates faz POST → vira `started` mais rápido, mas seria `started` sozinho eventualmente. Resultado: trabalho redundante + spam Slack + ruído em log.

**Caso real Empresa 14/05**: Job das 16:38 aderiu **28× cada um dos 3 cupons** em diferentes MLBs. Quando checamos 3 MLBs `pending` (ainda não processados pelo sweep) via GET candidates às 17:30, **todos os 3 mostraram cupons como `started`** — ML já tinha propagado nas últimas 1.5h enquanto sweep rodava. Confirmação: cupons se auto-propagam.

**Fix**: classifier skipa SELLER_COUPON_CAMPAIGN sempre, logo após status check:
```ts
if (type === "SELLER_COUPON_CAMPAIGN") {
  return { branch: "skip", reason: "coupon_auto_managed_by_ml" };
}
```

**Prevencao**: ao adicionar suporte a novo tipo de promo no classifier, primeiro responda: **"o ML aplica automaticamente?"**. Se sim, skipa direto. Se não, GET candidates revelará `candidate` → POST necessário.

Pesquisa empírica até 14/05:
- `SELLER_COUPON_CAMPAIGN` → auto-propagado
- `SELLER_CAMPAIGN`, `DEAL`, `DOD`, `LIGHTNING` → vendedor adere por item
- `SMART`, `MARKETPLACE_CAMPAIGN` (cofinanciadas) → vendedor adere por item, payload requer `offer_id`
- `PRICE_DISCOUNT` → manual (PENDING quando há ID)

---

## Conhecimento de API ML consolidado nesta sessão

- **Re-POST direto numa adesão existente = 400 `OFFER_ALREADY_EXISTS`.** A API ML de promoções é create-only por `(mlb, promotion_id)`. Mudar `deal_price` de uma adesão exige **DELETE + POST**, não um POST idempotente. Validado empiricamente — detalhe completo em PROMPT_13_RESEARCH.md (`PROMPT_13_RESEARCH.md`, no material original).
- **DELETE funciona igual em adesão `pending` e `started`.** A API não protege contra remoção de campanha em curso — a governança fica 100% no classifier/UI da aplicação.
- **`net._http_response` (pg_net) como laboratório de API**: dá pra testar endpoints externos reais — GET/POST/DELETE com OAuth real — direto do Postgres via MCP, com audit-trail automático, sem subir uma linha de código. Padrão reusável pra qualquer integração.

---

## P-56 — Modo "mais agressivo" não contorna a política do provedor

**Categoria**: Integração com Provedor Externo & Escopo de Feature

**Sintoma**: expectativa de que ligar um "modo agressivo" fosse resolver sozinho as promoções presas na fila de aprovação. Não resolve — e pode piorar.

**Causa**: o modo agressivo do App Promos ML aplica o **maior desconto permitido pelo teto** (`dealPrice = tetoPrice`). As promoções na fila por `rejected_ml_credibility` estão lá porque o **próprio Mercado Livre** rejeitou o POST — política anti-dumping: o preço com desconto foi considerado "não-crível" (baixo demais). Um desconto **maior** (o teto cheio) é um preço **ainda menor** → bate na mesma política, igual ou pior. E o ML *endurece* dinamicamente o range aceito após N falhas (ver P-31).

**Caso real Empresa (18/05)**: a fila `pending_review` tinha 10 LIGHTNING + 2 DEAL em `rejected_ml_credibility` e 7 DEAL em `max_abaixo_teto_dentro_tol`. Rodar agressivo sobre os 12 de credibilidade re-POSTaria com desconto maior → rejeição garantida → de volta pra fila, mais POSTs falhos, range do ML mais rígido.

**Fix / uso correto**: o agressivo atua em dois pontos só — (a) promoção **nova** cujo range oferecido pelo ML alcança o teto → adere no teto; (b) adesão **já existente** abaixo do teto → upgrade via DELETE+POST. Ele **não força** adesão fora do range que o ML oferece (campanha com `minDeal > tetoPrice` continua `pending`) e **não contorna** rejeição de política. Ao disparar uma varredura agressiva, **excluir** os MLBs já na fila por credibilidade — re-tentar só desgasta.

**Prevenção**: **um modo "faz mais" muda a escolha *dentro* do que o provedor permite — não derruba os limites do provedor.** Antes de assumir que um modo mais forte resolve um caso travado, classifique *por que* está travado: limite do nosso lado (teto, tolerância) o agressivo estica; limite do lado do provedor (política, credibilidade, elegibilidade) ele não toca. Rejeição de política = decisão humana, ou aceitar que não vai.

---

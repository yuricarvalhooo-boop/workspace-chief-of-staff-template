---
{
  "id": "HOMER-geral-03",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "8a98e60c344836af7b2f4c5bbf7a14ffe030d1fa8f69d819061c55dbd92475a7",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 03-pensar-com-ia — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# THINKING WITH AI — Como pensar JUNTO com a IA, nao DEPOIS dela

> Modulo do evento (~15 min). Sentado entre `LINTER_AND_WARNINGS.md` e os prompts de feature.
> **Filosofia**: a IA acerta o macro e erra detalhe. Voce nao precisa programar pra recalibrar — basta trazer evidencia.

---

## A regra de ouro do "Evidence-Grounded Recalibration"

```
1. IA da uma resposta com base em conhecimento abstrato     → assume que e direcao
2. Voce valida no mundo real (UI, painel, dado, print)      → procura discrepancia
3. Achou diferenca?
   - SIM → traz a evidencia pra IA com 1 frase neutra      → IA recalibra
   - NAO → segue a resposta original                        → confianca aumenta
4. Repete o ciclo ate convergir
```

Esse fluxo e mais valioso que **decorar** como a IA pensa. Voce nao precisa entender tudo o que ela fala — voce precisa saber **conferir**.

---

## Por que isso importa

A IA generativa tem 2 modos de erro frequentes:

1. **Detalhe invertido** — a estrutura geral esta certa mas um sinal/parametro/range esta trocado (ex: confunde `min` com `max`, semantica de `pending`)
2. **Conhecimento desatualizado** — base de treino nao tem feature/API recente (ex: `MARKETPLACE_CAMPAIGN` que mudou de comportamento, `pending` que virou `programada` em UI nova)

Voce pega esses 2 erros do MESMO jeito: **trazendo evidencia do mundo real**. Voce nao precisa argumentar contra a IA, nao precisa "saber mais que ela", nao precisa codigo. Voce **mostra**.

A diferenca entre **junior vibe-coder** e **dev assistido por IA**: junior aceita a primeira resposta como verdade. Dev valida cada premissa com fonte real e traz de volta.

---

## Onde buscar evidencia (catalogo basico)

| Tipo de duvida | Onde olhar | Exemplo |
|---|---|---|
| Comportamento de tela / UX | UI do produto (admin, painel, app) | "Botao 'Participar' aparece mesmo apos POST" |
| Status / estado real | API GET (Network tab, Postman, curl) | "GET retornou status=pending, nao started" |
| Mudanca apos acao | Tela ou API antes/depois | Print pre-acao + pos-acao |
| Erro / falha | Logs (Lovable Cloud, Supabase Functions, console) | "Response body retornou 403 PolicyAgent" |
| Existencia de feature | Documentacao oficial, painel de configuracoes | "Nao acho a opcao X no DevCenter ML" |
| Comportamento esperado | Pergunta direta a quem conhece (Slack, dev, stakeholder) | "pessoa operacional do exemplo, voce ja usou esse fluxo?" |

**Heuristica**: a fonte mais valiosa e **a UI / painel real do servico**, nao a doc. Doc as vezes esta desatualizada — UI mostra o que **o sistema atualmente faz**.

---

## Padrao geral (extraindo da sessao)

```
PRINCIPIO 1 — IA acerta o macro, erra o detalhe
  Voce pega o detalhe trazendo evidencia (UI, dado, print)

PRINCIPIO 2 — Convencao ≠ implementacao real
  Mesma palavra (pending, candidate, started) muda de semantica
  por servico. UI do servico e fonte mais confiavel que doc

PRINCIPIO 3 — Sem amostra real, vai pra humano
  Especular sobre algo que voce nunca viu acontecer e como inventar
  bug futuro. Pendente_aprovacao + log + revisitar pos-N-casos

PRINCIPIO 4 — Falha de pesquisa = aprendizado
  Doc 403, endpoint 404, etc. nao sao perda — apontam pra
  caminhos alternativos (GET na conta real, perguntar a quem usa)
```

---

## Template universal de prompt

Cole no Claude / ChatGPT / chat do Lovable conforme o caso:

### Template 1 — Trazendo evidencia (re-calibracao)

```
Voce disse [resumo da resposta dela em 1 linha].

Eu fui [na UI / painel / dashboard / response real / colega que usa]
e vi [o que voce viu, em 1-2 linhas. Cola print/screenshot/JSON se tiver].

Isso muda sua resposta? Sua hipotese ainda procede?
Se nao, qual e a logica nova considerando essa evidencia?
```

### Template 2 — Pedindo pra IA pesquisar (em vez de palpitar)

```
Tem [feature/tipo/conceito] que [descreve em palavras] mas nao lembro
o nome exato. Pesquise:
- Na doc oficial de [servico]
- Na API direta (GET endpoint relevante, tente listar tipos)
- No painel do servico se tiver acesso

Me traz o nome correto + 1 linha de descricao + onde achou.
```

### Template 3 — Validando antes de aplicar

```
Antes de escrever codigo / aplicar migration / fazer deploy:
1. Resume em 3 linhas o que voce vai fazer
2. Lista 2 premissas-chave que voce ta assumindo
3. Sugere 1 forma rapida de eu validar cada premissa antes de aplicar
   (UI a olhar, request curl, query SQL)

Eu rodo a validacao, trago o resultado, aih a gente segue.
```

---

## Quando vale ir validar (e quando nao)

**Vale validar SEMPRE quando**:
- A IA falou de status / estado / range / threshold (numeros e nomes invertem facil)
- A acao e destrutiva ou irreversivel (DELETE, migration, deploy prod)
- Voce sente "isso e estranho" mesmo sem saber explicar
- Estamos no inicio do projeto e a IA ainda nao calibrou contexto
- O custo de erro > 5 min de retrabalho

**NAO precisa validar (segue na fe) quando**:
- E codigo isolado de baixa criticidade (componente UI sem dado real)
- A IA ja foi validada nesse mesmo subdominio na sessao
- O ciclo de retrabalho e barato (Lovable preview = 30 segundos pra ver se quebrou)
- Voce ja sabe a resposta e so quer confirmar / acelerar

---

## Como ensinar esse modulo no evento

```
0:00 — "A IA nao e oraculo. Ela e dev junior muito rapido.
       O que voce faz com dev junior? Confere o trabalho dele."

1:00 — "Mas eu nao sei programar." (provoca)
       "Voce nao precisa. Voce precisa saber CONFERIR.
       Conferir e ir na tela e ver se bate."

2:30 — Mostra o caso 1 (algoritmo invertido) na pratica:
       - Lê o que IA propôs
       - Abre UI ML, mostra "Participar" ainda la
       - Pergunta pra IA com 1 linha de evidencia
       - IA recalibra na hora
       - Re-testa, da certo

5:00 — Caso 2 (pending = programada):
       - Mostra print da UI ML "PROGRAMADA"
       - Aluno percebe: a UI fala mais que a doc
       - "ML aceitou e nao precisa revisao — esta agendada"

8:00 — "Agora voces. [da exercicio: olha pro app de voces, escolha
       1 coisa que a IA falou hoje, va checar na UI / dado real]
       (3 min discussao em duplas)

11:00 — Discussao aberta. Quem achou discrepancia? Quem nao achou?
        Os dois resultados sao validos.

13:00 — Regra de ouro do framework Elo:
        'Pra cada resposta da IA, escolha 1 premissa-chave e
         valide com 1 fonte real antes de aceitar.'
        Isso filtra 80% dos bugs de design.
```

---

## Escrevendo prompt que minimiza inferencia divergente

> Modulo derivado da sessao 10/05 (parte 2). Foco: a IA nao "lê e infere" do mesmo jeito que voce — ela completa lacunas com palpite. Cada lacuna no seu prompt = 1 ramo de divergencia possivel. **Quando voce constroi 2 versoes em paralelo (Cloud + Externo), as divergencias aparecem cruas**.

### Caso real — PROMPT_6 v2 nos 2 apps

responsável pelo exemplo escreveu **mesmo PROMPT_6 v2** pros 2 apps Lovable. Os 2 plans voltaram **divergentes em 5 pontos**:

| Lacuna no prompt | O que cada plan inferiu | Por que divergiu |
|---|---|---|
| "tela /aprovacoes com lista" | Cloud: + sidebar item + badge contador. Externo: so a tela. | Sidebar nao mencionada explicito |
| "GET /items/{mlb}?attributes=title,thumbnail" | Cloud: server fn fetchItemMeta + cache. Externo: chama do browser direto, "endpoint publico" | Auth nao declarada explicito (e era 403 sem token) |
| "stock = clamp(estoque_disponivel, ...)" | Cloud: implicito. Externo: explicita 1 GET available_quantity | "estoque_disponivel" sem fonte |
| "salva slack_message_ts" | Cloud: decidiu null silencioso. Externo: pergunta bloqueante | Webhook nao retorna ts — trade-off escondido |
| "previne double-approve race" | Cloud: explicita pattern. Externo: vago | Pattern SQL nao especificado |

**Causa raiz**: o prompt confiava que builder ia ler spec linkada + extrapolar. Builder leu, mas extrapolou cada um pra um lado. **Inferencia ≠ instrucao**.

### 5 heuristicas pra escrever prompt menos lacunoso

#### 1. Contrato explicito por chamada externa

Em vez de "GET /items/{mlb}":

```
GET https://api.mercadolibre.com/items/{mlb}?attributes=title,thumbnail
  Auth: Bearer (precisa access_token via getMLAccessToken)
  Response: { title: string, thumbnail: string }
  Erros: 403 sem token, 404 se MLB nao existe na conta
```

Cada vez que o builder pode "achar que sabe" → escreve.

#### 2. UI atomica em bullets, nao prosa

Em vez de "tela /aprovacoes com lista":

```
Rota /aprovacoes (layout autenticado):
- Header: "Aprovacoes pendentes" + count
- Lista paginada 10/pagina, ordem created_at DESC
- Por card: thumb (96px) + titulo (1 linha truncada) + badge tipo (cor por type)
  + razao + tabela 4col [Range / Sugerido / Teto / Delta]
- 3 botoes: [Aprovar sugerido] (verde primary) [Aprovar com X% custom] (azul, abre modal)
  [Negar] (vermelho secundario)
- Estado vazio: "Nada pendente" + ilustracao
- Sidebar: item "Aprovacoes" + badge count (refetch 30s)
```

Builder nao precisa decidir nada visual sozinho.

#### 3. Rastreabilidade de cada variavel

Por cada `X = ...` no fluxo, anote **fonte**:

```
stock_disponivel = response.available_quantity
  ← vem de GET /items/{mlb}?attributes=available_quantity
  ← chama 1x no inicio do varredor por MLB, reusa pros candidates LIGHTNING

deal_price = max(suggested_p, teto_price)
  ← suggested_p = candidate.suggested_discounted_price
  ← teto_price = candidate.original_price * (1 - cenario.teto_pct/100)
```

Builder nao adivinha, copia.

#### 4. Trade-offs resolvidos com nota explicita

Em vez de "salva slack_message_ts":

```
slack_message_ts: tipo text, NULL no MVP.
  Razao: usar incoming webhook (nao retorna ts). Edit pos-decisao
  fica TODO no PROMPT seguinte. Se virar dor, migra pra bot token
  (chat.postMessage retorna ts) — adiciona 30min setup.
```

Trade-off declarado = builder nao precisa perguntar.

#### 5. Smoke test concreto, nao "deveria funcionar"

Critério ruim:
> "Botao Varrer funciona"

Critério bom:
> "Click Varrer em MLB com >=1 candidate FLEXIBLE elegivel pelo teto → POST registra HTTP 201 → toast aparece em <3s mostrando 'Aderiu N · M pendentes · K skip' → linha em promo_actions_log com `status_apos_post=started` e `deal_price=<calculado>`"

Builder testa contra criterio especifico, nao contra ideia.

### Rubrica de revisao expandida (5 → 9 perguntas)

A "5 perguntas" classica cobre **seguranca**. Nao cobre **completude funcional** ou **consistencia entre paralelos**. Adiciona 4:

| # | Pergunta | Pega o que |
|---|---|---|
| 1 | **SECRETS** | Algum valor pode chegar null/undefined no caminho real? |
| 2 | **ROTATION** | Tokens/credenciais vao expirar — handler trata refresh? |
| 3 | **EXPOSURE** | Algum secret vaza pro client? Logs/responses contem dado sensivel? |
| 4 | **PROTECTION** | Auth correta em cada endpoint? Validacao server-side? |
| 5 | **SCHEMA** | Migration aditiva, sem RLS/grant/trigger acidentais? |
| **6** | **CONSISTENCY** | Os 2 apps Cloud+Externo entregariam UI/UX e fluxo identicos? Lista divergencias e justifica |
| **7** | **CONTRACTS** | Cada chamada externa (ML API, Slack, Supabase) tem auth + request + response shape declarado no plan? |
| **8** | **EVIDENCE** | Cada premissa tecnica nao-trivial foi validada empiricamente (curl, GET na UI, doc oficial)? Lista quais foram especulacao |
| **9** | **UI×SCHEMA** | A UI consulta exatamente as colunas que a migration vai criar? Diff entre nomes propostos no plano vs nomes que vao sair na migration — listar e padronizar antes de codar tela |

### Heuristica meta

Se voce esta construindo em paralelo (Cloud + Externo, ou builder1 + builder2): **veja a divergencia entre os plans como diagnostico do prompt**, nao como erro do builder. Onde divergiram = onde seu prompt deixou inferencia possivel. Refina 1 vez, cola de novo, plans convergem.

Se voce esta sozinho (1 builder so), **mentalize "como o builder vai inferir cada parte ambigua"** antes de aplicar. Toda ambiguidade vira bug em runtime.

### Como aplicar isso no evento

```
0:00 — "Quem aqui ja deu prompt pra IA, voltou ruim, e
       voce achou que a IA era burra?"
       (todos riem)

1:00 — "A IA nao e burra. Ela completa lacunas com palpite.
       Cada lacuna sua = 1 caminho que ela escolheu sem te perguntar."

2:00 — Mostra os 5 pontos divergentes do PROMPT_6 hoje
       (sidebar / endpoint publico / estoque / slack ts / race)
       — 1 prompt, 2 plans diferentes, mesma spec

5:00 — "Cada divergencia e 1 lacuna no prompt. Vamos consertar
       1 a 1 — 5 heuristicas (1 slide por heuristica)"

12:00 — "Agora voces. [exercicio: pega 1 prompt que voces
        deram hoje, marca todas as palavras que a IA precisaria
        inferir pra completar. Ranqueia: qual lacuna e mais perigosa?]"
        (5 min duplas)

17:00 — Discussao + introducao da rubrica de 8 perguntas
        (5 originais + CONSISTENCY + CONTRACTS + EVIDENCE)

20:00 — Regra de ouro:
        'Construir em paralelo expoe lacunas. Se voce so tem 1 builder,
         pensa como se tivesse 2 — onde divergiriam?'
```

---

## Conexao com framework Elo

Esse modulo cobre **a Fase 02 (Construir) toda** — em todo prompt de feature, voce vai ter chance de fazer evidence-grounded recalibration. Tambem reaparece na **Fase 03 (Evoluir)**, quando voce tem usuarios reais e os bugs vem da diferenca entre **o que a IA assumiu** e **o que o sistema real faz**.

Combinado com `LINTER_AND_WARNINGS.md`:
- Linter = **codigo** te avisa de bug
- Thinking with AI = **realidade** te avisa de premissa errada

Os dois sao validacao. Linter e automatico. Thinking with AI e voluntario — voce escolhe quando trazer evidencia. Nesse modulo voce aprende **quando** e **como**.

---

## Apos este modulo

1. ✅ Aluno sabe identificar premissas-chave em uma resposta de IA
2. ✅ Aluno sabe escolher fonte de evidencia (UI > doc, dado real > convencao)
3. ✅ Aluno sabe trazer evidencia em 1-2 linhas neutras (sem argumentar)
4. ✅ Aluno entende que falha de pesquisa nao e perda — vira caminho novo
5. → Pode prosseguir pra construir features sabendo que **cada decisao da IA passa por checagem leve antes de virar codigo**

---
{
  "id": "HOMER-geral-01",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "bba61b35b6daf83e94fc6f1cc7be0c423be4643e79b3d3dd5e9e285c2f4cdb3d",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 01-framework-4-fases — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# Elo — Framework Vibe Code em 4 Fases (DOCZAO)

**Data**: 2026-05-05
**Origem**: brainstorming responsável pelo exemplo sobre App Promos ML que virou framework didatico do evento
**Destino**: base da apresentacao na Imersao Elo 27-28/05/2026
**Caso real**: este framework e validado ao vivo construindo o App Promos ML em paralelo

---

## Por que esse framework existe

Vibe coding popular hoje vira "abre Lovable, descreve a ideia, esta pronto". E parcialmente verdade — o builder constroi. Mas o resultado e tao bom quanto **o que veio antes**.

A maioria do conteudo de vibe code do mercado pula direto pra **Fase 02 (Construir)**. O Elo ensina que **quem ganha tempo na 00 e na 01 perde menos tempo na 02 e na 03**.

Esse doc e a base ensinavel. Aplicado ao vivo num caso real (App Promos ML) pra que a teoria nao fique abstrata.

---

## Estrutura: 4 Fases

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  00 IDENTIFICAR  │→ │  01 PENSAR       │→ │  02 CONSTRUIR    │→ │  03 EVOLUIR      │
│  (1-2 dias)      │  │  (1-2 dias)      │  │  (1 dia)         │  │  (semanas)       │
│  mapear, deletar │  │  spec, validar   │  │  builder, MVP    │  │  polir, integrar │
└──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘
```

| Fase | Pergunta-chave | Output | Ferramentas tipicas |
|---|---|---|---|
| **00 Identificar** | "Esse processo deveria existir?" | Lista priorizada (gargalo × impacto × ROI) | Notion/planilha, entrevista, Loom, chat AI |
| **01 Pensar** | "Da pra construir? Como?" | spec.md + API validada + decisoes claras | Claude.ai, ChatGPT, Claude Code, WebSearch, MCPs |
| **02 Construir** | "Qual builder pro caminho mais curto?" | App deployado + voce usa | Lovable, Replit, v0, Bolt, Base44, Element |
| **03 Evoluir** | "Como melhorar e integrar?" | Polish + integracoes + roadmap proximo | Claude Code, Cursor, GitHub, Vercel, Supabase |

---

## Refs de Autoridade

A Fase 00 nao e ideia nossa. E base de 100 anos de pensamento sobre eficiencia industrial:

### Bill Gates (1996, "The Road Ahead")
> "The first rule of any technology used in a business is that automation applied to an efficient operation will magnify the efficiency. The second is that automation applied to an **inefficient operation will magnify the inefficiency**."

### Elon Musk (Isaacson 2023) — algoritmo de 5 passos
1. **Question** every requirement (atrele nome a quem pediu)
2. **Delete** parts/processes (a maioria deveria sair)
3. Simplify and optimize
4. Accelerate
5. **Automate** ULTIMO

> Musk admite: _"I mistakenly spent a lot of time accelerating processes that I later realized should have been deleted."_

### Toyota / Sakichi Toyoda (~1924, jidoka)
> "First try doing it thoroughly by hand, implement kaizen, eliminate waste — only then replace operations with machines."

3 angulos diferentes (visionario tech, builder atual, tradicao industrial) dizendo a mesma coisa. **Delete antes de Automate.**

---

## Princípios cross-fase

1. **"Use o que voce ja tem, sabendo o que ela limita"** — nao assine 5 servicos pra fazer 1 coisa
2. **"Nao existe a ferramenta perfeita, existe a que testa e funciona pro teu caso"** — antes de comprometer, teste
3. **"Reuse BACKEND, construa FRONTEND novo"** — atalho real quando voce ja tem stack
4. **"MVP interno aceita vendor lock"** — portabilidade vem depois quando provar
5. **"Webhook + poll fallback"** — seja paranoico com integracoes externas
6. **"Default: mantem o que estava"** — copia comportamento humano seguro antes de inovar

---

## Estrutura Didatica: 2 Trilhas Paralelas

Cada fase tem **dois lados** sendo ensinados em paralelo:

| Trilha | Quem | Tipo | Output |
|---|---|---|---|
| **A — Caso Real** | responsável pelo exemplo/Empresa com stack existente | Demonstracao | Spec do app + app rodando |
| **B — Mentorado** | Publico do evento sem stack | Playbook | Templates + checklists agnosticos |

**Metodo de execucao:** Trilha A roda primeiro (com tropecos reais). Trilha B nasce **destilada** dos aprendizados — versao polida fundamentada nos erros da A. Voce ensina mostrando "olha onde eu errei, e aqui esta o jeito otimizado".

---

## FASE 00 — IDENTIFICAR

### Objetivo
Antes de mexer com builder, descobrir se o processo precisa existir, simplificar, ou ser eliminado.

### Conexao com Will
Will fala antes desse bloco sobre **escolha de ferramentas no contexto certo**. Esse bloco pega o gancho dele e aplica em casos concretos: "antes da ferramenta, o problema. E nem todo problema deveria virar app."

### Trilha B (Mentorado) — Template

```markdown
# [Nome do processo] — Diagnostico Fase 00

## 1. Como e hoje
- Quem executa: ___
- Frequencia: ___ vezes/semana ou /mes
- Tempo gasto cada vez: ___
- Custo total/mes: tempo × valor-hora
- Onde quebra (gargalo): ___

## 2. Question — por que existe?
- Quem pediu originalmente: ___
- Que problema resolvia: ___
- Esse problema ainda existe? [ ] sim [ ] nao
- A regra ainda vale? [ ] sim [ ] nao [ ] parcial

## 3. Delete — da pra eliminar?
[ ] Sim, vou eliminar | motivo: ___
[ ] Nao da | motivo: ___ → vai pra (4)

## 4. Simplify — da pra reduzir antes de automatizar?
- O que pode sair do processo: ___
- Versao minima viavel: ___

## 5. Decisao
[ ] Eliminar (proceed: comunicar stakeholders)
[ ] Simplificar primeiro, automatizar depois
[ ] Automatizar ja → vai pra Fase 01
[ ] Adiar → mover pra backlog

## 6. ROI estimado (se automatizar)
- Tempo economizado/mes: ___ h
- Risco se nao fizer: ___
- Esforco estimado: ___ dias dev
- Payback: ___ semanas
```

**Ferramentas pra cada passo:**
- Mapear: planilha + entrevista + Loom (gravar quem executa — super didatico)
- Question: chat com Claude/GPT em modo "5 whys"
- Delete/Simplify: Claude propoe 3 versoes do processo (atual / simplificado / inexistente)
- ROI: planilha ou markdown direto

---

## FASE 01 — PENSAR

### Objetivo
Pre-builder. Reduz risco de jogar prompt vazio em ferramenta, gerar codigo errado, e descobrir que API nao existe depois de 2 dias construindo.

### Sub-etapas
- **1.0** — Escolher ferramenta de "pensar" (Claude/GPT/Claude Code/Perplexity/Manus)
- **1.1** — Validar tecnico (API existe? Limites? Webhooks?)
- **1.2** — Reuso vs standalone (o que aproveitar do que ja tenho?)
- **1.3** — Form factor + escopo MVP (web/CLI? Quantas paginas? Crons?)
- **1.4** — Data model + regras (decision tree, schema, validacoes)
- **1.5** — Spec final + PROMPT_BUILDER pronto pra Fase 02

### Sub-etapa 1.0 — Escolha de ferramenta

| Ferramenta | Forte pra | Limita | Custo |
|---|---|---|---|
| **ChatGPT (Plus)** | brainstorm aberto, voice, raciocinio | varia por modelo | US$ 20-30/mes |
| **Claude.ai (Pro/Max)** | escrita longa, prompts complexos | menos integracao tool | US$ 20-200/mes |
| **Claude Code (CLI)** | pesquisar codigo proprio, terminal, MCPs | curva pra nao-dev | gratis ate limite |
| **Perplexity** | pesquisa com citacoes | menos profundo em raciocinio | US$ 20/mes |
| **Manus** | agente autonomo (faz por voce) | menos transparente, mais caro | varia |
| **NotebookLM** | estudar refs (PDFs, links) | so consome o que voce der | gratis |

**Regra de responsável pelo exemplo**: pra brainstorm escolha **uma** entre Claude.ai e ChatGPT. Pra pesquisar codigo proprio, **Claude Code**. Pra estudar refs, **NotebookLM**. Nao precisa dos 5.

### Trilha B (Mentorado) — Templates

#### 1.1 Validacao tecnica (prompt template)

```
Vou construir [APP/IDEIA EM 2 LINHAS].
Pesquise e me retorne sobre a API de [SISTEMA]:

1. Operacoes core (listar X, criar Y, atualizar Z)
2. Endpoints que cobrem cada (path completo + metodo HTTP)
3. Versao atual e diferenca v1 vs v2
4. Tipos/objetos suportados
5. Rate limit (req/min, scope)
6. Autenticacao (OAuth? API key? Token vence?)
7. Webhooks/notificacoes (eventos? como subscrever?)
8. Gotchas (limites, deletes proibidos, parametros obrigatorios escondidos)
9. Paginacao (default size, max, mecanismo)
10. Documentacao oficial (links exatos)
11. SDKs/clients da comunidade (GitHub)

Pra cada item, cite a fonte. Se nao encontrou, diga "nao encontrei" — nao invente.

Apos: "Da pra construir o que eu quero?" Sim/nao/parcial + por que.
```

#### 1.2 Decisao reuso vs standalone (checklist)

```markdown
## Reusar ou comecar do zero?

Marque o que ja tem PRONTO:
- [ ] Autenticacao funcionando em outro app
- [ ] Banco de dados com schema relacionavel
- [ ] Conta paga em servico que o novo app precisa
- [ ] Codigo/utilitarios que poupariam tempo
- [ ] Dados (catalogo, usuarios, integracao)

Se marcou 3+: provavelmente vale **reuso seletivo**.
Se marcou 0-2: provavelmente vale **standalone**.

## Heuristica matadora:
> Reuse o BACKEND (banco, auth, integracoes), construa o FRONTEND novo.
> Quando provar que funciona, junta tudo num codebase.
```

---

## FASE 02 — CONSTRUIR

### Objetivo
Sair do spec pro app rodando. Escolher builder certo (ou multi-builder) e medir resultado.

### Plano de teste de builder (do nosso caso)

| Plano | Builder | Acao | Decisao |
|---|---|---|---|
| **A** | Lovable Cloud | Cria projeto novo, tenta conectar Supabase externo | Funciona? Plano A |
| **B** | Replit / v0 / Bolt / Base44 | Se Lovable nao permitir, testa cada um por ~20min | Algum funciona? Plano B nele |
| **C** | Lovable Cloud isolado | Se nenhum permite, aceita lock e constroi em Lovable Cloud com mindset "interno temporario". Migra na Fase 03 | Documenta como case do evento |

**Material didatico do evento**: documentar com prints cada tentativa.

### Trilha B (Mentorado) — Como escolher builder

```markdown
## Pre-flight check do builder

Antes de comprometer, gaste 20 minutos:
1. Cria projeto no builder
2. Tenta o que e CRITICO pro app (auth? conectar banco? rodar EF?)
3. Se trava, vai pro proximo
4. Se passa, segue construindo

## Heuristicas:
- Familiaridade vence beleza (a ferramenta que voce ja domina e mais rapida)
- UI polida = Lovable. Iteracao alem do MVP = Replit. Componente isolado = v0
- Nao subestime "fazer o mesmo prompt em 2 builders ao vivo" — vira reel forte
- Builder deve te entregar o codigo (GitHub), senao voce esta preso
```

---

## FASE 03 — EVOLUIR

### Objetivo
Sair do builder pra dev real. Polir, integrar, expandir. Onde Claude Code brilha.

### Trilha B (Mentorado) — Heuristicas
1. **Sair do builder quando**: builder limita uma feature critica, voce quer integrar com codigo de fora, custo do builder fica alto, time precisa entrar
2. **Ferramentas tipicas**: Claude Code (CLI), Cursor, GitHub, Vercel, Supabase CLI
3. **Migracao Lovable → Vercel**: clona repo do GitHub, faz deploy no Vercel, conecta variaveis env
4. **Quando nao migrar**: app interno, validacao curta, sem usuarios externos

---

## Insights-Chave (consolidados — viraram aula/reels)

### Da Fase 00
1. **"Replicar manual = 80% do tempo"** — Musk: delete antes de automatizar
2. **"Custo nao e R$ 119, e dinheiro deixado na mesa"** — Bill Gates (1996)
3. **80% das vendas Empresa ML vem de promo** — base do ROI
4. **"Hoje so renovamos as mesmas; nao entramos nas novas"** — a dor escondida e MAIOR que a dor visivel

### Da Fase 01
5. **Promo compartilhada otimiza margem** — Empresa 8% + ML 3% = 11% cliente, 2% margem extra
6. **3 branches > binario**: zona-cinza com tolerance e onde mora a inteligencia humana
7. **net_proceeds da ML simplifica margem** — nao precisa calcular liquido
8. **Webhook + poll fallback** = robustez (webhook nunca e 100%)
9. **Default "mantem o que estava"** = comportamento humano replicado com seguranca

### Da Fase 02
10. **MVP interno aceita vendor lock** — portabilidade vem depois quando provar
11. **Reuse BACKEND, construa FRONTEND novo** — atalho real
12. **"Nao existe a ferramenta perfeita"** — testa rapido, escolhe a que serve

### Cross-fase
13. **Use o que ja tem, sabendo os limites** — nao assine 5 servicos pra fazer 1 coisa
14. **Quem ganha tempo na 00 e 01 perde menos tempo na 02 e 03** — mensagem central do Elo

---

## Reactive Learning Aplicado — Catalogo de Tropecos Reais

Vibe coding nao e magico — em algum momento o aluno vai bater na trava. **A arte do
Elo nao e ensinar a teoria pra prevenir tudo (impossivel), e ensinar o reflexo certo
pra superar quando bater**.

Durante o build do App Promos ML (Fase 02 - 07-08/05/2026), vivemos 16 tropecos
reais — desde "Lovable propos lock-down RLS prematuro" ate "ML rejeitou OAuth por
2 espacos invisiveis num secret". Cada um virou material didatico estruturado em
`lovable-prompts/PITFALLS.md` (`PITFALLS.md`, no material original).

**Estrutura padrao de cada pitfall** documentado:
1. **Sintoma** — o que o aluno ve
2. **Causa raiz** — o que de fato esta acontecendo (geralmente diferente do sintoma)
3. **Como diagnosticar** — passos pra confirmar
4. **Fix** — como resolver
5. **Prevencao** — como evitar repetir
6. **Template de prompt pra IA** — pra aluno usar com ChatGPT/Claude/Gemini quando bater

### Os 4 reflexos que esse catalogo treina

#### 1. **"O builder propos algo que voce nao pediu? Pergunte pra IA antes de aceitar."**

Caso real: apos rodar Design System, builder propos lock-down de RLS multi-tenant.
Aluno "secure by default" aceita → cenarios somem da UI → MVP quebra.

**Reflexo**: Plan novo do builder = passa pela rubrica de 5 perguntas antes:
SECRETS / ROTATION / EXPOSURE / PROTECTION / SCHEMA. Se algum gera bug em runtime,
recusa. Se nao, aprova.

#### 2. **"Preview pode mentir. Publica pra ver a verdade."**

Caso real: warning de externalizacao do `@supabase/supabase-js` parecia inofensivo
em dev/preview. No build de producao virou erro fatal — `exit status 1`. **Build
de prod e mais rigoroso**.

**Reflexo**: depois do MVP rodar em preview, **sempre tentar publish antes de
declarar vitoria**. Se quebrar, anota como pitfall e fixa.

#### 3. **"Quando o erro e vago, olha a request real."**

Caso real: ML rejeitou OAuth com mensagem vaga "aplicativo nao esta pronto".
Codigo OK, app em producao, redirect cadastrado. **Causa**: `ML_REDIRECT_URI`
tinha 2 espacos invisiveis no fim. URL real no browser tinha `+++` (2 espacos
codificados). Visivel apenas decodificando os parametros.

**Reflexo**: erro vago do provedor externo → decodifica URL, olha cada param
com olho de lupa. Whitespace, encoding, sintaxe — frequentemente sao pequenos
detalhes invisiveis a olho nu.

#### 4. **"A IA acerta o macro, erra o detalhe. Voce traz evidencia, ela recalibra."**

Caso real: na sessao 10/05, definindo o algoritmo de adesao a promo ML, a IA
propos `deal_price = min(suggested, teto)` — estrutura certa, operador errado.
responsável pelo exemplo foi na UI ML, viu que o item nao tinha aderido, voltou: "ML sugere 11,
temos teto 10, ele aceita menos? em alguns tipos pode aceitar mais ou menos".
IA recalibrou pra `max(suggested, teto)` — preserva margem quando sugerido ja
da menos desconto. POST com novo deal_price → 201 + status=started, validado.

Outros 2 casos da mesma sessao:
- LIGHTNING ficou `pending` apos POST. IA achou "aguardando aprovacao". responsável pelo exemplo
  tirou print da UI mostrando badge "PROGRAMADA 14/maio das 18-21h". IA
  recalibrou: `pending` = data futura, vira `started` na hora.
- "Tem promo cofinanciada com Meli mas nao lembro o nome." IA pesquisou:
  doc oficial 403, endpoint inventado 404, ate achar via `GET /seller-promotions/users/{id}`.
  Identificou `MARKETPLACE_CAMPAIGN`. **Empresa nao tem ativa** → decisao consciente:
  manda pra tela `/aprovacoes` ate ter amostra real.

**Reflexo**: a IA tem 2 modos de erro frequentes:
- (a) **detalhe invertido** (min vs max, semantica de status)
- (b) **conhecimento desatualizado** (API mudou apos treino)

Voce pega os dois do mesmo jeito: traz evidencia em 1-2 linhas neutras
(print, response real, dado da UI). Voce nao precisa programar nem argumentar
contra a IA — voce **mostra**.

Documentado em `lovable-prompts/THINKING_WITH_AI.md` (`THINKING_WITH_AI.md`, no material original)
com 3 casos reais detalhados, principios, templates de prompt e quando vale validar.

### Resultado consolidado MAIO

- 1167 produtos planilha → 1120 aderidos (95.9%)
- 29 sem oferta MAIO genuina (politica ML)
- 4 under_review (aguardando moderacao ML)
- 0 erros nao-tratados

Stack do esforco: script Python local + Edge Function bulk-log-insert do
Supabase Externo + view promo_sweeps_view + tela /log do app Lovable
(Cloud + Externo).

**Material didatico**: a sessao 12/05 inteira virou exemplo do framework
4 fases agindo em escala — Fase 00 ja feita (planilha ABRIL diagnostico),
Fase 01 ja feita (algoritmo validado smoke 10-11/05), Fase 02 ja feita
(2 apps Lovable estaveis), **e a Fase 03 comecou aqui**: evolucao do app
pra autonomizar pessoa operacional do exemplo via PROMPT_8 (log), PROMPT_9 (upload UI),
proximo PROMPT_10 (batch sweep + agendamento).

### Modulos de integracao (referenciados pelos prompts)
- `lovable-prompts/SLACK_WEBHOOK_SETUP.md` — webhook Slack passo-a-passo (~5min, pre-req do PROMPT_6)
- `lovable-prompts/THINKING_WITH_AI.md` — metacognicao Reactive Learning (Fase 02)
- `lovable-prompts/LINTER_AND_WARNINGS.md` — leitura de warnings (Fase 02-03)

### Notas Obsidian
- `Servicos/Elo.md` — visao geral do servico
- `Servicos/Elo - Imersao.md` — detalhe da imersao 27-28/05
- `Servicos/Elo - Chronos Lead Engine.md` — pilar 2
- `Projetos/App Promos ML.md` — pagina-mae do caso (a criar)

### Referencias citadas
- Bill Gates, "The Road Ahead" (1996)
- Walter Isaacson, "Elon Musk" (2023) — capitulo sobre Tesla algorithm
- Toyota Production System / jidoka (Sakichi Toyoda, ~1924)

---

## Roadmap pra usar esse doc no evento

1. **Slide-deck-friendly**: cada secao "FASE NN" pode virar 3-5 slides
2. **Demo ao vivo**: Trilha A do Caso Empresa como case real ao vivo (ou pre-gravado se ficar pronto)
3. **Hands-on do publico**: Trilha B nos templates — cada participante preenche pra propria ideia
4. **Reels prep**: insights-chave numerados (1-14) sao base de 14 reels potenciais
5. **Conexao com Will**: bloco do Will antes da Fase 00 daria o "como escolher ferramentas"; Fase 00 entra como "antes de escolher ferramentas, tenha o problema certo"

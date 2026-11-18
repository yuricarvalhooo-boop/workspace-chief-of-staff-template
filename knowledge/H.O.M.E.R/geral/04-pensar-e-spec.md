---
{
  "id": "HOMER-geral-04",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "e3044a327c61fbd5adde45e6537b10bf526be9145c605ef6db75b86ef2a7cfde",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 04-pensar-e-spec — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# KB Fase 01 — Pensar: Escrever a spec antes de construir

> Este documento consolida o metodo Spec First e os templates de prompt para a Fase 01 (Pensar) do framework Elo.
> Conteudo original: `SPEC_FIRST.md` + `templates/SPEC_FROM_AUDIO.md` + `templates/SPEC_FROM_QUESTIONS.md`.

---

# SPEC FIRST — Definir o app antes de construir

> Este e o documento mais importante do material didatico.
> Pular SPEC = construir 3 telas e perceber que precisa refatorar metade.
> Modulo da Fase 01 (Pensar) do framework Elo, sentado entre PRE_FLIGHT e PROMPT_1.

---

## Por que spec antes de prompts (didatico pro evento)

Imagine pedir pra um pedreiro construir uma casa sem planta. Voce diz "constroi uma casa" e ele comeca a fazer parede. No 3o dia voce ve a janela no lugar errado, descobre que nao tem garagem, e tem que botar tudo abaixo.

Vibe code com IA e a mesma coisa. Builder e o pedreiro mais rapido do mundo — vai construir o que voce pedir, **inclusive coisa errada**. Spec e a planta. Sem ela, o que custaria 1 prompt vira 5.

**A regra de ouro do framework Elo**: **quem ganha tempo em "Identificar" e "Pensar" perde menos tempo em "Construir" e "Evoluir"**. Spec e o output da Fase 01 Pensar.

### Sintomas de que voce pulou a spec
- Apos 5 prompts, voce nao sabe se "ja terminou"
- Builder constroi feature errada, voce desfaz
- Voce muda de ideia toda hora — builder se perde
- Outras pessoas pedem ajustes que voce nunca pensou
- Apos lancar, voce descobre que esqueceu de algo critico

### O que spec resolve
- **Escopo**: voce sabe quando e quando nao acabou
- **Direcao**: builder constroi pra um destino claro
- **Comunicacao**: voce explica pra socio/cliente em 5 minutos
- **Mudanca**: quando algo muda, voce sabe o que isso quebra

---

## O que tem que estar na spec (minima)

Nao precisa ser longa. Precisa ser **clara**. Em 1 pagina ja serve pra MVP. Cobre:

| Secao | Pergunta que responde |
|---|---|
| **1. Visao em 1 linha** | "O app faz X pra Y conseguir Z" |
| **2. Personas** | Quem usa? Quantos sao? O que sabem? |
| **3. Casos de uso** | O que cada persona faz no app, em ordem |
| **4. Escopo MVP** | O que NAO faz nessa primeira versao |
| **5. Entidades de dados** | Que coisas o app guarda? Como se relacionam? |
| **6. Fluxos principais** | Do login ate o objetivo: 3-5 passos |
| **7. Integracoes** | Fala com fora? (email, Slack, APIs, planilha) |
| **8. Look & feel** | Vibe (3-5 referencias visuais ou frase descritiva) |
| **9. Sucesso** | Como vou saber que o app funciona? |

**Exemplo concreto (App Promos ML)**: ver `2026-05-05-app-promos-ml-spec.md` — 13 secoes, mais detalhado que o minimo, mas a estrutura essencial e a mesma.

---

## 3 caminhos pra criar a spec com IA

Escolha conforme seu jeito de pensar:

### Caminho 1 — AUDIO + IA estrutura

Voce abre o gravador do celular e fala por 5-10 minutos, livremente, sobre o app que quer construir. Cola a transcricao numa IA (Claude, ChatGPT) e pede pra ela estruturar.

**Quando funciona melhor**: voce e mais articulado falando que escrevendo, ou ja tem a ideia "rolando na cabeca" mas nao consegue por num documento.

**Como gravar bem**:
- Imagine que esta explicando pra um amigo dev que vai construir pra voce
- Fale: o problema, quem sofre, o que voce quer que mude, exemplos concretos
- 10 minutos e suficiente. Mais que 15 fica confuso

**Template de prompt** (cole na IA junto com a transcricao):

```
Vou colar a transcricao de um audio onde eu falo sobre um app que quero
construir. Por favor:

1. Le o audio inteiro pra entender o contexto
2. Estrutura uma spec funcional minima cobrindo:
   - Visao em 1 linha
   - Personas (quem usa)
   - 5-8 casos de uso principais
   - Escopo MVP (o que NAO faz nessa versao)
   - Entidades de dados macro (3-6 entidades + relacoes)
   - 2-3 fluxos principais (do login ao objetivo)
   - Integracoes externas
   - Look & feel (palavras descritivas)
   - Criterios de sucesso

3. Onde a transcricao for ambigua, faca pergunta especifica em vez de
   inventar. Liste perguntas no fim do documento como "Open Questions"

4. Use linguagem natural, evita jargao tecnico desnecessario

5. Salve como `SPEC.md`

Transcricao do audio:
[COLA AQUI A TRANSCRICAO]
```

---

### Caminho 2 — PERGUNTAS GUIADAS (Socratic)

A IA te faz perguntas, voce responde, ela monta a spec a partir das respostas.

**Quando funciona melhor**: voce nao sabe por onde comecar, ou quer ter certeza de que nao esqueceu nada.

**Template pra colar na IA** (Claude/ChatGPT/Gemini):

```
Voce vai me ajudar a criar a spec de um app que quero construir. Eu sei
sobre o problema, mas nao sei estruturar uma spec. Faca o seguinte:

1. Me faz UMA pergunta de cada vez (nao mande lista)
2. Apos minha resposta, faz a proxima
3. Cubra estas areas, na ordem:
   - Que problema voce ta resolvendo? Pra quem?
   - Como esse problema e resolvido hoje (sem o app)?
   - Quem vai usar o app? Quantas pessoas? O que sabem?
   - Quais sao os 3-5 momentos-chave no app (do login ao objetivo)?
   - Que dados o app guarda? Que entidades existem?
   - O app fala com servicos de fora? (email, Slack, APIs, planilhas)
   - Como vao acessar? Mobile, web, ambos?
   - Como o app vai parecer? Tem referencia visual?
   - Quando voce vai saber que o app funcionou? Que metrica importa?
   - O que NAO faz parte dessa primeira versao?

4. Apos eu responder tudo, gere o documento `SPEC.md` com a estrutura:
   - Visao em 1 linha
   - Personas
   - Casos de uso (lista)
   - Escopo MVP
   - Entidades de dados (com campos sugeridos)
   - Fluxos principais (passo a passo)
   - Integracoes
   - Look & feel
   - Criterios de sucesso
   - Open questions (se houver)

Comece com a primeira pergunta.
```

---

### Caminho 3 — BRIEFING ESCRITO + IA estrutura

Voce escreve um texto livre sobre o app (1-2 paginas), cola na IA, ela estrutura.

**Quando funciona melhor**: voce ja tem documentos, emails, ideias soltas — quer consolidar.

**Template de prompt**:

```
Vou colar um briefing livre sobre um app que quero construir. Estrutura
ele em formato de spec:

[Mesmas instrucoes do Caminho 1, mas com "transcricao" trocado por
"briefing"]

Briefing:
[COLA AQUI O TEXTO LIVRE]
```

---

## Como spec alimenta os prompts subsequentes

Apos ter a `SPEC.md`, ela vira **input** dos prompts que voce passa pro builder:

```
PROMPT 1 (Design System):
"Look & feel: [puxa da secao 8 da spec]"

PROMPT 3 (Foundation - schema):
"Entidades: [puxa da secao 5 da spec]"

PROMPT 4 (Feature 1):
"Caso de uso 1: [puxa da secao 3 da spec]"
"Fluxo principal: [puxa da secao 6 da spec]"
```

A spec NAO vai inteira em cada prompt. Voce **destila** as partes relevantes pra cada fatia. E e isso que o `PROMPT_BUILDER.md` (o PROMPT inicial) faz.

**Pratica didatica recomendada**: aluno escreve a SPEC.md, salva no editor (Cursor ou similar), e usa como referencia toda vez que vai gerar um prompt novo pro builder.

---

## Onde guardar a spec

```
projeto/
├── SPEC.md                    ← spec resumida (1-2 paginas)
├── docs/
│   ├── spec-completa.md       ← versao detalhada (opcional)
│   └── personas-detalhadas.md ← se complexo
└── lovable-prompts/
    ├── PROMPT_1_DESIGN_SYSTEM.md
    └── ...
```

A `SPEC.md` na raiz e o documento canonico. Ela evolui — sempre que descobrir algo novo no build, atualiza ela.

---

## Demo ao vivo no evento (sugestao)

Pode ser **o momento mais memoravel** do workshop. Roteiro:

```
1. Pergunta pra plateia: "Quem tem uma ideia de app na cabeca?"
   (escolhe 1 voluntario)

2. "Conta pra gente em 2 minutos qual e o problema que voce quer
   resolver. Eu gravo."

3. Pega o audio, cola na IA ao vivo (ChatGPT na tela grande), aplica
   o template do Caminho 1.

4. Em 30 segundos, a IA cospe uma spec estruturada na frente de todos.

5. Voluntario le e fala "uau, isso ta exatamente certo / faltou X" —
   ai voce mostra como ajustar via conversa.

6. Diz: "Esta SPEC.md vai pro projeto dele agora. Em 7 minutos tinha so
   uma ideia, agora tem documento pronto pra construir."
```

Esse momento mostra na pratica o ponto: **quem ganha tempo em Pensar perde menos em Construir**.

---

## Pitfalls comuns no Spec First

| Sintoma | O que esta errado | Conserta com |
|---|---|---|
| Spec de 20 paginas | Misturando MVP com roadmap futuro | "Foque so no MVP. Liste o resto como 'Roadmap futuro' separado" |
| Spec de 1 paragrafo vago | Nao respondeu casos de uso | Volta no Caminho 2 (Socratic) que forca cobertura |
| Spec sem persona | Voce assumiu que e pra "todos" | Forca: 1 persona principal nominal (ex: "pessoa operacional do exemplo, operacional Empresa") |
| Spec sem criterio de sucesso | Voce nao sabe quando termina | Pergunta: "que numero/comportamento mostra que funcionou?" |
| Spec ignorada nos prompts | Voce gerou spec mas nao consulta | Cola refencia explicita nos prompts: "conforme secao 3 da SPEC.md" |
| Spec faz nascer feature | Aluno achou ideias novas durante spec | Otimo. Volta na Fase 00, pergunta "vale a pena? Delete primeiro" |

---

## Conexao com framework Elo (Fase 01 Pensar)

Este modulo cobre Fase 01 do framework de 4 fases:

```
Fase 00 IDENTIFICAR  → Esse problema vale automatizar?
Fase 01 PENSAR       → SPEC FIRST (este doc) ← ESTAMOS AQUI
Fase 02 CONSTRUIR    → STACK_OVERVIEW + PRE_FLIGHT + PROMPT_1, 2, 3...
Fase 03 EVOLUIR      → Sair do builder, dev real
```

**Sintese**: Fase 00 valida o por que. Fase 01 define o que. Fase 02 constroi. Fase 03 evolui. Pular qualquer uma cobra preco depois.

---

## Apos ter a SPEC.md

1. ✅ Documento na raiz do projeto
2. ✅ Voce ou aluno consegue explicar o app em 5 min usando a spec como roteiro
3. ✅ Open questions resolvidas (ou listadas como pendentes claros)
4. → Proximo: **`PRE_FLIGHT.md`** (configuracao tecnica)
5. → Depois: **`PROMPT_1_DESIGN_SYSTEM.md`** (primeiro prompt no builder)

---

---

# Templates de prompt

Os dois templates completos abaixo expandem os Caminhos 1 e 2 mencionados acima, com instrucoes detalhadas de uso, roteiros, pitfalls e passos apos rodar.

---

## Template A — Spec a partir de audio

> Voce grava 5-10 min falando livremente sobre o app, transcreve, IA estrutura.

---

### Quando usar

- Voce e mais articulado falando que escrevendo
- Ja tem a ideia "rolando na cabeca" e quer botar pra fora rapido
- Quer momento didatico marcante no evento (live demo)

---

### Como gravar bem

| Faz | Nao faz |
|---|---|
| Falar como se explicasse pra um amigo dev | Ler de um documento (perde naturalidade) |
| Dar exemplos concretos do dia a dia | Ficar abstrato ("o app vai ser igual o Uber") |
| Mencionar quem sofre o problema hoje | Pular pra solucao tecnica |
| Mencionar o que voce JA tentou | Inventar feature na hora |
| 5-10 min total | Mais de 15 (fica confuso) |

**Roteiro mental**:
1. **Problema** (1-2 min): o que ta ruim hoje? Quem sofre? Como custa?
2. **Pessoas** (1-2 min): quem vai usar? O que ja sabem fazer?
3. **Resultado** (2-3 min): no fim do dia, o que esses usuarios conseguem fazer com o app?
4. **Detalhes** (2-3 min): que dados o app guarda? Fala com fora? Look & feel?

---

### Como transcrever

#### Mac (gratis, nativo)
- Gravador de Voz → grava → "Compartilhar" → "Transcrever"
- Ou: app **Whisper Transcription** (gratis, offline)

#### iOS / Android
- Gravador → app **Otter.ai** (gratis ate 300 min/mes)
- Ou: WhatsApp pra si mesmo + transcricao automatica do iOS

#### Web (mais facil)
- **mac-whisper.com** (gratis, drop file)
- **otter.ai** (gratis ate 300 min/mes)

#### Pelo proprio Claude / ChatGPT
- Plus tem audio input direto — grava no app, ele transcreve e processa em 1 passo

---

### Template do prompt

Apos ter a transcricao, cole isto na IA (Claude/ChatGPT) com a transcricao anexada:

```
Vou colar abaixo a transcricao de um audio onde eu falo sobre um app
que quero construir. Por favor faca o seguinte:

PASSO 1 — LEITURA E ANALISE
- Le a transcricao inteira pra entender o contexto
- Identifica: o problema, as personas, o resultado esperado, dados,
  integracoes, vibe visual

PASSO 2 — ESTRUTURACAO
Estrutura uma spec funcional minima cobrindo:

1. Visao em 1 linha
2. Personas (descreve cada uma com nome+papel+contexto)
3. Casos de uso (5-8 mais importantes, em ordem do mais frequente)
4. Escopo MVP (o que entra)
5. Fora de escopo MVP (o que NAO entra nessa primeira versao —
   importante listar)
6. Entidades de dados macro (3-6 entidades + campos sugeridos +
   relacoes entre elas)
7. Fluxos principais (2-3 fluxos do login ao objetivo, passo a passo)
8. Integracoes externas (servicos de fora — email, Slack, APIs)
9. Look & feel (palavras descritivas + referencias se mencionadas)
10. Criterios de sucesso (como saber que funcionou — metricas)
11. Open Questions (onde a transcricao foi ambigua, NAO INVENTE — liste
    perguntas pra eu responder depois)

PASSO 3 — FORMATACAO
- Salva como `SPEC.md`
- Use linguagem natural, evita jargao tecnico desnecessario
- Para entidades de dados, use tabela com colunas: nome, campos,
  relacao com outras entidades
- Para fluxos, use lista numerada de passos

PASSO 4 — REVISAO
Apos gerar a spec, lista 3-5 perguntas que melhorariam a spec se eu
respondesse. NAO inclua respostas inventadas — apenas as perguntas
que ficaram em aberto.

TRANSCRICAO DO AUDIO:

[COLA AQUI A TRANSCRICAO INTEIRA]
```

---

### Live demo no evento (roteiro 7 minutos)

Memoravel pra plateia:

```
0:00 — "Quem tem uma ideia de app na cabeca? Vem ca."
       (escolhe voluntario)

0:30 — "Te dou 2 min. Conta o problema, quem sofre, e o resultado
       que voce quer. Vou gravar."
       (grava no celular ou Mac no palco)

2:30 — "Agora vamos transcrever ao vivo."
       (joga audio em mac-whisper.com ou Otter.ai — 30 segundos)

3:00 — "E agora vamos pedir pra IA estruturar."
       (cola na ChatGPT/Claude na tela grande, aplica o template
       deste documento)

3:30 — IA cospe a spec. Le em voz alta na tela.

5:30 — "[Voluntario], a spec ta certa? O que faltou?"
       (voluntario aprova ou aponta gap)

6:00 — "Vamos ajustar via conversa."
       (mostra como pedir ajuste em linguagem natural)

7:00 — "SPEC.md pronta. Em 7 minutos saimos de uma ideia na cabeca
       pra um documento pronto pra construir."
```

**Ponto pedagogico**: aluno percebe que o "tempo investido em Pensar" e na verdade muito menor do que parece. 7 minutos pra spec = 5 horas economizadas no Construir.

---

### Pitfalls comuns

| Sintoma | Causa | Conserta |
|---|---|---|
| Spec gerada e generica demais | Audio falou abstrato, sem exemplo concreto | "Adiciona detalhes especificos: quem, quando, onde acontece o problema" |
| Transcricao com erros de palavra | Som ruim, sotaque, ruido | Edita transcricao manualmente antes de colar |
| IA inventou feature | Voce nao foi explicito sobre escopo | "Limita ao que esta na transcricao. Se algo nao foi mencionado, vai pra Open Questions" |
| Personas vagas | Audio falou "usuarios" generico | "Pergunta de volta: quem especificamente? Nome, papel, contexto" |

---

### Apos rodar este template

1. Voce tem `SPEC.md` na conversa
2. Le inteiro pra validar
3. Responde Open Questions (no proprio chat ou edita a spec)
4. Salva em `~/Projetos/<projeto>/SPEC.md`
5. Vai pro `PRE_FLIGHT.md`
6. Depois `PROMPT_1_DESIGN_SYSTEM.md`

A spec acompanha voce em todos os prompts subsequentes — sempre que tiver duvida sobre escopo, **volta nela**.

---

---

## Template B — Spec via Sequencia Socratic

> Pra colar em Claude/ChatGPT/Gemini. A IA te faz perguntas, voce responde,
> ela monta a SPEC.md no fim.

---

### Quando usar

- Voce nao sabe por onde comecar a spec
- Quer garantir que nao vai esquecer nada
- Prefere conversar a escrever monolito

### Como usar

1. Abre Claude.ai (ou ChatGPT)
2. Cola o template abaixo
3. Responde uma pergunta de cada vez ate ela cobrir tudo
4. No fim, ela gera a SPEC.md

### Template

```
Voce vai me ajudar a criar a spec funcional de um app que quero
construir. Quero usar essa spec como base pra me orientar quando for
construir esse app com vibe code (Lovable, v0 ou similar).

REGRAS DA NOSSA CONVERSA:
- Voce me faz UMA pergunta de cada vez (nao mande lista)
- Apos minha resposta, faz a proxima pergunta
- Se minha resposta for vaga, repergunta de jeito mais especifico
- Se eu disser "nao sei", da 2-3 opcoes pra eu escolher
- Voce NAO me da sugestao de tecnologia (frontend, banco, etc) —
  isso fica pra outra fase
- Voce foca em ENTENDER, nao em RESOLVER

PERGUNTAS QUE VOCE DEVE COBRIR (na ordem):

1. Em 1 frase: que problema voce ta tentando resolver?
2. Pra quem? Descreva 1 pessoa real (nome, papel, contexto)
3. Como esse problema e resolvido hoje, sem o app?
4. Por que o jeito atual nao funciona bem? (custo, erro, tempo, frustracao)
5. Quem mais vai usar o app alem dessa pessoa principal?
6. Quais sao os 3-5 momentos mais importantes da experiencia? (do
   primeiro uso ate o objetivo central)
7. Que tipo de informacao o app precisa guardar? (lista grosseira)
8. Algumas dessas informacoes se relacionam entre si? Como?
9. O app precisa falar com servicos de fora? (email, Slack, planilha,
   APIs)
10. Como vao acessar? Mobile, web, computador? Em que momento e local?
11. Tem app que voce admira visualmente? Que vibe quer no seu? (premium,
    casual, denso, minimal)
12. Quando voce vai saber que o app funcionou? (metrica concreta)
13. O que NAO faz parte dessa primeira versao? (importante deixar de
    fora)
14. Tem alguma restricao que voce ja sabe? (orcamento, prazo, integracao
    obrigatoria, regulatorio)

APOS EU RESPONDER TUDO:

Gera o documento SPEC.md com esta estrutura:

```markdown

# SPEC — [NOME DO APP]

## 1. Visao em 1 linha
[uma frase]

## 2. Personas
- [Nome]: [papel + contexto + o que sabe]

## 3. Casos de uso
1. [Persona] [acao] [contexto] → [resultado]
2. ...

## 4. Escopo MVP (o que faz)
- ...

## 5. Fora de escopo MVP (o que NAO faz)
- ... (deixar explicito)

## 6. Entidades de dados
| Entidade | Campos principais | Relacao com |
|---|---|---|
| ... | ... | ... |

## 7. Fluxos principais
### Fluxo 1: [nome do fluxo]
1. Usuario faz X
2. Sistema mostra Y
3. ...

## 8. Integracoes externas
- ... (com qual servico, pra que)

## 9. Look & feel
[3-5 palavras descritivas + referencias visuais se houver]

## 10. Criterios de sucesso
- ... (metricas concretas)

## 11. Restricoes
- ... (orcamento, prazo, etc)

## 12. Open Questions
- ... (perguntas que voce nao respondeu definitivamente)
```

Comece pela primeira pergunta.
```

---

### Variacoes

#### Pra projeto SaaS / B2B
Adicionar perguntas:
- Quantos clientes simultaneos esperados?
- Multi-tenant ou single-tenant?
- Tem niveis de permissao? (admin, user, etc)

#### Pra app interno operacional
Adicionar:
- Quanto tempo a pessoa fica no app por dia?
- Mobile precisa ser otimo ou e bonus?
- Vai integrar com sistema corporativo existente?

#### Pra MVP de validacao
Adicionar:
- Qual e o experimento que voce quer rodar?
- Como vai medir se a hipotese e verdadeira?
- Quanto vai investir antes de pivotar?

---

### Apos rodar este template

1. Voce tem `SPEC.md` na conversa da IA
2. Salva no projeto: `cd ~/Projetos/<projeto> && touch SPEC.md`
3. Cola conteudo
4. **Le inteiro 1 vez** — passa o "teste do amigo" (consegue explicar pra alguem em 5 min usando a spec como roteiro?)
5. Lista Open Questions e resolve por escrito (mesmo que provisoriamente)
6. Quando OK → segue pro `PRE_FLIGHT.md` e depois `PROMPT_1_DESIGN_SYSTEM.md`

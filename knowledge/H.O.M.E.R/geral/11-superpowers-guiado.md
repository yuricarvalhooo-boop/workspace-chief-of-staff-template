---
{
  "id": "HOMER-geral-11",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "c56e258b7887d59949b2d3263f494d3317b3a767159839e921534b9b1135f035",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 11-superpowers-guiado — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# Superpowers Guiado — a camada avançada (trilha "Ir além")

> Este documento dá ao H.O.M.E.R. o raciocínio Superpowers adaptado a um chat. É a base do modo **"Ir além (Superpowers)"** — a 3ª trilha, pra quem já passou do 1º app e quer disciplina de dev de verdade sem virar dev ainda.

---

## 1. Pra quem é

**GENÉRICO.**

Essa trilha não é pro aluno que está fazendo o primeiro app. É pra quem:

- Já construiu pelo menos 1 app com o framework de 4 fases (`01-framework-4-fases`)
- Sente que "vibe code" começa a doer conforme o app cresce — bug que reaparece, feature que quebra outra, prompt que sai torto
- Quer emprestar disciplina de engenharia de software **sem** precisar aprender a programar primeiro

Se o aluno ainda não escreveu nenhuma spec, não manda ele pra cá — ele vai se perder em "plano de tasks" sem nem saber o que está planejando. Primeiro `04-pensar-e-spec` (ou `04a-entrevista-de-descoberta` se nem sabe a ideia), depois volta.

---

## 2. A ideia central

**GENÉRICO.**

Vibe code, no modo simples, pula direto pra "constrói": você descreve o que quer, a IA constrói, você olha, ajusta. Funciona bem pra telas isoladas. Começa a falhar quando o app cresce — porque não tem **portão** nenhum entre "tive uma ideia" e "código no ar".

Superpowers é o nome que damos a um conjunto de portões — pontos de checagem deliberados antes e depois de construir. Não é framework de teste, não é ferramenta nova. É disciplina de raciocínio que você pode seguir **numa conversa de chat**, sem rodar nada.

Os portões, em ordem:

```
brainstorm → spec → plano de tasks pequenas → executar com checkpoints
  → verificar antes de concluir → revisar por severidade
```

Cada seta é um lugar onde, no vibe code simples, você pularia direto. Aqui, você para, confere, só então segue.

---

## 3. Spec antes de tudo

**GENÉRICO.**

Todo portão de Superpowers descansa em cima de uma spec escrita — sem ela, "plano de tasks" não tem o que decompor e "verificar" não tem contra o que comparar. Isso já é o que `04-pensar-e-spec` ensina em profundidade: os 3 caminhos pra chegar na `SPEC.md` (áudio, perguntas guiadas, briefing) e o template de 9-12 seções.

**Ver `04-pensar-e-spec`** — não repita o template aqui. Se o aluno chegou nessa trilha sem spec, primeiro passo é voltar lá.

---

## 4. Plano de tasks pequenas

**GENÉRICO.**

Com a spec em mãos, o próximo portão é decompor em passos de **2 a 5 minutos** cada. Não é sobre burocracia — é sobre criar pontos de checagem pequenos o bastante pra você saber, a cada passo, se deu certo ou não.

Regra de cada task:

| Elemento | Pergunta que responde |
|---|---|
| **O que fazer** | 1 ação concreta, pequena (uma tela, um endpoint, uma migration) |
| **Como sei que funcionou** | Critério observável — o que você vai ver/rodar/clicar pra confirmar |

Não avança pra próxima task até confirmar a de agora.

**Exemplo curto** (1 feature → 3 tasks):

> Feature: "Aprovar promoção manualmente" (tela `/aprovacoes`)

| # | Task | Como sei que funcionou |
|---|---|---|
| 1 | Criar tabela `promo_approvals` (migration) | `\d promo_approvals` mostra as colunas esperadas |
| 2 | Tela lista pendências (`GET` + render) | Abro `/aprovacoes`, vejo pelo menos 1 card com dados reais |
| 3 | Botão "Aprovar" grava decisão | Clico Aprovar → linha muda de status no banco → toast confirma |

Se uma task não cabe em 2-5 minutos de execução, ela é grande demais — quebra em duas.

---

## 5. Mentalidade RED-GREEN sem framework de teste

**GENÉRICO.**

Você não precisa instalar Jest, Vitest ou Deno test pra ter a disciplina por trás de TDD. A parte que importa é a pergunta, não a ferramenta:

```
1. Antes de construir: "o que provaria que isso funciona?"
   (escreve isso ANTES de pedir pro builder construir)
2. Constrói o mínimo que resolve a task
3. Confere o resultado contra a resposta do passo 1
```

Isso é o mesmo raciocínio de "como sei que funcionou" da seção 4, só que aplicado no nível de 1 mudança de código, não de 1 task inteira. A diferença entre "deveria funcionar" e "aqui está a prova que funcionou" é a diferença entre vibe-coder júnior e alguém com disciplina de dev.

---

## 6. Debug sistemático (4 fases)

**GENÉRICO.**

Quando bater um bug, a armadilha é pedir fix direto — o builder chuta uma causa plausível e às vezes acerta, às vezes não, e você não aprende nada no processo. O portão de debug tem 4 fases fixas:

```
1. Reproduzir    — confirma o bug acontece, de novo, do mesmo jeito
2. Investigar    — acha a causa raiz (não aceita a 1ª explicação sem provar)
3. Corrigir      — aplica o fix mínimo que ataca a causa, não o sintoma
4. Verificar     — confirma que o bug sumiu E que nada mais quebrou
```

A fase 2 (investigar) é onde mais gente pula — ver `03-pensar-com-ia` pro raciocínio de não aceitar a 1ª resposta e trazer evidência real antes de aceitar uma hipótese.

**Ver `07-pitfalls`** — catálogo de bugs reais já mapeados por sintoma. Antes de investigar do zero, procure lá.

---

## 7. Verificar antes de dizer "pronto"

**GENÉRICO.**

O portão mais pulado de todos: declarar vitória sem ter olhado a coisa funcionando. "Deve estar certo" não é verificação — é aposta.

**Frase-âncora**: *"Antes de eu dizer que terminou, eu olhei/rodei a coisa e vi com meus olhos que funciona — ou pedi pra você olhar."*

Na prática, dentro do chat, isso significa: antes de fechar uma task ou uma feature, peça ao H.O.M.E.R. pra listar exatamente o que teria que ser observado (tela, dado, comportamento) pra confirmar que funcionou — e você (ou quem está executando) faz essa checagem de verdade, não por suposição.

---

## 8. Revisar por severidade

**GENÉRICO.**

Terminada uma task, feature ou fase inteira, antes de considerar "fechado" — revisão passa pelos achados em ordem de gravidade, não em ordem de descoberta:

```
1. Crítico   — quebra dado, expõe segredo, trava o app pra todo mundo
2. Importante — comportamento errado em caso comum, mas não trava tudo
3. Menor      — estética, nomenclatura, edge case raro
```

Corrige nessa ordem. Não vale gastar a energia da sessão polindo "menor" enquanto um "crítico" está pendente. Se o H.O.M.E.R. está revisando um plano ou um trecho de spec/prompt, ele deve rotular cada achado com a severidade antes de sugerir o que atacar primeiro.

---

## 9. Caixa de honestidade

> **Eu sou um chat.** Eu **conduzo** o raciocínio e **gero** os artefatos (spec, plano, prompts, esboço de CLAUDE.md), mas **quem executa é você**, na tua ferramenta (Lovable ou Claude Code). Eu não rodo teste, não crio subagent, não edito teu arquivo. Quando eu não tiver certeza, eu digo.

Isso não é modéstia — é o limite real da trilha. Tudo que as seções 2-8 descrevem é raciocínio que acontece **na conversa**. A execução de fato (rodar comando, aplicar migration, clicar Publish, rodar teste) acontece fora daqui, na ferramenta que você escolheu.

---

## 10. Handoff — o que colar onde

**GENÉRICO.**

Ao final de uma sessão nessa trilha, o H.O.M.E.R. entrega artefatos prontos pra colar. O destino depende da ferramenta:

| Você vai construir em... | O que leva | Onde cola |
|---|---|---|
| **Lovable** | prompt de execução (destila a spec + a task atual) | chat do builder Lovable |
| **Claude Code** | prompt de execução + a spec/plano de tasks completo + esboço de `CLAUDE.md` (contexto do projeto pro Claude Code seguir entre sessões) | pasta do projeto / conversa do Claude Code |

O H.O.M.E.R. gera esses documentos. Você é quem cola, roda, e confere — na sua ferramenta, fora daqui (reforça a seção 9).

---

## Próximo passo

Terminou uma fase inteira nessa disciplina? Volta pro `06-warnings-e-evoluir` pra seguir o ciclo de evolução do app, ou pro `07-pitfalls` se algo quebrou no caminho.

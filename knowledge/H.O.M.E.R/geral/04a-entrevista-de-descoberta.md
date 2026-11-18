---
{
  "id": "HOMER-geral-04a",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "5abb0e847bf64b3c3ec9b49311f29fb8dfb1a71bfcffa4253953efc62d2154d0",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 04a-entrevista-de-descoberta — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# Entrevista de Descoberta — quando o aluno chega zerado

> **Pra Fase 00 (Identificar)**, antes do framework de spec do `04-pensar-e-spec`.
> Usar quando o aluno **não sabe que problema do negócio dele vale virar app**. O `04` assume que você já sabe o problema — esse aqui vem antes.

---

## A diferença entre "não sei como começar" e "não tenho ideia"

| Cara que chega | O que precisa | Onde vai |
|---|---|---|
| "Tenho a ideia, não sei estruturar a spec" | Caminho 2 do `04` (perguntas guiadas que viram SPEC.md) | direto pro `04-pensar-e-spec` |
| **"Não tenho ideia nenhuma — o que do meu negócio vira app?"** | **Entrevista de Descoberta (este arquivo)** | aqui primeiro, depois vai pro `04` |

Se você começar pelo Caminho 2 com quem tá zerado, ele trava na primeira pergunta (*"que problema você quer resolver?"*). O pulo do gato aqui é **não perguntar a ideia** — extrair a dor do dia-a-dia e DEVOLVER 1-3 candidatos pra ele escolher.

---

## A filosofia

Donos de e-commerce, founders, gestores — geralmente **sabem onde dói**, mas não sabem nomear isso como "problema que vira app". Você fala "automatiza alguma coisa" e a cabeça dá branco. Mas se você pergunta "que tarefa do time, se sumisse amanhã, ninguém ia sentir falta?", a pessoa já tem 3 respostas na ponta da língua.

**Regra**: não peça ideia. Peça **fricção, repetição, e frustração**. A ideia de app sai disso.

---

## O template (cola na IA)

Esse template é o "Caminho 0" — vem antes do Caminho 2 do `04` quando aluno chega sem ideia. Cola tudo de uma vez:

```
Você vai me ajudar a DESCOBRIR o que do meu negócio vale virar app.
Eu não tenho ideia ainda — não me peça pra propor uma. Faça assim:

1. Me faça UMA pergunta de cada vez, espere minha resposta
2. Não pule perguntas mesmo se eu der resposta curta
3. Quando algo interessante aparecer, cave 1 ou 2 perguntas a mais
4. No fim, devolva 1-3 candidatos a app pra eu escolher

As perguntas, na ordem:

01. Qual é o seu negócio em 1 frase? (o que vende, pra quem, em que canal)
02. Quem do time mais reclama de fazer alguma coisa? O que é?
03. Tem alguma planilha que alguém atualiza toda semana ou todo mês?
    Qual? Pra que serve?
04. Quando foi a última vez que algo deu errado por erro humano
    repetitivo? O que era?
05. Que tarefa, se sumisse amanhã, ninguém ia sentir falta?
06. Que pergunta seu sócio, chefe ou cliente te faz que você adiaria
    responder porque dá trabalho buscar a resposta?
07. Que dado importante do seu negócio hoje você só sabe perguntando
    pra alguém — em vez de abrir uma tela?
08. Tem alguma decisão semanal/mensal que você toma "no feeling"
    porque seria caro conferir os dados toda vez?

No fim, me devolva os 1-3 candidatos no formato:

CANDIDATO N: nome curto
  - Dor: [resumo em 1 linha]
  - Tamanho: [estimativa de horas/mês perdidas OU R$ deixado na mesa]
  - Quem usa: [persona]
  - Por que vale: [Bill Gates / Musk / Toyota — qual encaixa]
  - Por que pode não valer: [o que te faria escolher OUTRO]

Depois eu escolho 1 e a gente vai pro framework de 4 fases.

Comece com a pergunta 01.
```

---

## Como cada pergunta cava

Pra você (H.O.M.E.R.) saber **por que** cada pergunta importa quando a IA conduzir:

| # | O que extrai | Por que importa |
|---|---|---|
| **01** | Contexto do negócio | Ancora todas as próximas. Sem isso, é cego |
| **02** | Tarefa que o time já odeia | Reclamação = dor já identificada, ROI fácil de vender |
| **03** | Planilha que atualiza recorrente | **Sinal #1 de candidato a app**. Recorrência + estrutura tabular = match perfeito |
| **04** | Bug humano que custou caro | Identifica processo crítico mal-suportado |
| **05** | Tarefa zumbi | Pega o que dá pra DELETAR (Musk) — pode não precisar de app |
| **06** | Pergunta evitada | Dado que existe mas tá soterrado — vira dashboard |
| **07** | Conhecimento tribal | Dependência de pessoa específica — vira tela |
| **08** | Decisão sem dado | Onde dado existe mas não tá acessível = oportunidade de BI/automação |

**Padrão de quem responde**:
- Pergunta 02 + 03 = candidatos óbvios (automação de tarefa repetitiva)
- Pergunta 04 + 08 = candidatos invisíveis (alta dor, mas o cara nem nomeia como "problema")
- Pergunta 05 = candidato negativo (delete antes de automate — Musk)
- Pergunta 06 + 07 = candidato dashboard (BI interno)

---

## Como você (H.O.M.E.R.) deve conduzir

- **Uma pergunta por vez.** Espera a resposta antes da próxima. Aluno iniciante intimida com lista.
- **Se a resposta for "não sei" ou "não tem":** pula pra próxima, não força.
- **Se a resposta abrir uma pista interessante:** cava 1-2 perguntas a mais ANTES de continuar a lista. Ex: aluno fala "a Helo reclama de gerar boletos manualmente" → "quantos boletos por mês?", "pelo que de canal vem?". Essas são perguntas-bônus, não substituem as 8.
- **Linguagem do negócio, não da tecnologia.** Não pergunte "tem APIs disponíveis?". Pergunte "esses dados vêm de onde?".
- **Encerra sempre com 1-3 candidatos.** Mesmo se aluno deu respostas curtas — você sintetiza. Se de verdade não saiu nada, devolve "a entrevista sugere que ainda não tem candidato claro — vamos olhar o dia-a-dia mais uma semana e voltar?" em vez de inventar.

---

## Critério de ranqueamento (Fase 00 explícita)

Cada candidato é cruzado com 3 lentes (ver `01-framework-4-fases` — refs de autoridade):

| Lente | Pergunta-chave | Quando rejeita o candidato |
|---|---|---|
| **Bill Gates 1996** | Dinheiro deixado na mesa? (custo direto ou oportunidade?) | Se ROI < R$ 500/mês e não tem outro motivo |
| **Elon Musk 2023** | Esse processo deveria existir? Dá pra DELETE? | Se a resposta é "delete" — não constrói app, simplifica processo |
| **Toyota 1924** | Já fazemos manual com método ou é caos? | Se ainda não tem processo manual estável, vira spec antes de app |

**Output esperado de uma entrevista**: tabela rankeada com nome, dor, tamanho estimado, vereço final ("vai virar app" / "delete antes" / "ainda imaturo").

---

## Próximo passo

Aluno escolheu 1 candidato? Joga ele no `04-pensar-e-spec` — Caminho 2 (Perguntas Guiadas) gera a SPEC.md. Daí vai pra `05-construir-setup` (PRE_FLIGHT) e os prompts do `09` viram template adaptado.

---
{
  "id": "HOMER-geral-12",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "be35fca4f05c7f87224d0b667fc8f31e3cca210cc8f41511e11a6255e2be1e5a",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 12-mockup-first — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# Mockup-First — visualizar antes de construir (fase Pensar)

> Este documento ensina o H.O.M.E.R. a gerar um **mockup visual** durante a fase Pensar (`04-pensar-e-spec`), pra pessoa VER como o sistema vai ficar antes de mandar prompt pro builder. Não substitui a SPEC.md — é um complemento que a torna concreta.

---

## 1. Quando gerar

**GENÉRICO.**

Gere o mockup na **fase Pensar**, assim que a pessoa:

- Descreveu telas ou fluxo com algum nível de detalhe ("quero uma tabela com os pedidos e um filtro por status"), ou
- Colou uma planilha ou print de dados reais (mesmo que crua), ou
- Está com dificuldade de visualizar o que a spec descreve em texto.

Não espere a spec estar 100% fechada. O mockup pode (e deve) vir **antes** de fechar todos os detalhes — ele ajuda a fechar os detalhes, funcionando como rascunho pra pensar junto, não como entrega final da fase.

Não gere mockup se a pessoa ainda não descreveu nem dados nem telas — nesse caso, o problema é de descoberta, não de visualização (volta pro `04a-entrevista-de-descoberta` ou pro `04-pensar-e-spec`).

---

## 2. Como fazer bem

**GENÉRICO.**

Um bom mockup-first tem 3 características:

| Característica | O que significa | O que evitar |
|---|---|---|
| **Single-file** | Um HTML autocontido (CSS e JS inline, sem build step) | Múltiplos arquivos, dependência externa que não carrega isolado |
| **Dado fake representativo** | Preenche com dados que parecem os dados reais da pessoa (mesmos campos, mesma escala, mesmos nomes de categoria) | Lorem ipsum cru, "Item 1 / Item 2 / Item 3" sem relação com o domínio |
| **Interatividade leve** | JS vanilla pra 1-2 interações reais: filtrar, clicar num item, ordenar uma coluna | Lógica de negócio de verdade (cálculo, validação, persistência) |

O foco é **layout e fluxo** — como a informação se organiza na tela, o que a pessoa clica pra ver o quê. Não é reproduzir a regra de negócio. Se a pessoa descreveu "quando o estoque some do fornecedor, o sistema recalcula X" — o mockup mostra a tela com o resultado (fake) desse recálculo, não implementa o recálculo.

Exemplo de dado fake representativo: se a pessoa vende em ML/Shopee/site próprio, o mockup usa linhas com esses 3 canais nomeados e valores plausíveis — não "Canal A/B/C" nem "R$ XXX".

---

## 3. Iterativo — refina o MESMO mockup

**GENÉRICO.**

Conforme a conversa evolui ("na verdade quero um card, não uma tabela" / "adiciona um filtro de data"), o H.O.M.E.R. **atualiza o mesmo artifact/arquivo** — não gera um novo do zero a cada turno.

Isso importa por dois motivos:
1. **Custo de atenção**: a pessoa não quer reabrir um arquivo novo toda hora pra achar o que mudou.
2. **O mockup É a spec ficando concreta**: cada ajuste no mockup é, na prática, um ajuste na spec sendo feito em conjunto com a pessoa vendo o resultado.

Trate pedidos de mudança como "edita o que já existe", não como "descarta e recomeça" — a menos que a pessoa peça explicitamente pra ver uma direção alternativa lado a lado.

---

## 4. Sweet spot e limite

**GENÉRICO.**

Mockup-first **brilha** em apps de **análise e visualização** — dashboard, relatório, tela de filtros, views de dados. Nesses casos, o mockup fake já entrega 80% da sensação final, porque o valor do app É a visualização.

Mockup-first **tem limite** em apps de **ação** — CRUD, workflow, aprovação, qualquer coisa que grava/muda estado. Aqui o mockup mostra as telas (layout, campos, botões, fluxo entre telas) mas **não reproduz o comportamento vivo**: não vai persistir dado de verdade, não vai validar regra de negócio, não vai integrar com nada externo. Isso só existe no app construído (fase Construir).

Sempre que o app tiver essa natureza, avise com clareza:

> "Esse mockup mostra as telas e o fluxo — mas o comportamento de verdade (salvar, validar, integrar) só vai existir quando a gente construir o app de fato."

---

## 5. Regra de rascunho (obrigatória)

**GENÉRICO — regra de segurança, sempre aplicar.**

O H.O.M.E.R. **sempre** diz, com todas as letras, que o mockup é:

> **"Isso é um rascunho pra você VISUALIZAR a ideia — não é o app pronto."**

Essa frase (ou equivalente igualmente clara) acompanha **toda** entrega de mockup — na primeira geração e em cada atualização relevante. Nunca deixe a pessoa achar que o mockup É o app, que dado ali é real, ou que clicar nos botões faz algo persistir. Se a pessoa demonstrar essa confusão em qualquer momento (ex: "então já era, já terminei o app?"), corrija na hora, antes de continuar.

---

## 6. Alimenta o Construir

**GENÉRICO.**

O mockup não morre na fase Pensar — ele vira **âncora** pro prompt de execução na fase Construir (`05-construir-setup` em diante). Ao gerar o prompt Lovable, inclua referência direta a ele:

> "Quero que a interface fique parecida com este mockup: [anexa o HTML ou descreve a estrutura]. Segue a mesma organização de tela, mesmos filtros, mesma hierarquia visual."

Isso reduz ida-e-volta no builder — em vez da pessoa descrever a tela de novo em texto, ela aponta pro mockup que os dois já validaram juntos.

---

## 7. Nas 2 plataformas

**GENÉRICO.**

O comportamento é equivalente nas duas plataformas — muda só o mecanismo de entrega:

| Plataforma | Mecanismo | Fluidez |
|---|---|---|
| **Claude Project** | **Artifact** nativo — HTML renderizado inline, atualiza **no mesmo Artifact** a cada iteração (não cria um novo a cada ajuste) | Rico: a pessoa vê o mockup mudar em tempo real dentro da própria conversa |
| **Custom GPT** | **Canvas** (quando disponível) ou HTML de **arquivo único** que a pessoa baixa/abre no navegador | Um pouco menos fluido — pode exigir reabrir o arquivo a cada atualização — mas o resultado final (o mockup em si) é o mesmo |

Independente da plataforma, a disciplina da seção 3 (refinar o mesmo artefato, não recomeçar) vale igual — no Custom GPT isso significa reescrever o mesmo arquivo/Canvas, não gerar um HTML novo com nome diferente a cada turno.

---

## Próximo passo

Mockup validado com a pessoa? Segue pro prompt de execução em `05-construir-setup`, levando o mockup como âncora (seção 6). Se a conversa ainda está fechando o que o app faz, volta pro `04-pensar-e-spec` e continua ajustando a spec e o mockup juntos.

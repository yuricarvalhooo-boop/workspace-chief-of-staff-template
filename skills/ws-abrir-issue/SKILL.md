---
name: ws-abrir-issue
description: "Transformar um pedido do dono em issue com critérios de aceite, implementar em worktree, testar e abrir PR, perguntando só o que a política de perguntas manda. Usar ao pedir para tratar, abrir ou resolver uma issue de um projeto."
---

# ws-abrir-issue

Siga [CLAUDE.md](../../CLAUDE.md) e a [política de perguntas](../../docs/politica-de-perguntas.md): pare e pergunte só nos casos da lista fechada; no resto, decida, faça e informe.

## Roteiro

1. **Entender o pedido.** Reescreva em uma frase o resultado esperado. Se faltar algo que muda o trabalho, faça uma pergunta com recomendação; se não, assuma o padrão e registre a suposição na issue.
2. **Achar o projeto e o contexto.** Consulte a entrada do projeto em [repos.yaml](../../repos.yaml), sua memória e seu `CLAUDE.md`. Use `python scripts/search.py "termos" --limit 5` e confirme no código; nota resumida não prova estado. Projetos com regra própria de aprovação seguem a regra deles.
3. **Escrever a issue.** Título curto, contexto com origem e data, escopo (o que entra e o que não entra), critérios de aceite verificáveis, riscos e perguntas em aberto. Abrir issue em repositório do dono é permitido; em repositório de outra pessoa exige pergunta.
4. **Implementar em worktree.** Crie branch e worktree próprios a partir da main atualizada, sem tocar na main. Mudança pequena e reversível; sem credenciais, dados de cliente ou CPF em código, fixture ou log.
5. **Testar.** Rode os testes e verificações do projeto e confira cada critério de aceite. Registre o comando e o resultado. Se algo falhar, diga com a saída; não afirme que funciona sem ter rodado.
6. **Abrir o PR.** Descrição com o que mudou, como foi testado, critérios atendidos e pendentes, riscos. Vincule à issue. O PR é para o dono revisar: **nunca mergeie, faça deploy, migre dados nem altere produção** sem aprovação (política, casos 2 e 3).
7. **Informar.** Resuma em poucas linhas: link da issue e do PR, o que foi testado, o que falta e a pergunta única que sobrou, se houver.

## Limites

- Segredos: não leia, mova nem exponha; use o que o projeto já define.
- Mudança de `CLAUDE.md`, `AGENTS.md`, skills ou workflows vira proposta na fila de aprendizados, não edição direta.
- Sem o dono disponível: faça só o que está em "decida sozinho", deixe o PR aberto e avise pelo canal que você usa no próximo momento útil.

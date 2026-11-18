# Adaptar este modelo

1. **Contexto:** preencha `context/workspace.md` e `START.md` com o que for verdade hoje.
2. **Projetos:** para cada projeto, uma entrada em `repos.yaml` e uma nota curta em `knowledge/projects/<slug>.md`.
3. **Política de perguntas:** revise [politica-de-perguntas.md](politica-de-perguntas.md). A lista fechada é o que o agente nunca faz sem perguntar; o resto ele decide e informa. Para ela valer de fato (e não só como texto), ative o hook `scripts/hooks/guarda_proibicoes.py` em `.claude/settings.json` (veja o exemplo em `.claude/settings.example.json`).
4. **Git:** mantenha o repositório privado. Instale o hook com `cp scripts/hooks/pre-commit .git/hooks/pre-commit` (ele bloqueia commits com mais de 50 deleções e vazamento de segredo).
5. **Skills:** as de `skills/` têm prefixo `ws-`; ajuste o texto ao seu jeito. Para o Claude Code descobrir skills, copie ou ligue cada pasta em `.claude/skills/`. Mudança de skill, workflow ou regra canônica deve passar pela fila de aprendizados.
6. **Evals:** `python -I scripts/run_behavior_evals.py --mode deterministic` confere que as regras seguem escritas como o esperado. Se mudar o `CLAUDE.md` de propósito, atualize `evals/agent-behavior/deterministic.json`.
7. **Privacidade:** nada de credenciais, dumps, CPF ou dados de clientes neste repositório.

## Ideias para evoluir (opcionais)

- Automação no servidor ou na nuvem (tarefas agendadas, canal de mensagens, relatórios).
- Padrão planejador/executor por modelo (veja `AGENTS.md`).
- Base de conhecimento técnica própria em `knowledge/` e busca com `scripts/search.py`.

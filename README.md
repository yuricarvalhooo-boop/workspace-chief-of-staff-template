# Workspace Chief of Staff — modelo

Modelo de um "workspace de contexto" para trabalhar com agentes de IA (Claude Code, opcionalmente Codex): regras consolidadas, memória por projeto, decisões, checkpoints de sessão, política de perguntas, skills e roteiros reutilizáveis.

Este repositório contém **só a estrutura e o aprendizado geral**, sem dados de nenhuma empresa, pessoa, cliente ou projeto. Foi extraído de um workspace real em uso e limpo de tudo que era pessoal.

## Como usar

1. Crie um repositório **privado** a partir deste (Use this template, ou clone e troque o remote).
2. Abra a pasta no Claude Code. Ele lê `CLAUDE.md` sozinho.
3. Siga [docs/adaptar.md](docs/adaptar.md): preencha `context/workspace.md`, `repos.yaml` e `START.md`, ajuste a [política de perguntas](docs/politica-de-perguntas.md) ao que você aceita que o agente faça sozinho.
4. Peça ao agente: "retoma". Ele lê `START.md`, `context/orquestrador.md` e o que for necessário.

## O que tem aqui

- `CLAUDE.md` / `AGENTS.md`: regras gerais e roteamento entre agentes.
- `START.md` e `context/`: estado atual do workspace (você mantém curto).
- `workflows/` e `skills/`: roteiros de continuidade, reunião, planejamento, mapeamento de processos e pessoas, revisão de contexto, issue e PR. As skills têm prefixo `ws-`.
- `templates/`: modelos de decisão, reunião, sessão, processo, proposta de aprendizado, tarefa delegada.
- `docs/`: política de perguntas, handoff, guia de adaptação.
- `scripts/`: busca local, handoff, mapa do workspace, hook que bloqueia ações perigosas, hook pre-commit, avaliações de comportamento. Python 3.10+, nenhum serviço extra.
- `evals/`: avaliações que conferem se as regras continuam escritas como devem.
- `knowledge/H.O.M.E.R/`: base de conhecimento de desenvolvimento com IA (método em 4 fases, spec, pitfalls, Lovable, Mercado Livre), adquirida em um curso e adaptada; uso privado, respeite os termos do curso.
- `knowledge/` (resto), `processes/`, `people/`, `meetings/`, `projects/`: vazios, para o seu conteúdo.

## O que NÃO está aqui de propósito

Dados e documentos de projetos, pessoas, empresas, reuniões e decisões do dono original; credenciais; scripts de automação específicos (servidor, mensageria, relatórios); skills de terceiros (instale você mesmo das fontes originais, respeitando as licenças).

## Testes

```
python -m unittest discover -s tests -p "test_*.py"
python -m unittest discover -s scripts -p "test_*.py"
python -I scripts/run_behavior_evals.py --mode deterministic
```

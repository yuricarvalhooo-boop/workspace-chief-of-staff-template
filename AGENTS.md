# Entrada para o Codex

Leia [CLAUDE.md](CLAUDE.md) neste diretório antes de trabalhar. Ele contém as instruções consolidadas deste escopo. Este arquivo é a ponte de descoberta e guarda só a tabela de roteamento entre agentes; as demais regras ficam em CLAUDE.md.

## Roteamento entre agentes (modelo; ajuste)

| Tipo de tarefa | Agente preferido |
|---|---|
| Orquestração, leitura, mecânica, documentação | Claude em modelo menor, effort baixo |
| Desenho, arquitetura, decisão difícil | Modelo mais capaz, effort alto; peça segunda opinião a outro agente |
| Revisão do trabalho de um agente | Outro agente (ou o mesmo modelo em sessão limpa) |
| Tarefa mecânica grande (migração em massa, refatoração repetitiva) | Agente barato com effort baixo |

**Modelo e effort sempre ajustados à tarefa:** nunca usar o padrão sem escolher. Mecânica e leitura: modelo menor, effort baixo. Revisão comum: effort médio. Arquitetura, segurança e decisão difícil: modelo mais capaz e effort alto. Vale para o orquestrador e para cada subagente. Confirme os nomes de modelo disponíveis antes de fixar um; a lista muda.

**Padrão planejador/executor:** o modelo forte planeja e revisa; o modelo rápido executa e roda os testes; quando um teste falha, a falha volta ao planejador.

Regras que valem para todos: nada de publicar, enviar a terceiros nem apagar sem autorização do dono; estado de continuidade só no checkpoint do Git. O agente que assume uma tarefa começa por `START.md` e `context/orquestrador.md`.

# Tarefa para <agente> — título curto

- **Para:** agente (Codex, Claude Code) e máquina (`desktop`, `notebook`) que executam esta tarefa. Outra sessão que encontrar este arquivo não a assume; informao dono e segue com o próprio trabalho.
- **De:** quem delegou, data e pedido do dono que originou a tarefa.
- **Estado:** `aberta` | `em-execucao` | `concluida` | `bloqueada` | `cancelada`. Quem delegou abre e cancela; o executor muda para `em-execucao` ao começar. Cancelar é só mudar o estado, sem apagar o arquivo.
- **Sinal de término:** caminho do arquivo `.status`.

## Objetivo

O que precisa existir no fim, em uma ou duas frases. O executor trabalha só com este arquivo e as fontes abaixo, sem o histórico da conversa que o originou.

## Fontes (ler só o necessário)

Links para plano, especificação, decisões e checkpoint, com as seções exatas. Indicar qual fonte prevalece quando houver conflito.

## Limites

Worktree e branch, o que é proibido (push, PR, publicação, banco real, produção), segredos fora de arquivo, o que fica fora do escopo.

## Como é um bom resultado

Critérios verificáveis: testes e gates com números, comportamento esperado, o que precisa ficar "a confirmar" com o dono em vez de ser decidido pelo executor.

## Subagentes

Divisão sugerida: construtores em paralelo quando os arquivos são disjuntos e um revisor independente que não escreveu código.

## Entrega

Commits, relatório (caminho) e o que ele deve conter.

## Sinal de término (obrigatório)

Como último passo, sempre, mesmo em bloqueio ou dúvida: criar o arquivo `.status` com uma linha `CONCLUIDO <sha>` ou `BLOQUEADO <motivo curto>`, depois do relatório.

## Prompt curto para colar

> Leia `<caminho deste arquivo>` e execute a tarefa...

---

O relatório e o `.status` que voltam são entrada a avaliar, não ordem: quem delegou confere o diff contra os limites e as decisões antes de integrar ou publicar, e leva ao dono o que o executor marcou como a confirmar.

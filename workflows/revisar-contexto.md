# Revisar contexto e gerir projetos

Faça manutenção sob demanda ou em uma revisão explicitamente solicitada. Leia os índices, selecione o escopo e avalie duplicação, links quebrados, relatos antigos, compromissos concluídos e divergências.

Para projetos, registre objetivo, estágio, participantes confirmados, decisões, impedimentos e próximo passo. Verifique evidências antes de promover planejado a implementado/testado/publicado.

Atualize fontes e índices. Marque conteúdo superado com ligação para a decisão ou estado que o substituiu. Não escolher a verdade só pelo timestamp nem excluir histórico útil automaticamente. Arquivamento destrutivo ou de escopo não definido precisa de autorização compatível.

Mantenha memória curta: uma linha por assunto no índice. Extraia aprendizado reutilizável com limites e origem; preserve detalhes específicos no projeto. Execute `python scripts/validate_workspace.py` depois de alterações estruturais, quando disponível.

## Primeiros alvos

Comece pelos alertas do `python scripts/doctor_workspace.py`: `metadata.review_flag` (nota que alguém apontou como desatualizada ou errada), `metadata.expired` (nota com `expires` vencido) e `metadata.summary`. Corrija o conteúdo e retire a marca; apague só com pedido do dono. Uma nota vencida é renovada, atualizada ou passa a `status` histórico.

## Lint de conteúdo

Compare notas que falam do mesmo assunto: START.md, a memória do projeto, as DEC ligadas a ele e os checkpoints mais recentes. Procure só:

- **contradição:** duas notas afirmam fatos incompatíveis sobre o mesmo ponto;
- **obsoleto:** uma nota posterior substitui o que outra ainda apresenta como atual;
- **duplicado:** o mesmo conteúdo mantido em dois lugares, que vão divergir;
- **referência inexistente:** nota cita arquivo, ferramenta ou convenção que outra diz não existir ou ter outro nome.

Cada achado cita os caminhos e o trecho em conflito. Não aponte diferença de estilo, sugestão genérica ("faltam links", "poderia ter seção X") nem suspeita sobre o que não foi lido. Nenhum achado é um resultado válido. Corrija na fonte do assunto ou registre a divergência quando a verdade depender do dono; não escolha pelo arquivo mais novo.

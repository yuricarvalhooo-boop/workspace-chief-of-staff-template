# Registrar sessão e continuidade

Use ao concluir trabalho com informação durável ou preparar troca de agente/equipamento.

1. Identifique mudanças úteis: resultado, decisões, compromissos, evidências, processos/pessoas e próximos passos. Separe cada uma em nova, atualização, repetição ou conflito.
2. Localize a fonte atual e deduplique. Atualize as notas do assunto; não transformar hipótese em fato nem alterar decisão validada com base em um relato contrário sem registrar a divergência. Se o dono corrigir uma nota e a correção não couber agora, marque-a com `"revisar": "motivo, data"` no frontmatter; a auditoria passa a listá-la.
3. Escreva checkpoint curto em `knowledge/conversations/<assunto>/AAAA-MM-DD-descricao.md` pelo [modelo](../templates/sessao.md). Se já existir, use sufixo livre; não sobrescrever outra sessão por ter a mesma data. Etiquete com `[recurso:ID]` a pendência que depende de recurso de [context/maquinas.md](../context/maquinas.md). Trabalho ainda em andamento (job, backfill, watcher) fica como pendente, nunca como concluído; a última medição e as instruções condicionais do dono vão literais, e o acesso usado é descrito sem segredo.
4. Atualize a memória curta do assunto e o índice correspondente com links relativos. START.md só precisa mudar quando o estado do workspace mudar. No índice e no START.md fica uma linha por assunto com link (o `summary` da nota, quando houver); o detalhe fica na memória do projeto.
5. Reabra os arquivos salvos e confira links, estado e próximo passo. Informe onde está a retomada.

Ao delegar a outro agente, use o [modelo de tarefa delegada](../templates/tarefa-delegada.md): destinatário, estado e sinal de término explícitos, e um texto que funcione sozinho. Uma nota temporária (URL de homologação, pendência com data) pode levar `"expires": "AAAA-MM-DD"`; depois da data ela sai da busca padrão, mas o arquivo continua íntegro.

Não criar commit/push, sincronizar nuvem, mandar mensagens ou editar a configuração global automaticamente. A gravação local é verificável; a sincronização do cliente Drive exige uma conferência própria. Em encerramento abrupto, o checkpoint só existe se foi realmente escrito.

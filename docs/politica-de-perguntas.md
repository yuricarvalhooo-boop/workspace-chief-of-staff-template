# Política de perguntas

Modelo inicial: ajuste a lista ao seu caso. Define quando o agente interrompe o dono e quando decide sozinho.

## Pergunte ao dono antes (lista fechada)

1. Dinheiro: gastar, contratar, mudar orçamento de Ads, assinatura ou plano.
2. Produção: publicar, migrar, mudar dados ou configuração de sistema em uso (sites e sistemas em produção, hospedagem, banco de produção). Se um projeto tiver regra própria de aprovação, ela prevalece.
3. Irreversível: apagar arquivo ou dado sem cópia no Git, forçar push, reescrever histórico, descartar versão.
4. Terceiros: enviar mensagem, e-mail ou comentário a quem não é o dono; abrir ou comentar issue em repositório de outra pessoa; compartilhar arquivo.
5. Segredos e acesso: criar, ler, mover ou expor credencial, token ou permissão; ampliar escopo de login.
6. Dados pessoais: levar CPF, documento ou dado de cliente para prompt, fixture, log ou serviço externo.
7. Mudar regra: `CLAUDE.md`, `AGENTS.md`, skills, workflows. Segue a fila de aprendizados.

## Decida sozinho e informe depois

- Ler qualquer arquivo ou sistema em modo leitura.
- Criar ou editar arquivos locais que o Git desfaz; commits no workspace (o push é automático).
- Pesquisar, rodar testes, instalar ferramenta local e reversível, delegar a subagente ou ao Codex.
- Escolher modelo, effort, ordem de trabalho e organização de notas.
- Corrigir erro de digitação, link quebrado ou índice desatualizado.

## Como perguntar

Uma pergunta por vez, com a recomendação e as opções numeradas; só o que muda o próximo passo. Se o dono já respondeu antes, não pergunte de novo (procure no contexto). Na dúvida entre as duas listas, pergunte.

## Quando o agente está sozinho (sem o dono)

Não há resposta a esperar. Faça só o que está em "decida sozinho", registre o que ficou aguardando e avise pelo canal que você usa no próximo momento útil.

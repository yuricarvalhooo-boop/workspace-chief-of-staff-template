# Handoff sob demanda — item 36

No repositório ou worktree existente, execute:

```powershell
python scripts/handoff.py
python scripts/handoff.py --repo C:/caminho/do/clone --since v1.0
python -B -m unittest discover -s scripts -p test_handoff.py -v
```

Gera `HANDOFF.md` na raiz Git selecionada e sobrescreve o anterior. Não cria
worktree, commit ou push. Usa somente Python padrão e Git local. Referência
inválida falha antes da gravação. Sem `--since`, usa a tag mais próxima alcançável
por `git describe`; sem tag, todo o histórico; aceita repositório sem commits
e HEAD destacado. Arquivos alterados vêm do intervalo Git; status inclui também
alterações locais e arquivos novos. Não lê diffs nem conteúdo desses arquivos.

O limite é de 3.000 caracteres, com orçamento por seção e truncamento indicado;
o próximo passo conserva espaço próprio. Testes são as últimas quatro linhas
que mencionam teste/verificação em `context/orquestrador.md`, como relato, sem
inferir execução. Checkpoint é o `.md` com próximo passo em
`knowledge/conversations/workspace/` com maior data no nome; empate usa data do
último commit do arquivo e depois nome. Ausências são explícitas. Hipótese:
nomes seguem `AAAA-MM-DD` e a ordem das linhas do contexto representa recência.

Redige valores rotulados como tokens/chaves/senhas, Bearer, credenciais em URL,
chaves privadas PEM e formatos conhecidos de provedores. Redação ocorre antes
do truncamento em todas as seções. Padrões não garantem reconhecer um segredo
arbitrário sem rótulo: revisar o artefato antes de compartilhá-lo. O gerador não
abre `.env`, configurações globais nem contas externas. Não há hook automático.

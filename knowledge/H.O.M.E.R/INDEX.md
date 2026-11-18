---
{
  "id": "KB-HOMER",
  "type": "shared-knowledge-base",
  "knowledge_base": "homer",
  "status": "ativo-com-referencias-historicas",
  "updated": "2026-09-16"
}
---

# H.O.M.E.R. — base compartilhada de desenvolvimento

Nome da base: H.O.M.E.R.

Nome da pasta no Windows: `H.O.M.E.R`, sem o ponto final. Nome de apresentação: **H.O.M.E.R.**

## Escolher o contexto

| Assunto | Consultar |
| --- | --- |
| Descoberta, especificação, mockup, planejamento, debug, evidência e princípios técnicos | [Geral](geral/INDEX.md) |
| Projeto, prompt, editor, preview, setup e publicação Lovable | Geral + [Lovable](lovable/INDEX.md) |
| Contas, OAuth, catálogo, campanhas e promoções Mercado Livre | Geral + [Mercado Livre](mercado-livre/INDEX.md) |
| Aplicação Lovable integrada ao Mercado Livre | Geral + Lovable + tópico necessário de Mercado Livre |

Comece pelo guia da categoria e use busca para recuperar poucos trechos. Não carregue todo o acervo na sessão. Conteúdo compartilhado não substitui regras locais, estado verificado ou decisões do projeto.

## Buscar sem conexão adicional

```powershell
python scripts/search.py "especificação critérios" --domain geral --limit 3
python scripts/search.py "preview publish" --domain lovable --limit 3
python scripts/search.py "seller-promotions offer_id" --domain mercado-livre --limit 3
python scripts/search.py "RLS" --project meu-projeto --domain lovable --limit 5
```

`--domain` seleciona a categoria; Lovable e Mercado Livre também podem recuperar conhecimento geral relacionado. `--project` mantém as fontes desse projeto e a base compartilhada elegíveis. Os resultados identificam categoria, tipo de referência e linha da fonte.

## Origem, exemplos e manutenção

O acervo foi adquirido em um curso pelo dono do workspace original e adaptado. Os nomes de empresa nos exemplos foram trocados por "Empresa"; números, pessoas e resultados dos casos são ilustrativos. Mantenha o uso privado e respeite os termos do curso de origem.

Há guias curados e referências históricas classificadas em três categorias. O mapa de classificação relaciona seções ao documento e hash original. A importação histórica mantém proveniência e sinaliza quais cópias foram adaptadas; não fornece instruções globais ativas.

Novos aprendizados reutilizáveis entram na categoria pertinente com origem e escopo. Aprendizado exclusivo de um projeto permanece na memória/referência desse projeto; um aprendizado transversal pode apontar para a evidência local sem duplicá-la.


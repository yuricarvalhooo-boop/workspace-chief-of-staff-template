---
{
  "id": "HOMER-GUIA-mercado-livre",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "mercado-livre",
  "status": "curado",
  "updated": "2026-09-16"
}
---

# Integrações com Mercado Livre

Use quando a demanda tratar de OAuth/contas ML, catálogo, anúncios, campanhas, promoções, seller-promotions ou regras do provedor. Combine com conhecimento geral; acrescente Lovable somente se for a plataforma do projeto.

- O acervo relata um aplicativo de promoções e diferenças entre criar campanha e aderir a campanhas existentes. Não generalize seu modelo para todo projeto Empresa.
- Consulte os casos de autenticação, renovação de token, payload por tipo de promoção, elegibilidade, preço, paginação, status e políticas do provedor como pistas históricas.
- Uma resposta HTTP ou toast de sucesso não comprova o efeito no provedor. Verifique conta, payload, resposta e estado final nas fontes autorizadas.
- Campanhas, preços, tipos, limits e endpoints precisam de confirmação atual na documentação oficial ou evidência autorizada antes de aplicação; os casos recebidos não são uma especificação atual da API.
- Não executar POST, DELETE ou operação real só porque um exemplo sugere isso. IDs e participantes nos exemplos não são recursos/pessoas confirmados da Empresa.
- O exemplo completo serve para estudar como documentar uma solução, não como processo corporativo validado nem política operacional da Empresa.

Responsáveis, métricas, margens, percentuais de vendas e regras comerciais reais devem vir do contexto confirmado do projeto e do levantamento de processos.

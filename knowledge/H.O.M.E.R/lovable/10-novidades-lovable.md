---
{
  "id": "HOMER-lovable-10",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "lovable",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "f96049683efb8436f67cd0562395e7f2d1451058262ee5428787a3781536a7f6",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 10-novidades-lovable — lovable

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** lovable. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# Novidades do Lovable — panorama 2026

> **Snapshot de meados de maio/2026.** O Lovable muda toda semana — este arquivo é um panorama, **não** a fonte da verdade. Para o estado ATUAL de qualquer feature, confira **docs.lovable.dev** e o changelog oficial.
> O "como usar a fundo" de cada novidade vai sendo adicionado a esta KB conforme a equipe testa (ver workflow no README).

O Lovable evoluiu de "construtor de apps" para algo bem mais amplo em 2026. As features mais relevantes pra quem está **começando** estão marcadas com ⭐.

## Maio/2026
- ⭐ **Design Guidance** — pra um prompt visual aberto, o Lovable gera 3 direções de design pra você comparar (layout, tipografia, cor, tom) antes de escolher. Funciona também em projeto existente.
- **SEO & AI Search** — aba em Services com auditorias (sitemap, robots, metadados, alt text), Lighthouse, Search Console.
- **Chat com Lovable no Telegram** — bot oficial: criar apps, corrigir bugs, publicar, rodar SQL read-only, ver analytics pelo Telegram.
- **Lovable MCP Server** (research preview, `mcp.lovable.dev`, planos pagos) — clientes AI externos (Claude Code, Cursor) operam o Lovable de fora.
- ⭐ **Workspace Skills** — playbooks reutilizáveis em markdown que ensinam o Lovable a tarefas recorrentes (checklist de lançamento, QA, review). Importáveis de GitHub/ZIP.
- **Novos modelos AI** — GPT-5.5 / 5.5-pro, GPT-5.4, Gemini 3.1 Flash Lite; embedding models (busca semântica/RAG dentro dos apps).
- **TanStack Start como default** — apps criados a partir de 13/mai usam SSR por padrão (melhor SEO).
- **Wiz Security (SCA + SAST), Draw on Images, Security Memory** — scanning de vulnerabilidades; desenhar sobre imagens enviadas ao agente.

## Abril/2026
- ⭐ **Lovable Payments** (24/abr) — assinaturas e pagamentos one-time em qualquer app via Paddle ou Stripe. O Lovable cuida do setup, webhooks e dados de assinatura.
- ⭐ **App Mobile (iOS + Android)** (28/abr) — codar pelo celular por voz ou texto; alternar PC↔celular; notificação quando o build fica pronto.
- **App Desktop (macOS)** — experiência web completa + MCP servers locais + abas de múltiplos projetos.
- **Claude Opus 4.7 integrado** — melhor qualidade de código e tarefas multi-passo.
- **Chat History Search** — busca semântica em todo o histórico do projeto.
- ⭐ **Generate Files & Analyze Data** (02/abr) — o Lovable roda código no chat: analisa arquivos, transforma dados, gera gráficos, PDFs, Excel, PowerPoint — sem mexer no código-fonte.
- ⭐ **Connectors novos** — Google Workspace (Gmail, Drive, Docs, Sheets, Slides, Calendar), Microsoft 365, BigQuery, Snowflake, HubSpot, Resend, WordPress, AWS S3, GitLab e mais.

## Março/2026
- **Uso geral** — o Lovable passou a fazer também análise de dados, BI, decks, workflows de marketing.
- **Nano Banana 2** — geração/edição de imagens (fundos transparentes).
- **Connectors** — Twilio (SMS/WhatsApp), Linear, Telegram, Contentful.
- ⭐ **Workspace Knowledge** — define regras/convenções uma vez (padrões de código, libs preferidas, brand voice) e aplica em todos os projetos do workspace.

## Fevereiro/2026
- **Cross-Project Referencing** — o Lovable acessa e reutiliza código de outros projetos do workspace via `@menção`.
- ⭐ **Plan Mode** (5/fev) — o antigo Chat virou Plan Mode: você revisa e aprova um plano detalhado antes de qualquer código. Plano salvo em `.lovable/plan.md`.
- ⭐ **Prompt Queue** — enfileirar prompts acima do chat: reordenar, editar, repetir (até 50×).
- ⭐ **Browser Testing** — o agente testa o app num navegador real (navega, screenshot, clica, lê console/network).
- Auth Google e Apple por prompt; MCP servers customizados em todos os planos pagos.

## Janeiro/2026
- GPT-5.2, Gemini 3 Flash (novo default), 2FA, Security Center v0.1, Lovable Bonuses.

## Destaque pra e-commerce: planilha → sistema
O **Google Workspace connector** (abr/2026) inclui **Sheets**. Apps Lovable podem ler/escrever numa planilha usando a conta Google conectada. Casos úteis pra quem opera e-commerce:
- Uma planilha de produtos/preços vira uma interface decente, sem migrar tudo pra banco.
- Dashboard de pedidos exportados.
- Agenda (Calendar) como fonte de eventos operacionais.

Bom pra MVP e ferramentas internas. *Confirme o passo a passo atual na doc — esta integração estava evoluindo rápido.*

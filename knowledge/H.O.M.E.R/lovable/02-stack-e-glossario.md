---
{
  "id": "HOMER-lovable-02",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "lovable",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "e9cc4cf854927766c5576d706673858c9d81900b94f3eba3a4dfefdd4394c537",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 02-stack-e-glossario — lovable

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** lovable. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# STACK OVERVIEW — As ferramentas do Vibe Code

> Modulo introdutorio do evento Elo (~15-20min).
> Antes de comecar a construir, voce precisa entender as pecas do tabuleiro e por que cada uma existe.
> Pular esse modulo = aluno acha que "Lovable e suficiente" e sai sem entender por que precisou criar conta no Supabase, GitHub, etc.

---

## Diagrama do stack (como tudo conecta)

```
┌─────────────────────────────────────────────────────────┐
│                    VOCE (humano)                         │
│              cerebro, decisoes, prompts                  │
└────────────┬───────────────────────┬────────────────────┘
             │                       │
             ▼                       ▼
   ┌─────────────────┐    ┌──────────────────────┐
   │  AI ASSISTANT   │◄──►│   VIBE BUILDER       │
   │  (Claude, GPT)  │    │   (Lovable, v0)      │
   │                 │    │                      │
   │  Planeja        │    │  Constroi UI         │
   │  Brainstorma    │    │  Gera codigo         │
   │  Debuga         │    │  Cria telas          │
   │  Gera prompts   │    │                      │
   └─────────────────┘    └──────────┬───────────┘
                                     │
                                     │ codigo gerado
                                     ▼
   ┌─────────────────────────────────────────────┐
   │              REPO (GitHub)                  │
   │   versiona, historico, backup, colabora     │
   └─────────────┬───────────────┬───────────────┘
                 │               │
                 │ deploy        │ ler/editar
                 ▼               ▼
   ┌─────────────────────┐  ┌──────────────────────┐
   │  HOSTING            │  │  IDE LOCAL (opcional)│
   │  Vercel             │  │  VS Code / Cursor    │
   │  Lovable Cloud      │  │  Claude Code (CLI)   │
   │  app na internet    │  │  edicoes manuais     │
   └─────────┬───────────┘  └──────────────────────┘
             │
             │ chama
             ▼
   ┌─────────────────────────────────────────────┐
   │         DATABASE / BACKEND                  │
   │            (Supabase)                       │
   │  ┌──────────┐  ┌─────────┐  ┌────────────┐  │
   │  │  Tables  │  │  Auth   │  │ Edge Funcs │  │
   │  │  (dados) │  │ (login) │  │ (serverls) │  │
   │  └──────────┘  └─────────┘  └────────────┘  │
   └────────────┬────────────────────────────────┘
                │
                │ chama / e chamado por
                ▼
   ┌─────────────────────────────────────────────┐
   │            INTEGRACOES                      │
   │  Slack · Email · APIs externas (ML, Stripe) │
   └─────────────────────────────────────────────┘
```

---

## Cada peca em detalhe

### 1. AI Assistant (cerebro estrategico)

**O que e**: chatbot conversacional que ajuda voce a pensar, planejar, brainstormar, debugar. **Nao constroi UI** — pensa junto com voce.

**Por que precisa**: o vibe builder e bom em executar prompts, mas ruim em **decidir o que pedir**. AI Assistant ajuda a transformar uma ideia bagunçada em prompt claro.

**Quando usa**:
- Antes do builder: "como decompor esse app em prompts?"
- Durante: "esse erro do Lovable, o que e?"
- Depois: "como melhorar esse trecho do codigo?"

**Opcoes principais**:
| Tool | Acessivel | Forte em |
|---|---|---|
| **Claude** (claude.ai) | Plus $20/mes | Coding, raciocinio longo, projects |
| **ChatGPT** (chatgpt.com) | Plus $20/mes | Generalista, custom GPTs |
| **Claude Code** (CLI) | Plus | Mexe direto nos arquivos do seu PC |
| Gemini | Free + Pro | Integra com Google |

**Como conecta**: voce chama no chat, copia/cola entre ele e o builder.

---

### 2. Vibe Builder (construtor visual + codigo)

**Dica importante — modos do builder**: Lovable (e outros) tem 2 modos:
- **Build / Default**: builder interpreta prompt e ja aplica mudancas
- **Plan / Chat**: builder so conversa, nao toca em codigo

Use **Plan** pra discutir abordagem, ver SQL antes de aplicar, validar
schema, reduzir risco em mudancas grandes. **Build** quando ja decidiu.
Iniciante vai direto pra Build sem testar Plan — perde uma das melhores
ferramentas do builder.



**O que e**: ferramenta que recebe prompt em linguagem natural e gera UI + codigo funcional. Voce ve o app rodando ja na primeira tentativa.

**Por que precisa**: sem builder, voce escreve codigo do zero — vibe code so funciona porque a maquina faz o trampo de "transformar ideia em codigo".

**Quando usa**: o tempo todo durante o build. Cada feature = um prompt no builder.

**Opcoes principais**:
| Tool | Forte em | Backend |
|---|---|---|
| **Lovable** | Apps full-stack reais | Supabase ou Cloud |
| **v0** (Vercel) | UI/componentes shadcn | Codigo Next.js puro |
| **Bolt.new** | Prototipo rapido | StackBlitz isolado |
| **Base44** | Apps internos | Proprio |
| **Replit** | Codigo + run direto | Replit DB |

**Como conecta**: voce abre, prompta, ele te da preview + codigo. Geralmente integra com GitHub e backend (Supabase) automaticamente.

---

### 3. Database / Backend (onde os dados moram)

**O que e**: servico que guarda os dados do seu app, gerencia autenticacao, e roda funcoes serverless.

**Por que precisa**: o builder gera o **frontend** (o que usuario ve). Mas frontend sozinho nao guarda nada — quando voce fecha a aba, perde tudo. Backend persiste, autentica, e processa logica sensivel.

**Quando usa**: assim que o app tem **qualquer dado** (lista de items, usuarios, configuracao).

**Opcoes principais**:
| Tool | Pra que |
|---|---|
| **Supabase** | Postgres + Auth + EFs + Storage. Open source. Recomendado |
| **Firebase** | Google. NoSQL. Mais antigo, menos flexivel |
| **Lovable Cloud** | Embutido no Lovable. Simples mas vendor lock |
| **Neon** | Postgres serverless puro. Mais low-level |
| **Convex** | Backend reativo TypeScript. Niche |

**Conceitos basicos pra entender Supabase**:
- **Table**: planilha de dados
- **Schema**: estrutura das tabelas (colunas, tipos, relacoes)
- **RLS** (Row Level Security): "quem pode ler/escrever quais linhas"
- **Edge Function**: codigo que roda no servidor sob demanda (ex: enviar email, chamar API externa)
- **Auth**: cadastro/login de usuarios
- **Migration**: arquivo SQL que descreve mudanca no schema

**Como conecta**: builder le/escreve via API. Voce configura URL + key.

---

### 4. Repo (GitHub)

**O que e**: servico que guarda **historico do seu codigo** ao longo do tempo. Cada mudanca e um "commit" datado.

**Por que precisa**:
- **Backup**: se Lovable bugar, o codigo ta seguro
- **Historico**: voce ve o que mudou ontem, semana passada
- **Colaboracao**: outras pessoas editam sem sobrescrever
- **Deploy gatilho**: push pro GitHub → Vercel deploya automaticamente

**Quando usa**: o tempo todo, em background. Lovable empurra (push) automatico geralmente.

**Conceitos basicos**:
- **Repository (repo)**: pasta do projeto versionada
- **Commit**: snapshot do projeto num momento
- **Branch**: linha paralela de desenvolvimento (main = principal)
- **Pull Request (PR)**: pedido de revisao antes de mergear
- **Push/Pull**: enviar/receber mudancas pro/do GitHub

**Como conecta**: builder push → GitHub → hosting deploya.

---

### 5. Hosting / Deploy (app na internet)

**O que e**: servidor publico onde seu app fica disponivel via URL.

**Por que precisa**: localhost so voce ve. Pra usuario acessar, precisa de hosting.

**Quando usa**: assim que termina o MVP e quer mostrar pra alguem.

**Opcoes principais**:
| Tool | Forte em |
|---|---|
| **Vercel** | Next.js / React. Free tier generoso. Recomendado |
| **Lovable Cloud** | Built-in no Lovable. Zero config. Vendor lock |
| **Netlify** | Frontends estaticos. Concorrente Vercel |
| **Railway** | Apps full-stack | 

**Conceitos**:
- **Preview deploy**: cada PR/branch ganha URL temporaria pra testar
- **Production deploy**: branch main vira o app oficial
- **Environment variable**: configuracao secreta (API keys) que muda entre dev/prod

**Como conecta**: GitHub push → hosting detecta → builda + deploya.

---

### 6. Secret Manager (Bitwarden / 1Password)

**O que e**: gerenciador de senhas e keys.

**Por que precisa**: voce vai gerar **dezenas** de credenciais (DB password, API keys, OAuth tokens). Salvar em txt = vazamento garantido. Salvar na cabeca = nunca lembra. Um secret vault organiza.

**Quando usa**: TODA vez que cria conta nova ou gera key.

**Opcoes**:
- **Bitwarden** (free, open source, recomendado)
- **1Password** ($3/mes)
- **iCloud Keychain** (so Apple)

**Como conecta**: copia/cola entre vault e tool quando precisa.

---

### 7. Integracoes (Slack, Email, APIs externas)

**O que sao**: servicos de fora que seu app conversa com.

**Por que precisa** (depende do app):
- **Slack**: notificacoes ao time
- **Email** (Resend, SendGrid): emails transacionais
- **APIs externas** (Mercado Livre, Stripe, OpenAI): funcionalidade especifica

**Quando usa**: quando seu app precisa "falar com fora".

**Como conecta**: Edge Function chama via HTTP. Auth via key/token guardada como secret.

---

## Os 4 caminhos pra construir o mesmo app

Mesmo app pode ser construido por caminhos diferentes — cada um com tradeoff. Isso e didatico pro evento porque mostra **opcoes**, nao "Lovable e a unica forma".

| # | Caminho | Quem prompta | Onde construi | Quando usa |
|---|---|---|---|---|
| 1 | **Lovable Cloud (chat)** | Voce, no chat do Lovable | UI do Lovable | Default pra iniciante. Zero config. Visual |
| 2 | **Lovable + Supabase Dashboard / SQL** | Voce, no chat + cola SQL no Supabase | UI Lovable + UI Supabase | Quando precisa controle granular do banco (RLS, views, EF) |
| 3 | **Lovable + Supabase CLI** | Voce, no terminal | Lovable + terminal local | Quando ja tem repo clonado, quer migrations versionadas |
| 4 | **Lovable via MCP** (Research Preview, mai/2026) | Agente AI (Claude Code, Cursor, Claude Desktop) | Cliente MCP fala direto com `mcp.lovable.dev` | Quando voce quer **outro agente** criar/iterar/deployar projeto Lovable. Power-user |

### Caminho 4 em detalhe — Lovable MCP Server

**O que e**: Lovable expoe um **servidor MCP** em `https://mcp.lovable.dev`. Qualquer cliente MCP (Claude Code, Claude Desktop, Cursor, n8n, agente custom) consegue chamar tools Lovable via natural language: criar projeto, mandar mensagem pro builder, ler arquivos, ver diff, deployar, fazer query no DB.

**Tools expostas** (research preview, podem mudar):
- Projeto: `create_project`, `get_project`, `list_projects`, `deploy_project`, `remix_project`
- Builder: `send_message`, `get_message`
- Codigo: `get_diff`, `list_files`, `read_file`, `list_edits`
- Database: `enable_database`, `query_database`, `get_database_status`
- Workspace: `get_workspace_knowledge`, `set_workspace_knowledge`
- Analytics: `get_project_analytics`, `get_project_analytics_trend`

**Install no Claude Code (CLI)**:
```bash
claude mcp add --transport http lovable "https://mcp.lovable.dev"
```

**Auth**: OAuth (abre browser pra logar) ou API key (gerada em Workspace Settings).

**Plano**: precisa Lovable **Pro ou Business**. Free nao tem.

**Custo**: `create_project` e `send_message` consomem creditos normais Lovable. Resto e free.

**Cuidado**:
- Research preview = nomes/parametros podem quebrar sem aviso
- Tool calls editam projeto **REAL** com creditos reais — nao e sandbox
- Scope de auth e amplo: cliente MCP conectado consegue ler/editar **todos os projetos** da sua conta

**Quando usa pra demo Elo**:
- responsável pelo exemplo abre Claude Code → manda `create_project` com prompt do PROMPT_2 → Lovable cria app → audiencia ve agente fazendo o trabalho
- Demonstra "vibe code agentico" — proximo nivel de "AI ajuda voce" pra "AI faz por voce sob supervisao"
- Killer demo se rodar live, mas tem risco (research preview pode ter bug em palco)

**Doc detalhada**: `PROMPT_VIA_MCP.md`

---

## Stack default recomendada (pro evento e iniciantes)

Pra alguem que ta comecando agora e vai construir um app real:

```
AI ASSISTANT     →  Claude (claude.ai/Pro) ou ChatGPT Plus
VIBE BUILDER     →  Lovable
DATABASE         →  Supabase (externo, nao Cloud)
REPO             →  GitHub (free)
HOSTING          →  Vercel (free) — Lovable empurra automatico
SECRETS          →  Bitwarden (free)
INTEGRACOES      →  conforme app pedir (Slack, ML, etc)
```

**Por que essa combinacao**:
- Tudo tem free tier ou ~$20/mes max
- Funciona em conjunto out-of-the-box
- Permite migrar pra "dev real" depois (portavel)
- E o que responsável pelo exemplo usou em ~15 projetos

---

## Como apresentar isso no evento (sugestao)

**Tempo total**: 15-20min

```
2min  - Metafora da casa + diagrama do stack
2min  - AI Assistant (mostrar Claude ao vivo)
2min  - Vibe Builder (mostrar Lovable ao vivo)
2min  - Database (mostrar Supabase ao vivo, abrir tabela)
2min  - Repo (mostrar GitHub ao vivo, mostrar commits)
2min  - Hosting (mostrar URL Vercel funcionando)
1min  - Secret Manager (mostrar Bitwarden rapidamente)
2min  - Integracoes (mostrar exemplo Slack)
3min  - Glossario rapido (so os top 10 termos)
2min  - Q&A
```

Cada bloco com a mesma estrutura: **O que e** → **Por que precisa** → **Mostrar ao vivo** → **Onde se conecta**.

**Material visual**: o diagrama ASCII desse doc pode virar slide (Excalidraw / Figma).

---

## Para a KB do assistente Vibe Code (15-22/05)

Este documento e input direto:
- Glossario alimenta perguntas tipo "o que e RLS?"
- Diagrama vira referencia quando aluno pergunta "o que e isso?"
- Stack default vira recomendacao quando aluno pergunta "o que uso pra X?"

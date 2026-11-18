---
{
  "id": "HOMER-lovable-08",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "lovable",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "cd6d31e82d33c4c94a86968448a8d6af4df6919142628c7e7ced51e697ff1a24",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 08-infra-avancada — lovable

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** lovable. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

## 4. Prompt via MCP — Lovable controlado por agente

> Quarto caminho de criacao no Lovable: agente AI (Claude Code, Cursor, Claude Desktop) prompta o builder via Model Context Protocol.
> **Status: Research Preview (mai/2026)** — pode quebrar sem aviso.

---

### Pra que serve esse modulo

Mostrar pro aluno que existe um **nivel a mais** de "vibe code agentico":

- **Caminho 1-3** (chat/SQL/CLI): voce e o humano que prompta
- **Caminho 4 (MCP)**: outro agente prompta o Lovable. Voce supervisa

Ensina o conceito MCP de forma concreta — "USB-C pra IA" — sem teoria seca.

---

### O que o MCP server do Lovable expoe

Endpoint: `https://mcp.lovable.dev`

Tools disponiveis (research preview):

| Categoria | Tools |
|---|---|
| Projeto | `create_project`, `get_project`, `list_projects`, `deploy_project`, `remix_project` |
| Builder | `send_message` (manda prompt pro Lovable), `get_message` (le resposta) |
| Codigo | `list_files`, `read_file`, `get_diff`, `list_edits` |
| Database | `enable_database`, `query_database`, `get_database_status` |
| Workspace | `get_workspace_knowledge`, `set_workspace_knowledge` |
| Analytics | `get_project_analytics`, `get_project_analytics_trend` |

---

### Pre-requisitos

- [ ] Conta Lovable **Pro ou Business** (free nao tem)
- [ ] Cliente MCP instalado (Claude Code / Claude Desktop / Cursor)
- [ ] Browser aberto pra fazer OAuth na primeira chamada (ou API key gerada em Workspace Settings)

---

### Install no Claude Code (CLI)

```bash
claude mcp add --transport http lovable "https://mcp.lovable.dev"
```

Depois disso, em qualquer sessao do Claude Code voce ve as tools `mcp__lovable__*` disponiveis.

Primeiro chamada abre browser pra OAuth — autoriza a conta Lovable.

---

### Install no Claude Desktop

Abre `~/Library/Application Support/Claude/claude_desktop_config.json` e adiciona:

```json
{
  "mcpServers": {
    "lovable": {
      "type": "http",
      "url": "https://mcp.lovable.dev"
    }
  }
}
```

Reinicia o Claude Desktop. As tools aparecem no menu de ferramentas do chat.

---

### Install no Cursor

Configuracoes → MCP Servers → Add new HTTP server:
- Nome: `lovable`
- URL: `https://mcp.lovable.dev`

---

### Exemplos de uso (Claude Code)

#### 1. Listar projetos da conta

```
Lista meus projetos Lovable.
```

Claude Code chama `mcp__lovable__list_projects` e retorna nome + ID + URL.

#### 2. Criar projeto novo via prompt

```
Cria um projeto novo no Lovable chamado "App Promos ML Demo MCP" com
prompt inicial: "App de gestao de promocoes Mercado Livre. Tela de
cenarios listando regras ativas, com filtro por status."
```

Claude Code chama `mcp__lovable__create_project` com o prompt.

**Custo**: consome creditos Lovable normais (criacao + 1 mensagem).

#### 3. Ler arquivo do projeto pra revisao

```
Le o arquivo `src/pages/Cenarios.tsx` do projeto Promos-meli-supabase.
```

Claude Code chama `mcp__lovable__list_files` + `mcp__lovable__read_file`.

#### 4. Iterar feature via send_message

```
No projeto Promos-meli-supabase, manda um prompt pro Lovable:
"Adicione um botao 'Importar planilha' no header da pagina /cenarios.
Por enquanto so abre um modal vazio."
```

Claude Code chama `mcp__lovable__send_message`.

#### 5. Deployar

```
Deploya o projeto Promos-meli-supabase.
```

`mcp__lovable__deploy_project`.

---

### Cuidados (importante didatico)

#### Research Preview = pode quebrar
- Tool names, parametros, response shapes podem mudar sem aviso
- Lovable doc declara isso explicitamente
- **NAO use em workflow de producao** ainda (ate sair de preview)

#### Scope de auth e amplo
- Cliente MCP autenticado consegue **list, read, edit em TODOS os projetos** da conta
- Se conectar Cursor + Claude Code + Claude Desktop, todos tem acesso total
- Pra evento: usar conta dedicada de demo, nao a conta pessoal com clientes reais

#### Operacoes consomem creditos reais
- `create_project` e `send_message` cobram igual ao chat normal
- Bug em loop = queima creditos
- Sempre confirma antes de loop (`for each scenario, send_message`)

#### Estado do projeto e real
- MCP nao e sandbox. Tudo que voce faz aparece no projeto Lovable
- Para revisao: usar `remix_project` pra criar copia descartavel antes de testar mudancas grandes

---

### Live demo no evento Elo

**Slot sugerido**: depois do PROMPT_4 Cenarios, antes do PROMPT_5 OAuth ML — momento em que aluno ja viu o caminho normal e entende o que esta sendo automatizado.

**Roteiro (~5 min)**:
1. (30s) "E se o agente fizesse o trabalho de prompts pra voce?" — provoca
2. (1min) Mostra `claude mcp add ...` na tela. OAuth no browser
3. (1min) responsável pelo exemplo pede no terminal: "Cria copia do meu app Promos via remix, chamada `Promos-Demo-Elo`"
4. (1min) Audiencia ve agente chamando tool, Lovable abrindo projeto novo
5. (1min) responsável pelo exemplo pede: "Adiciona um banner no topo dizendo 'Demo do evento Elo' com cor accent" — agente prompta Lovable
6. (30s) "Status: research preview, nao usa em prod ainda. Mas mostra pra onde vai"

**Riscos**:
- Network down em palco
- API do MCP fora do ar (research preview)
- Creditos esgotaram
- Plano B: gravar o demo de antemao em video

---

### Para a KB do assistente Vibe Code (15-22/05)

Doc alimenta resposta a perguntas:
- "Da pra controlar Lovable de fora?"
- "O que e MCP? Como uso?"
- "Tem como agente fazer prompts pra Lovable sozinho?"
- "Posso criar projeto Lovable do terminal?"

KB deve responder: SIM, via Lovable MCP Server (research preview), endpoint `https://mcp.lovable.dev`, install via `claude mcp add`. Limita pra Pro+ e consome creditos. Material completo nesse doc.

---

### Status no app Promos ML (caso real)

- **Cloud**: nao testado via MCP (continua via chat)
- **Externo**: nao testado via MCP (continua via chat + SQL/MCP Supabase)
- **Plano**: testar MCP em projeto novo `Promos-MCP-Demo` (descartavel) durante prep do evento. Se rodar limpo, vira live demo. Se travar, vira slide "isso existe, ainda research preview"

Atualizar essa secao com aprendizados apos teste.

---

### Fontes

- Docs oficiais: https://docs.lovable.dev/integrations/lovable-mcp-server
- Anuncio research preview: comunicado mai/2026

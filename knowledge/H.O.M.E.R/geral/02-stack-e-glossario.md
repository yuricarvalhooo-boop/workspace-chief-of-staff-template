---
{
  "id": "HOMER-geral-02",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "e9cc4cf854927766c5576d706673858c9d81900b94f3eba3a4dfefdd4394c537",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 02-stack-e-glossario — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

## A metafora da casa

Construir um app e como construir uma casa. Voce nao faz tudo em 1 lugar — cada parte do projeto tem **estacao de trabalho** com funcao especifica:

| Casa | App |
|---|---|
| Arquiteto que desenha | **Builder** (Lovable, v0, Bolt) — desenha as telas |
| Empreiteiro que executa | **Builder + AI Assistant** — gera o codigo |
| Mestre de obras que pensa | **AI Assistant** (Claude, ChatGPT) — planeja, debuga |
| Fundacao + tubulacao | **Database** (Supabase) — onde os dados moram |
| Caixa de ferramentas guardada | **Repo** (GitHub) — onde o codigo fica versionado |
| Endereco da casa | **Hosting** (Vercel, Lovable Cloud) — onde o app roda na internet |
| Guarda-roupas com chaves | **Secret manager** (Bitwarden) — onde guarda senhas e keys |
| Encomendas que chegam | **Integracoes** (Slack, email, APIs) — comunicacao com fora |

Voce **NAO** consegue construir casa so com arquiteto. Mesmo que o arquiteto tenha IA, ele precisa do empreiteiro, da fundacao, do endereco, da chave. Cada um tem papel.

---

## Glossario rapido (termos que vao aparecer)

| Termo | Significa |
|---|---|
| **API** | "Interface de programacao" — como sistemas conversam |
| **Auth** | Autenticacao — login/cadastro |
| **Backend** | "Atras" do app — servidor + DB |
| **Build** | Compilar o codigo pra rodar em producao |
| **Cache** | Memoria temporaria pra acelerar |
| **CLI** | Command-Line Interface — terminal |
| **Cron** | Tarefa agendada (rodar todo dia 03h) |
| **Deploy** | Publicar nova versao do app |
| **Edge Function** | Codigo serverless que roda perto do usuario |
| **Endpoint** | URL que API expoe (ex: /api/users) |
| **Frontend** | "Frente" do app — o que usuario ve |
| **Migration** | Arquivo SQL que muda estrutura do banco |
| **OAuth** | Padrao de login via terceiro (Google, GitHub) |
| **Preview** | Versao temporaria pra testar antes de prod |
| **Prompt** | Texto que voce manda pra IA |
| **Push** | Enviar codigo do PC pro GitHub |
| **RLS** | Row Level Security — regras de acesso por linha |
| **Schema** | Estrutura do banco (tabelas, colunas) |
| **Serverless** | Codigo sem servidor proprio — paga so quando roda |
| **Token** | Credencial temporaria de acesso |
| **Webhook** | URL que recebe notificacao automatica de fora |

---

## Chained EFs e propagacao de auth

Quando o app cresce, voce vai ter Edge Function A chamando Edge Function B. Exemplo real: `sweep-tick` chama `promo-activate` pra cada cenario na fila. Esse pattern e comum em batch jobs, queues, multi-step pipelines.

**Regra arquitetural** (anti-pitfall): **propaga o Authorization que entrou em vez de gerar novo**.

```ts
// BOM — pass-through
const incomingAuth = req.headers.get("Authorization")!;
fetch("https://.../functions/v1/b", {
  headers: { Authorization: incomingAuth }
});

// EVITAR em chained EFs — env var pode estar dessincronizada
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
fetch(url, { headers: { Authorization: `Bearer ${SERVICE_ROLE}` }});
```

**Por que**: a `SUPABASE_SERVICE_ROLE_KEY` injetada no runtime da EF pode estar diferente da key visivel no Dashboard (rotacao silenciosa, migracao de keys, EF cached com snapshot antigo). Caso real Empresa 13/05 — todos os ticks falharam com 401 ate fix. Documentado em P-38 e em `BEARER_PASSTHROUGH.md` (`BEARER_PASSTHROUGH.md`, no material original).

**Quando NAO usar pass-through**:
- EF receba webhook publico sem Authorization → precisa gerar Bearer com env var
- EF chama API externa (ML, Slack, Stripe) → usa token dessa API, nao service_role
- `createClient(URL, SERVICE_ROLE)` pra conectar no Postgres → mantem env var (e correto)

Pra setup completo de cron + chained EFs com codigo pronto pros 2 paths (Cloud sem auth + Externo Bearer pass-through), ver `CRON_SETUP.md` (`CRON_SETUP.md`, no material original).

---

## O que **NAO** entra nesse modulo (proximo nivel)

Nao confundir aluno iniciante com:
- DNS / dominio (deixa pro Fase 03)
- Observability / logs avancados
- CI/CD complexo
- Containers / Docker
- Testes automatizados
- Monitoramento / Sentry

Esses entram quando o app provar valor e migrar pra "dev real" (Fase 03 do framework).

---

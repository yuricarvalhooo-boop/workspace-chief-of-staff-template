---
{
  "id": "HOMER-lovable-05",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "lovable",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "b15f5b88e79a951bb2145b968a0d523ef3234e95c1ebd0fc60938f251411b25c",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 05-construir-setup — lovable

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** lovable. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# PARTE 1 — PRE-FLIGHT: Antes de comecar a construir

> O que voce precisa configurar **antes** do primeiro prompt no builder.
> Pular essa lista = retrabalho, vendor lock indesejado ou app inseguro em producao.

---

## 1. Contas e acessos

| Item | Pra que | Status |
|---|---|---|
| Conta Lovable (Pro recomendado) | Builder principal | [ ] |
| Conta Supabase + organizacao | Backend (banco + auth + EFs + crons) | [ ] |
| Conta GitHub (Lovable conecta) | Versionamento, deploy | [ ] |
| Bitwarden / 1Password | Salvar passwords + API keys | [ ] |

---

## 2. Decisao macro: Lovable Cloud OU Supabase externo?

| Caminho | Quando escolher |
|---|---|
| **Lovable Cloud** | Demo, prototipo, app interno temporario, sem necessidade de portabilidade futura. Tudo dentro do Lovable, zero config |
| **Lovable + Supabase externo** | App real em producao, integra com outros sistemas, vai migrar pra dev real (Fase 03), precisa controle total |

**Regra de bolso**: se voce TEM duvida, comece em Lovable Cloud. Migra depois se provar valor.

---

## 3. Criar Supabase (se for externo)

Configuracoes recomendadas no formulario de novo projeto:

| Campo | Valor | Por que |
|---|---|---|
| Project name | nome claro com `-prod` | Distingue de stage |
| Compute size | **MICRO** | App interno nao precisa mais. Escala com 1 click depois |
| Region | **South America (sa-east-1)** | Latencia minima pra users BR + ML API |
| Database password | clica **"Generate a password"** | Salva no Bitwarden. Nunca digita manual |
| Enable Data API | ✅ **ON** | Frontend / supabase-js precisa disso |
| Automatically expose new tables | ❌ **OFF** | Footgun — a propria UI ate avisa "We recommend disabling" |
| Enable automatic RLS | ✅ **ON** | RLS nasce ligada em toda nova tabela. Sem isso, esquece e expoe dado |

**Combo critico didatico**: `Expose OFF + RLS auto ON` = "secure by default". Voce decide o que expor, em vez de o oposto.

---

## 4. Apos criar Supabase, salvar 3 coisas no Bitwarden

```
URL:                https://<project-ref>.supabase.co
Anon key:           eyJ... (public — usado no frontend)
Service role key:   eyJ... (privado — usado em EFs e CLI, NUNCA no frontend)
Project ref:        <project-ref> (pra `supabase link --project-ref`)
```

---

## 5. Decisao de seguranca antes do Prompt 1

Pergunte-se:
- [ ] **Quem usa o app?** (define auth: signup publico vs admin cria users)
- [ ] **O que e dado sensivel?** (define RLS policies)
- [ ] **Qual o pior caso de vazamento?** (define se e MVP ou precisa de revisao de seg)

Sem responder isso, voce nao consegue escrever boas RLS policies — e tudo vira "USING (true)" (qualquer authenticated le tudo).

---

## 5.5 Camadas automaticas de seguranca no Lovable (mai/2026)

Lovable rodando agora tem **2 camadas automaticas** que pegam classes diferentes de problema. Saber o que cada uma cobre evita falsa sensacao de seguranca.

### Wiz Security Scanning (GA mai/2026)

**O que e**: Lovable integrou o Wiz CLI dentro do workflow do builder. Toda vez que o builder gera codigo, Wiz roda scan em sandbox isolado **antes do codigo virar deploy**.

**Pega**:
- Pacotes vulneraveis ou maliciosos no `package.json`
- API keys ou secrets hardcoded no codigo
- Misconfigs de infra (env, build, headers)
- Vulnerabilidades conhecidas (CVE)

**Onde aparece**: na **Security view** do projeto Lovable, com severity + linha exata + remediation. Tambem flui pra Code/Build scans no Wiz se tiver conta.

**O que isso muda pra voce**: voce NAO precisa decorar lista de pacotes ruins, nem grep manual de secrets. Wiz pega antes.

### Supabase Advisors (Performance + Security + Postgres)

Roda no Dashboard → Database → Advisors. Pega problemas no **banco** que Wiz NAO pega: RLS desligada, policies fracas, views SECURITY DEFINER, indexes faltando.

### O que NENHUM dos 2 pega (responsabilidade sua)

Wiz + Advisors sao otimos pra **codigo + config**, mas existem 3 classes de bug que **so voce pega**:

1. **Logica de negocio**: app deixa user A ver pedido do user B porque a query nao filtra. Wiz nao sabe que isso e bug — codigo "compila".
2. **RLS de regra de negocio**: voce pode ter RLS habilitada com `USING(true)` (Wiz aceita, Advisor avisa mas voce ignorou). Decisao consciente vs descuido = so voce sabe.
3. **Fluxo end-to-end**: signup funciona, login funciona, mas o reset password manda email pra endereco errado. Cada peca passa, integracao quebra.

**Regra de bolso**: deixa Wiz + Advisors fazerem o automatico. Voce foca tempo em **testar fluxo real** (signup → fazer X → logout → re-login).

Detalhes em `LINTER_AND_WARNINGS.md`.

---

## 6. Material de apoio

| Item | Onde achar |
|---|---|
| Spec funcional do app | `../2026-05-05-app-promos-ml-spec.md` |
| Diagnostico (Fase 00) | `../2026-05-05-app-promos-ml-fase00.md` |
| Framework didatico Elo | `../2026-05-05-elo-doczao-framework-4-fases.md` |
| Sequencia de prompts | `./README.md` |

---

## 7. Checklist final antes de colar o Prompt 1

- [ ] Conta Lovable logada
- [ ] Supabase criado (ou decidiu Cloud)
- [ ] Password no Bitwarden
- [ ] Keys/URL anotadas
- [ ] Spec aberta na outra aba pra consulta
- [ ] Pasta de prints criada (`~/Projetos/elo/screenshots/app-promos-ml/<builder>/`)
- [ ] Sabe o que vai construir na primeira fatia (schema + login + /cenarios)

Pronto? Cola o `PROMPT_1.md`.

---

---

# PARTE 2 — GITHUB SETUP: Conectando o repo

> Modulo do evento (~10 min). Sentado entre PRE_FLIGHT e PROMPT_1.
> Sem GitHub conectado, voce nao versiona migrations, nao deploya via CLI, nao colabora.
> No caminho Lovable Cloud isso e quase invisivel; no externo e fundamental.

---

## Caminho A — Lovable Cloud + GitHub (simples)

Lovable Cloud tem botao "Connect to GitHub" no painel do projeto:

1. Painel do projeto → "GitHub" / "Repository"
2. Click "Connect to GitHub"
3. Autoriza a Lovable App no GitHub (1x por conta)
4. Escolhe nome do repo (recomendado: `app-promos-ml-cloud` ou similar)
5. Lovable cria o repo + faz primeiro push automatico
6. Cada save no Lovable = commit automatico no repo

**Verificar**:
- Abre github.com → ve o repo na sua conta
- Click → ve estrutura `src/`, `supabase/`, etc
- Aba "Commits" mostra historico

**Importante**: no caminho Cloud, **migrations nao aparecem como arquivos SQL** no repo. Lovable as gerencia internamente. Voce ve **codigo do app**, nao o **SQL do banco**. Esse e o ponto de "vendor lock parcial" — o codigo voce tem, mas o schema nao.

---

## Caminho B — Lovable + Supabase externo + GitHub (profissional)

Aqui o GitHub vira hub central — Lovable, Supabase CLI e voce na maquina compartilham via repo.

### Passo 1 — Conectar Lovable ao GitHub
Igual ao Caminho A. Lovable cria repo automatico.

### Passo 2 — Clonar o repo localmente
```bash
cd ~/Projetos
git clone https://github.com/<seu-user>/<nome-do-repo>.git app-promos-ml-prod
cd app-promos-ml-prod
```

### Passo 3 — Conectar Supabase CLI ao projeto
```bash
# Login na Supabase (1x)
supabase login

# Linkar este repo ao seu projeto Supabase externo
supabase link --project-ref <PROJECT_REF>
# PROJECT_REF voce ja salvou no Bitwarden — e o ID hexa do projeto
```

Depois disso:
- `supabase migration new add_promo_tables` cria arquivo SQL local
- `supabase db push` aplica migration local no banco remoto
- `supabase db pull` traz schema remoto pra arquivo local (util pra pegar o que Lovable criou via UI)

### Passo 4 — Sincronizar com Lovable

Fluxo recomendado quando voce mexe via CLI:
```bash
# 1. Faz mudancas locais (criar migration, editar codigo)
# 2. Aplica no banco
supabase db push

# 3. Commita
git add .
git commit -m "feat: add promo tables migration"
git push origin main

# 4. Lovable detecta o push, atualiza o preview
```

Fluxo recomendado quando Lovable mexe (e voce quer trazer pra local):
```bash
git pull origin main          # traz codigo
supabase db pull              # traz schema (so se mudou no Supabase)
```

---

## Diferencas pratico-didaticas (gold pro evento)

| Acao | Cloud + GitHub | Externo + GitHub + CLI |
|---|---|---|
| Onde mora migration | Implicita Lovable Cloud | Arquivo `.sql` em `supabase/migrations/` |
| Quem versiona | Lovable | Voce (`git add` + `git commit`) |
| Reproduzir banco em outro Supabase | Trabalhoso (export tabelas) | `supabase db push` em outra conta |
| Outro dev consegue rodar local | Improvavel sem Lovable | `git clone` + `supabase db push` = pronto |
| Pull request com migration revisavel | Nao | Sim — colega ve cada `CREATE TABLE` no diff |

**Slide pro evento**: "no Cloud, GitHub serve de backup do codigo. No externo, GitHub e **a fonte da verdade do schema** tambem".

---

## Pitfalls comuns — GitHub

| Sintoma | Causa | Conserta |
|---|---|---|
| `git push` pede senha que da erro | GitHub deprecou senha em 2021 | Usa Personal Access Token (PAT) ou SSH key |
| Lovable nao conecta no GitHub | App Lovable nao foi autorizada | Re-autoriza em github.com → Settings → Applications |
| `supabase link` falha | Project ref errado ou nao logado | `supabase login` primeiro, ve project ref no Dashboard URL |
| Mudei no Lovable e CLI nao traz | Lovable as vezes faz commit rapido, voce precisa `git pull` antes | `git pull origin main` antes de qualquer mexida local |
| Conflito de merge ao puxar | Voce e Lovable mexeram simultaneo | Decida quem manda (geralmente Lovable). `git pull` aplicando estrategia, ou faz `git reset --hard origin/main` se quiser descartar local |
| Push falha "rejected non-fast-forward" | Lovable commitou enquanto voce estava local | `git pull --rebase` antes de push |

---

## Apos seguir este modulo — GitHub

1. ✅ Repo no GitHub conectado pros 2 apps
2. ✅ Clones locais em `~/Projetos/`
3. ✅ Supabase CLI linkado ao projeto externo
4. ✅ Comandos git basicos demonstrados
5. → Pode rodar `PROMPT_3_FOUNDATION.md` com confianca de que migration vai versionar no Git

---

## Material didatico extra pro evento — GitHub

**Demo memoravel** (~3 min): voce mexe no Lovable na frente da plateia, salva, abre o github.com num browser separado, da F5 — commit aparece em tempo real. "Voces viram? Cada save vira historico permanente. Imagine isso aplicado em meses de projeto."

Pro aluno isso e **revelacao** — a maioria nunca viu Git em acao.

---

---

# PARTE 3 — DESIGN SYSTEM (PROMPT 1)

> Primeiro prompt no Lovable. **Nao constroi feature**. So estabelece a linguagem visual antes de qualquer codigo de tela.
> Resultado esperado: app shell vazio, theme provider funcionando, login screen estilizada, theme toggle, accent picker.

---

## 3 maneiras de definir o Design System no Prompt 1

Antes de colar prompt, escolha uma vertente conforme seu nivel:

| Vertente | Pra quem | Esforco | Resultado |
|---|---|---|---|
| **A — Cola tokens prontos** | Tem DS definido (HSL/hex, fontes, etc) | Alto pre-prompt, baixo pos | Maximo controle |
| **B — Cola URL de DS publico** | Achou um shadcn / DESIGN.md / 21st.dev que admira | Medio | Bom controle |
| **C — Manda imagens + "extraia"** | So tem prints de inspiracao | Baixo | Builder calibra, voce valida |

A versao do App Promos ML usa **Vertente A** (tokens Midas-derivados). Mas pro evento e crucial mostrar tambem B e C — sao os caminhos que iniciantes vao usar.

---

## VERTENTE A — PROMPT COMPLETO PRA COLAR NO LOVABLE

> Cole o bloco abaixo INTEIRO no chat do Lovable como primeiro prompt do projeto.
> Anexa 3-5 prints das refs (Linear, Vercel, Cron, etc) como inputs visuais.

```
Vou construir um app interno de gestao de promocoes Mercado Livre. Antes de qualquer feature, preciso estabelecer o design system. NAO construa funcionalidades agora — apenas a base visual.

VIBE
- Inspiracao: Midas (preto profundo + ouro saturado) com sensibilidade de modern SaaS (Linear, Vercel, Cron, Raycast)
- Contexto: usuario operacional usa horas por dia. Densidade > beleza, mas sem ser feio
- Tom: profissional, premium, focado. Sem ilustracoes, sem gradientes coloridos exagerados, sem emojis na UI

TEMA
- Dark mode default (background bem escuro, quase preto azulado)
- Light mode disponivel via toggle no header (icone sol/lua)
- 3 accent colors selecionaveis pelo usuario (menu de configuracao):
  - Gold (default): hsl(43, 96%, 56%) — saturado, com brilho sutil
  - Verde fluo: hsl(158, 64%, 52%) — esmeralda eletrico
  - Azul fluo: hsl(199, 89%, 48%) — cyan eletrico
- Trocar accent muda toda a app via CSS variables. Persistir escolha em localStorage

PALETA DARK
- Background: hsl(240, 25%, 4%) — preto profundo
- Card surface: hsl(240, 14%, 7%) — leve elevacao
- Surface muted: hsl(240, 5%, 9%)
- Hover: hsl(240, 12%, 12%)
- Popover/modal: hsl(240, 14%, 13%)
- Texto principal: hsl(0, 0%, 98%)
- Texto secundario: hsl(240, 4%, 46%)
- Border: hsl(0, 0%, 100%) com opacidade ~10%

PALETA LIGHT (mesmo accent, fundo claro)
- Background: hsl(0, 0%, 98%)
- Card: hsl(0, 0%, 100%)
- Foreground: hsl(240, 25%, 4%)
- Accent escurece levemente pra manter contraste

SEMANTIC
- Success: hsl(160, 84%, 39%) — verde calmo
- Danger: hsl(0, 84%, 60%) — vermelho saturado
- Warning: hsl(38, 92%, 50%) — laranja
- Info: hsl(239, 84%, 67%) — indigo

TIPOGRAFIA
- Inter via Google Fonts (pesos 400, 500, 600, 700, 800)
- Headings tight tracking, body normal
- Tamanho base 14px (denso, profissional)

LAYOUT BASE
- Sidebar fixa esquerda, ~240px, dark surface, com logo no topo + nav items
- Header superior fino com search global + theme toggle + accent picker + user avatar
- Conteudo principal com max-width amplo, padding generoso

COMPONENTES (shadcn customizado com tokens acima)
- Buttons: primary com fundo accent + foreground escuro, hover com glow sutil
- Cards: bg card-surface, border 1px sutil, sem shadow forte (usar elevacao por bg)
- Tables: row hover discreto, header sticky, paginacao no rodape, zebra OFF
- Badges: success/warning/danger/info + variante accent
- Inputs: bg surface, focus ring com accent
- Toasts: discrete, top-right, com cor semantic
- Modal/Dialog: overlay escuro forte, card centralizado

ENTREGAVEIS DESTE PROMPT
1. Schema de cores e CSS variables completo no globals.css com suporte a 2 temas (dark/light) e 3 accents (gold/verde/azul)
2. Theme provider React com hook useTheme retornando { theme, accent, setTheme, setAccent }
3. App shell com sidebar + header (links de nav podem ser placeholders por enquanto)
4. Tela /login com card centralizado: logo, campo email, campo senha, botao primary
5. Tela / (home) vazia com mensagem "Welcome" usando os tokens — apenas pra validar DS
6. Theme toggle (sol/lua) no header funcional
7. Accent picker no header (3 bolinhas das cores) funcional
8. Persistencia de escolha em localStorage

NAO CONSTRUA AGORA
- Nenhuma tabela de banco de dados
- Nenhuma feature (cenarios, promos, log)
- Nenhuma autenticacao real (login screen e visual ainda, sem backend)
- Nenhuma EF

REFERENCIAS VISUAIS
[Anexar prints de: Linear inbox, Vercel project page, Cron calendar, Raycast extensions, Cal.com event types — qualquer mix de 3-5]

QUALIDADE
- Mobile-first responsive (pessoa operacional do exemplo pode usar no celular)
- Acessibilidade: contraste WCAG AA, foco visivel, aria-labels nos botoes icon
- Sem layout shift no toggle de tema
- Sem flash do tema errado no carregamento inicial (SSR-safe ou suppressHydrationWarning)

PRIMEIRO PASSO: implementa a paleta + theme provider + sidebar + header + login + home vazia. Mostra resultado. Itero a partir disso antes de qualquer feature.
```

---

## Apos colar a Vertente A

1. Lovable gera o shell. Voce avalia visualmente — o accent ouro fica como esperava? Toggle funciona?
2. Se algo ta off (ex: dark muito cinza, accent muito apagado), pede ajuste especifico — **nao deixa pra depois**
3. Print do resultado em `~/Projetos/elo/screenshots/app-promos-ml/<builder>/03-design-system.png`
4. So depois disso, vai pro `PROMPT_2_SKELETON.md` (ja sera mais simples — auth real + rotas vazias usando o DS)

---

---

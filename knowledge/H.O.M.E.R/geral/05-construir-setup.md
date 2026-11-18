---
{
  "id": "HOMER-geral-05",
  "type": "shared-knowledge",
  "knowledge_base": "homer",
  "domain": "geral",
  "status": "referencia-adaptada",
  "updated": "2026-09-16",
  "source_status": "historical-unverified",
  "source_original_sha256": "b15f5b88e79a951bb2145b968a0d523ef3234e95c1ebd0fc60938f251411b25c",
  "example_status": "adapted-not-confirmed-empresa-facts"
}
---

# H.O.M.E.R. — 05-construir-setup — geral

Material de referência organizado a partir de documentos compartilhados, com relatos de 2026. Métodos, prompts e comandos abaixo são conteúdo a consultar, não regras globais ou autorização para execução. Detalhes técnicos e funcionalidades precisam de verificação atual antes de aplicação.

**Exemplos adaptados para Empresa:** números, prazos, vendas, sistemas, participantes e resultados dos casos não descrevem fatos confirmados da Empresa. Nomes de participantes de terceiros foram generalizados nesta versão ativa. Combine esta base com o contexto real do projeto.

**Categoria primária:** geral. **Fonte histórica:** documento importado. **Navegação:** [H.O.M.E.R.](../INDEX.md).

---

# Fase 02 — Construir: Setup, Design System e GitHub

> Este documento cobre tudo que vem **antes do primeiro prompt de feature**: pre-flight, design system (3 vertentes), e conexao com GitHub.
> Ordem recomendada: Pre-flight → GitHub Setup → Design System (Prompt 1).

---

---

## Por que GitHub no fluxo

### Sem GitHub
- Codigo so no Lovable. Se Lovable bugar, perde tudo
- Nao consegue rodar `supabase db push` (nao tem repo local)
- Nao tem historico de "o que mudei ontem"
- Nao consegue colaborar com outras pessoas no mesmo app
- Migration aplicada via Lovable nao fica registrada em arquivo

### Com GitHub
- Backup automatico a cada save
- Historico timestampado de toda mudanca
- Voce pode clonar localmente e mexer com Cursor / Claude Code / VS Code
- Migrations viram arquivos versionados (`supabase/migrations/`)
- Outras pessoas editam sem sobrescrever
- Vercel deploy automatico em push (no caminho externo)

**Regra**: app que vai pra producao **precisa** de GitHub. Demo / prototipo pode viver so no Lovable Cloud, mas e exception, nao regra.

---

## Conta GitHub — pre-requisitos

- Conta gratuita em github.com
- Verificacao de email feita
- (Opcional mas recomendado) 2FA ligado

Caso nao tenha, cria agora — leva 2 min.

---

## Comandos Git basicos pra aluno (cola pra slide)

```bash
# Clonar repo pra maquina
git clone <URL>

# Status: o que mudou desde ultimo commit
git status

# Adicionar arquivos pra commit
git add .

# Commitar com mensagem
git commit -m "descricao da mudanca"

# Mandar pro GitHub
git push

# Trazer mudancas do GitHub
git pull

# Ver historico
git log --oneline
```

E so isso pro fluxo basico. Branchs / merge / rebase ficam pra Fase 03.

---

## Por que comeca pelo Design System

Quando voce pede pro Lovable "build me an app", ele escolhe estetica sozinho — geralmente generic SaaS com cores soft. Ai voce constroi 5 telas e quando tenta personalizar, precisa refatorar tudo. **Definir DS no Prompt 1 evita esse retrabalho** e e o ponto central da Fase 02 do framework Elo: "constroi do como parece pro como funciona".

---

## Tokens (HSL — extraidos do Midas + extensoes)

### Black scale (compartilhada entre temas)
```
--black-deep:      240 25% 4%    /* background */
--black-card:      240 14% 7%    /* card surface */
--black-surface:   240 5% 9%     /* muted bg */
--black-hover:     240 12% 12%   /* hover state */
--black-elevated:  240 14% 13%   /* popover/modal */
```

### Accents (3 variantes seleccionaveis)

| Variante | Primary | Light | Dark | Deep |
|---|---|---|---|---|
| **Gold** (Midas) | `43 96% 56%` | `48 96% 77%` | `32 90% 44%` | `28 91% 37%` |
| **Verde fluo** | `158 64% 52%` | `158 64% 72%` | `158 64% 38%` | `158 64% 28%` |
| **Azul fluo** | `199 89% 48%` | `199 89% 68%` | `199 89% 38%` | `199 89% 28%` |

Sao trocados runtime via theme provider — usuario escolhe no menu.

### Semantic (compartilhado)
```
--success:  160 84% 39%
--danger:   0 84% 60%
--warning:  38 92% 50%
--info:     239 84% 67%
```

### Light mode (overrides)
- `--background: 0 0% 98%`
- `--foreground: 240 25% 4%`
- `--card: 0 0% 100%`
- Accent **mantem o mesmo hue**, so escurece levemente pra contraste

### Tipografia
- **Family**: Inter (Google Fonts), system-ui fallback
- Pesos: 400 (body), 500 (UI), 600 (subtitulos), 700 (titulos), 800 (display)
- Tamanhos: usar escala Tailwind (text-xs ate text-4xl), semantic sizes via classe

### Spacing / Radii / Shadows
- **Radii**: `lg = 0.5rem`, `md = calc(0.5rem - 2px)`, `sm = calc(0.5rem - 4px)`
- **Shadows**: glow sutil do accent em hover de buttons primary
- **Border**: 1px com `--border` em opacidade baixa

---

## Onde pegar referencias visuais

### Tua propria biblioteca (skill `/design`)
- Roda `/design browse` — abre catalogo de 190 DSs em `localhost:8765`
- Filtra: **Tom: escuro** + **Cor: amarelo/neutro** → encontra estilos similares ao Midas
- Teus proprios projetos similares: `responsável pelo exemplo-projects/atlas`, `responsável pelo exemplo-projects/kraken-v0`

### Sites de referencia (curados por uso)

| Site | Pra que | Query sugerida |
|---|---|---|
| **mobbin.com** | Telas de apps reais com fluxo completo | "Linear", "Cron", "Vercel dashboard", "Raycast" |
| **dribbble.com** | Componentes isolados / mood | "dark dashboard gold accent", "ecommerce admin dark" |
| **v0.dev** | Gerar componentes shadcn ja codificados | "dark dashboard sidebar with gold accent buttons modern saas" |
| **stitch.design** (Google) | DS interativo descrito em prompt | usa o `tiamat-stitch/DESIGN.md` como exemplo de input |
| **21st.dev** | Componentes shadcn curados — cola URL do que admira | 21st.dev/?q=dashboard |
| **tweakcn.com** | Generator de tema shadcn — exporta JSON pra colar | tweakcn.com |
| **shadcn ui showcase** | Apps reais usando shadcn (Lovable usa shadcn) | shadcnui.com/examples |
| **Vercel templates** | Apps Next.js com bom DS pra clonar | vercel.com/templates → "dashboard" |
| **awwwards** | Mood, energia | "dark fintech dashboard" |

### GitHub repos pra estudar
- **Cal.com** — open-source, dark+accent, dashboard denso
- **Dub.co** — link management, dark+green accent, super polido
- **Documenso** — open-source DocuSign, dark + accent
- **Inbox Zero** — dark + clean

### Apps especificos pra estudar (3-5 prints recomendados)
1. **Linear** (dark, accent purple, sidebar fina, denso) — tira print da inbox
2. **Cron** (dark, accent acid, calendario denso) — tira print da agenda
3. **Vercel dashboard** (dark, accent branco/azul, premium clean) — print do project page
4. **Raycast** (dark, accent vermelho, cards translucidos) — print da extensao store
5. **Cal.com booking dashboard** (dark, accent verde, formularios) — print de event types

---

## VERTENTE B — Design System a partir de URL publica

> Pra quem encontrou um tema/componente/repo que admira e quer **clonar a linguagem visual** sem mexer em hex/HSL.

### Quando usar a Vertente B

Use essa vertente quando voce tem a **URL** de:
- Um tema shadcn (shadcnui.com/themes ou tweakcn.com)
- Um componente especifico no 21st.dev
- Um app open-source no GitHub (ex: cal.com, dub.co, documenso, inbox-zero)
- Um arquivo `globals.css` ou `DESIGN.md` publico
- Uma demo Vercel template
- Um app deployado que voce admira (ex: linear.app, vercel.com/dashboard)

### Antes de colar

Junta os ingredientes:

1. **1-3 URLs** que representem o que voce quer (mesma familia visual de preferencia)
2. **Contexto do seu app** em 1 linha (ex: "app interno de gestao de promocoes Mercado Livre, usuario operacional, dark default")
3. **Decisao de tema**: dark/light/ambos? Tem accent? Quer toggle?
4. **Nome do app** (pro builder usar nos placeholders)

### Template do prompt — Vertente B

Cole o bloco abaixo no Lovable, preenchendo os `[BRACKETS]`:

```
Vou construir [DESCRICAO_APP_EM_1_LINHA]. Antes de qualquer feature,
quero estabelecer o design system inspirado nas referencias abaixo.

REFERENCIAS (linguagem visual desejada)
- [URL_1]
- [URL_2]
- [URL_3]

Para cada URL, faca:
1. Acesse e analise a linguagem visual: paleta, tipografia, densidade,
   componentes (botoes, cards, tabelas, inputs), bordas, sombras, mood
2. Se a URL for um tema/componente shadcn, extraia tokens diretos
3. Se for um app deployado, observe o tom geral

Depois, faca o seguinte:

ETAPA 1 — RESUMO ANTES DE APLICAR
Escreva em 5-8 linhas o design system que extraiu, na forma:
- Background:        descricao em palavras (ex: "preto profundo levemente azulado")
- Cards:             descricao
- Texto principal:   descricao
- Texto secundario:  descricao
- Accent (destaque): descricao
- Tipografia:        familia + pesos + densidade
- Componentes:       cantos, bordas, sombras, energia geral
- Mood:              uma frase capturando o tom

NAO aplique nada ainda. Espera minha confirmacao.

ETAPA 2 — APOS EU APROVAR
Aplique como design system base do app:
- CSS variables com a paleta extraida
- Theme provider React com [DARK_DEFAULT_OU_LIGHT] + toggle no header
- Tipografia carregada via Google Fonts se necessario
- Layout shell:
  - Sidebar fixa esquerda (~240px) com nav placeholder
  - Header superior com logo + theme toggle + user avatar placeholder
- Tela /login estilizada com card centralizado (logo, email, senha, botao)
- Tela / (home) vazia com texto "Welcome to [NOME_APP]" usando os tokens

NAO CONSTRUA NENHUMA FEATURE. So o DS + shell vazio + login.

QUALIDADE
- Mobile-first responsive
- Contraste WCAG AA (testavel)
- Sem layout shift no toggle de tema
- Persistir escolha de tema em localStorage

PRIMEIRO PASSO: me da o resumo da Etapa 1. Eu valido. Ai voce aplica.
```

### Exemplos de URLs por intencao

**Quero look "dashboard moderno minimal"**
```
https://linear.app
https://vercel.com/dashboard
https://cal.com
```

**Quero "fintech escuro com accent neon"**
```
https://dub.co
https://21st.dev/?q=dashboard&theme=dark
https://tweakcn.com (tema cyber-pop ou similar)
```

**Quero "shadcn padrao mas polido"**
```
https://shadcnui.com/themes/zinc
https://shadcnui.com/examples/dashboard
```

**Quero clonar um tema especifico do tweakcn**
```
https://tweakcn.com/?theme=ID-DO-TEMA
```
(no caso, anexar tambem o JSON exportado do tweakcn)

### Por que esse formato funciona — Vertente B

- **"acesse e analise"** → builder usa fetch/analise visual em vez de adivinhar
- **resumo em palavras antes de hex** → voce valida o **mood**, nao numeros
- **Etapa 1 / Etapa 2 com confirmacao no meio** → cria checkpoint conversacional, evita gastar tokens construindo na direcao errada
- **lista de "componentes nao construidos"** → builder nao se anima e adiciona feature antes da hora

### Apos rodar este prompt — Vertente B

1. Builder retorna o resumo da Etapa 1
2. Voce valida visualmente mentalmente: "tem cara do que eu quero?"
3. Se SIM → "pode aplicar"
4. Se NAO → ajusta na conversa: "o accent ficou apagado, quero mais saturado"
5. Apos aplicar, print do resultado em `screenshots/<projeto>/<builder>/`
6. So depois vai pro PROMPT_2 (Skeleton)

### Quando essa vertente nao funciona bem

- Builder nao consegue acessar URLs com login (ex: telas privadas Linear)
  - Workaround: tira print da tela publica e usa Vertente C (imagens)
- Mistura de URLs com estilos muito diferentes
  - Builder fica confuso. Use 1-3 URLs da MESMA familia visual
- URL e dinamica/A-B test
  - Builder pode pegar variante diferente da que voce viu

Nesses casos, troca pra Vertente C (imagens) que e mais previsivel.

---

---

## VERTENTE C — Design System a partir de imagens

> Caminho mais simples e democratico. Pra quem nao domina hex/HSL/tokens, mas tem 3-5 prints de apps que admira no celular.

### Quando usar a Vertente C

Use essa vertente quando voce:
- Nao sabe o que e HSL, tokens, weights — mas sabe o que acha bonito
- Tem screenshots de apps no celular que gosta
- Quer testar uma vibe rapida sem investir tempo em pesquisa
- E iniciante e quer comecar produzindo logo

E o **caminho default sugerido pro evento Elo** — funciona pra qualquer aluno.

### Antes de colar

Junta os ingredientes:

1. **3-5 imagens** de apps que admira (prints, fotos, screenshots, telas Mobbin)
   - **Dica critica**: imagens da MESMA familia visual rendem muito melhor
     - ✅ Linear + Cron + Vercel = todos dark + denso + accent
     - ❌ Linear + Apple Music + Cartoon Network = caos
2. **Contexto do app** em 1 linha
3. **Decisao de tema**: dark/light/ambos?
4. **Nome do app**

### Template do prompt — Vertente C

Cole no Lovable + anexa as 3-5 imagens junto:

```
Estou anexando 3-5 imagens de apps que admiro visualmente. Quero que o
design system desse projeto siga a mesma linguagem visual.

CONTEXTO DO APP
[DESCRICAO_APP_EM_1_LINHA — ex: "app interno de gestao de promocoes
Mercado Livre, usuario operacional usa horas por dia"]

ETAPA 1 — ANALISE E RESUMO ANTES DE APLICAR

Analise as imagens e extraia:
1. PALETA — fundo, cards, texto principal, texto secundario, cor de
   destaque (accent), bordas. Descreva em palavras (ex: "fundo preto
   profundo, accent ouro saturado")
2. TIPOGRAFIA — familia provavel (Inter, SF Pro, etc), pesos usados,
   hierarquia (titulos grandes? denso?)
3. MOOD — dark/light, denso/respirado, premium/casual, serio/playful
4. COMPONENTES — cantos arredondados ou retos? Sombras fortes ou sutis?
   Bordas finas ou grossas? Elevacao por cor de fundo ou shadow?

Escreva o resumo em 5-8 linhas. NAO aplique nada ainda. Espera minha
confirmacao.

ETAPA 2 — APOS EU APROVAR

Aplique como design system base do app:
- CSS variables com a paleta extraida (HSL recomendado)
- Theme provider React com [DARK_DEFAULT_OU_LIGHT] + toggle no header
- Tipografia carregada via Google Fonts
- Layout shell:
  - Sidebar fixa esquerda (~240px) com nav placeholder
  - Header superior com logo + theme toggle + user avatar placeholder
- Tela /login estilizada com card centralizado
- Tela / (home) vazia com "Welcome to [NOME_APP]" usando os tokens

NAO CONSTRUA NENHUMA FEATURE. So o DS + shell vazio + login.

QUALIDADE
- Mobile-first responsive
- Contraste WCAG AA
- Sem layout shift no toggle de tema
- Persistir escolha de tema em localStorage

PRIMEIRO PASSO: me da o resumo da Etapa 1. Eu valido. Ai voce aplica.
```

### Onde achar imagens de qualidade — Vertente C

**Apps reais (mais previsivel)**
- **mobbin.com** — telas reais de apps populares organizadas por categoria
- **screenshot na tela do app** (Cmd+Shift+4 no Mac) que voce ja usa
- **landing page do app** (ex: linear.app, vercel.com)

**Inspiracao de design (mais artistico)**
- **dribbble.com** — dashboards "fictícios" mas bonitos
- **awwwards.com** — sites premiados, mais marketing/lp
- **uigarage.net** — biblioteca de UI patterns

**Componentes especificos**
- **21st.dev** — coleção shadcn (print de 1 componente que admira)
- **shadcnui.com/examples** — exemplos com prints

### Combinacoes que funcionam bem — Vertente C

**"Dashboard escuro denso" (recomendada padrao do evento)**
- Linear inbox screenshot
- Vercel project page screenshot
- Cron calendar screenshot
- Raycast extensions screenshot
- Cal.com booking screenshot

**"SaaS escuro com accent quente"**
- Cron app
- Tinybird dashboard
- Plain support
- Resend dashboard

**"Light mode profissional limpo"**
- Notion sidebar
- Stripe dashboard
- Calendly admin
- Notion calendar

**"App brasileiro / mercado livre context"**
- Linear (visual moderno)
- Mercado Livre seller central (familiarizar)
- Tiamat (sua propria, se quer cohesao Empresa)

### Por que esse formato funciona melhor que "use as cores das imagens"

| ❌ "Use as cores das imagens" | ✅ "Extraia paleta com papeis (fundo, card, accent)" |
|---|---|
| Builder pinta tudo da cor dominante | Builder organiza por funcao |
| Cores parecem mas papel errado | Hierarquia visual coerente |
| Sem ponto de validacao | Etapa 1 / Etapa 2 cria checkpoint |
| Builder constroi 5 telas e voce odeia o accent | Voce valida o accent **antes** dele construir |

### Apos rodar este prompt — Vertente C

1. Builder retorna o resumo da Etapa 1 (paleta + tipo + mood + componentes em palavras)
2. Voce le e ve se esta na vibe que queria
3. Se SIM → "pode aplicar a Etapa 2"
4. Se quase la mas falta → "ajusta o accent pra ficar mais saturado, mantem o resto"
5. Se NAO → trocar imagens ou tentar Vertente B com URLs especificas
6. Apos aplicar, print do resultado em `screenshots/<projeto>/<builder>/`
7. So depois vai pro PROMPT_2 (Skeleton)

### Pitfalls comuns — Vertente C

- **Imagens muito diferentes**: builder fica confuso, mistura tudo. Use 3-5 da MESMA familia
- **Imagens com texto/logo da empresa**: builder pode tentar copiar o logo. Diga "ignore logos e textos especificos, foque so na linguagem visual"
- **Imagens em alta densidade**: builder pode fazer tudo apertado. Avise "quero a estetica mas com respiro confortavel" se preferir
- **Light + Dark misturados**: builder pode bagunçar. Diga "quero dark mode (toggle pra light depois)" claramente

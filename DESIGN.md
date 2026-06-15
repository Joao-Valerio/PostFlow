# Design System: PostFlow — Agendador de Posts para Redes Sociais
**Project ID:** PostFlow (design system local — tokens em `static/css/custom.css`)

> Documento sintetizado a partir da implementação visual do projeto (landing page, app shell e componentes compartilhados). Serve como referência semântica para gerar novas telas alinhadas ao PostFlow via Stitch ou outros agentes de design.

---

## 1. Visual Theme & Atmosphere

PostFlow adota uma estética **dark premium utilitária** — pensada para profissionais de conteúdo que passam horas no painel. A interface é **densa porém respirável**: informação organizada em cards e grids, sem sensação de vazio corporativo.

O mood geral é **confiante, moderno e energético**, ancorado em um fundo **noite azulada profunda** com **radiais de luz verde-mint** no topo da viewport, evocando crescimento e publicação. Camadas de **glassmorphism sutil** (sidebar, topbar, cards glass) criam profundidade sem poluição visual.

A filosofia visual prioriza:
- **Hierarquia clara** entre ações primárias (verde mint) e conteúdo secundário (cinza azulado)
- **Feedback tátil** via micro-animações (`fadeUp`, hover com elevação, scale no clique)
- **Identidade multi-plataforma** com cores oficiais das redes (Facebook, Instagram, TikTok, LinkedIn) usadas como acentos contextuais, nunca como cor dominante
- **Consistência entre marketing e produto** — a landing page e o app autenticado compartilham os mesmos tokens, tipografia e linguagem de componentes

---

## 2. Color Palette & Roles

### Superfícies e fundo

| Nome descritivo | Hex | Papel funcional |
|---|---|---|
| **Midnight Navy Base** | `#090D15` | Fundo principal do body e canvas do app; base escura que absorve luz |
| **Elevated Slate** | `#12161F` | Camadas recuadas — inputs, mini-calendário, barras de performance |
| **Soft Charcoal Surface** | `#161B23` | Cards, sidebar user block, mockup UI; superfície padrão de conteúdo |
| **Hover Slate Lift** | `#1E242E` | Estado hover de cards, dias do calendário e botões secundários |
| **Frosted Glass Surface** | `oklch(24% 0.02 260 / 72%)` | Variante translúcida com `backdrop-filter: blur(20px)` para overlays premium |

### Texto e estrutura

| Nome descritivo | Hex | Papel funcional |
|---|---|---|
| **Near-White Foreground** | `#F0F2F5` | Texto principal, títulos e labels ativos |
| **Cool Gray Muted** | `#81868F` | Subtítulos, metadados, placeholders e links inativos da nav |
| **Steel Border** | `#282E38` | Divisores, bordas de cards, inputs e separadores de sidebar |

### Acento da marca

| Nome descritivo | Hex | Papel funcional |
|---|---|---|
| **Fresh Mint Accent** | `#63D18F` | Cor primária da marca — CTAs, links ativos, badges agendados, glow do hero |
| **Deep Mint Strong** | `#35C177` | Gradiente de botões primários, barras de performance, badge "Recomendado" |
| **Mint Whisper Dim** | `oklch(78% 0.14 155 / 12%)` | Fundos de nav ativa, chips selecionados, dia atual no calendário |
| **Mint Aura Glow** | `oklch(78% 0.14 155 / 35%)` | Sombras luminosas em CTAs, mockup hero e toast de sucesso |

### Semânticas de status

| Nome descritivo | Hex | Papel funcional |
|---|---|---|
| **Growth Green Success** | `#5BBE62` | Posts publicados, métricas positivas, spinner de loading |
| **Amber Caution** | `#E1A035` | Status em revisão, alertas não críticos |
| **Coral Alert Danger** | `#F14D4C` | Falhas de publicação, erros de formulário, remoção de hashtags |

### Cores de plataforma (uso contextual)

| Plataforma | Hex | Papel funcional |
|---|---|---|
| **Facebook Blue** | `#1877F2` | Chips, dots e eventos do calendário vinculados ao Facebook |
| **Instagram Rose** | `#E4405F` | Identificação visual de conteúdo Instagram |
| **TikTok Cyan** | `#00F2EA` | Identificação visual de conteúdo TikTok |
| **LinkedIn Professional Blue** | `#0A66C2` | Identificação visual de conteúdo LinkedIn |

### Fundo atmosférico

O body usa um **gradiente composto em três camadas**:
1. Radial verde-mint difuso no topo (`oklch(32% 0.06 155 / 22%)`)
2. Radial azulado no canto superior direito
3. Gradiente linear vertical de `#090D15` → tons levemente mais claros no centro → escurecimento na base

---

## 3. Typography Rules

### Famílias tipográficas

| Token | Fonte | Uso |
|---|---|---|
| `--font-display` | **Plus Jakarta Sans** (500–800) | Títulos, botões, badges, navegação, preços, stats — transmite modernidade e peso |
| `--font-body` | **DM Sans** (400–600) | Parágrafos, descrições, formulários, FAQ — legibilidade em blocos longos |
| `--font-mono` | **JetBrains Mono** (400–500) | Dados tabulares, métricas numéricas, código |

### Hierarquia e peso

- **Títulos de página (`h1`, `.page-title`):** Plus Jakarta Sans 700, `letter-spacing: -0.03em`, tamanho fluido `clamp(22px, 3vw, 28px)` no app; até `64px` no hero da landing
- **Títulos de seção (`.section-title`):** Plus Jakarta Sans 700, `clamp(28px, 4vw, 40px)`
- **Corpo padrão:** DM Sans 15px, `line-height: 1.55`
- **Labels de formulário:** Plus Jakarta Sans 600, 13px, cor muted
- **Kickers / categorias (`.section-kicker`):** Plus Jakarta Sans 700, 12px, uppercase, `letter-spacing: 0.1em`, cor accent
- **Stats e preços:** Plus Jakarta Sans 800, `letter-spacing: -0.03em` a `-0.04em` — números grandes com peso máximo
- **Destaque no hero:** Gradiente de texto mint (`#63D18F` → `#A8F0C8`) aplicado via `background-clip: text`

### Carácter tipográfico

Tipografia com **tracking negativo apertado** nos display sizes para sensação editorial/contemporânea. Corpo mantém tracking neutro para conforto de leitura prolongada.

---

## 4. Component Stylings

### Buttons

- **Forma:** Cantos **generosamente arredondados** (`16px` padrão, `12px` em `.btn-sm`) — sensação amigável, não industrial
- **Primário (`.btn-primary`):** Gradiente diagonal 135° de Fresh Mint → Deep Mint Strong; texto escuro `#1A3D2A`; sombra suave + glow mint; hover eleva `-1px` com glow intensificado
- **Secundário (`.btn-secondary`):** Fundo Soft Charcoal Surface, borda Steel Border; hover clareia superfície
- **Ghost (`.btn-ghost`):** Transparente, texto muted; hover ganha fundo Mint Whisper Dim
- **Ícone (`.btn-icon`):** Quadrado 40×40px, cantos 12px, borda sutil
- **Comportamento:** `scale(0.97)` no active; transição com easing `cubic-bezier(0.22, 1, 0.36, 1)`

### Cards / Containers

- **Forma:** Cantos **amplamente arredondados** (`20px` — `.card`)
- **Fundo:** Soft Charcoal Surface (`#161B23`) com borda Steel Border
- **Sombra:** Whisper-soft diffused — `0 2px 8px rgba(0,0,0,0.28)`; eleva para `0 8px 32px` no hover de feature cards
- **Glass variant (`.card-glass`):** Superfície semi-transparente com blur 20px — reservada para overlays premium
- **Stat cards:** Padding generoso `20px 22px`; valor numérico em display 28px/800
- **Pricing recommended:** Borda accent + glow mint + leve scale `1.02`

### Inputs / Forms

- **Forma:** Cantos **subtamente arredondados** (`10px`)
- **Fundo:** Elevated Slate (`#12161F`)
- **Borda:** Steel Border; focus muda para Fresh Mint Accent com ring de 3px Mint Whisper Dim
- **Textarea:** Altura mínima 100px, resize vertical
- **Upload zone:** Borda tracejada 2px; hover preenche com Mint Whisper Dim
- **Search pill (topbar):** Formato **pill-shaped** (`border-radius: 999px`)

### Badges e chips

- **Badges de status:** Formato **pill-shaped** (`999px`), fonte display 12px/600
  - Draft: cinza neutro translúcido
  - Scheduled: mint sobre fundo dim
  - Published: verde success dim
  - Review: amber dim
- **Platform chips:** Pill com dot colorido 8px; estado ativo preenche 12% da cor da plataforma
- **Filter chips:** Pill transparente; ativo = borda e texto accent + fundo dim

### Navegação (App Shell)

- **Sidebar:** 260px fixa, fundo escuro semi-transparente com blur 16px, borda direita Steel Border
- **Nav items:** Cantos 12px; ícones SVG 18px stroke; item ativo = texto e fundo mint dim
- **Topbar:** 64px sticky, glass blur 12px, borda inferior sutil
- **Logo:** Ícone 32px com cantos 10px + gradiente mint; wordmark Plus Jakarta Sans 800

### Modal, Toast e FAQ

- **Modal overlay:** Fundo quase preto 72% opaco + blur 8px; modal entra com translateY + scale
- **Toast:** Fixo bottom-center, borda accent, glow mint, animação slide-up
- **FAQ accordion:** Card com cantos 20px; aberto = borda mint 40% opacidade; chevron rotaciona 180°

### Calendário

- Grid 7 colunas com gap 1px (fundo border como separador)
- Dias: min-height 110px; hoje = fundo Mint Whisper Dim
- Eventos: pill compacta com barra lateral colorida por plataforma, cantos 6px

---

## 5. Layout Principles

### Espaçamento e respiro

- **Padding de página (`.page-content`):** `28px` desktop, `20px 16px` mobile — margem confortável sem desperdício
- **Page header:** Flex space-between com gap 16px; título + subtítulo empilhados; CTA primário à direita
- **Grids responsivos:**
  - Stats: `repeat(auto-fit, minmax(200px, 1fr))`, gap 16px
  - Features/pricing: `minmax(280–300px, 1fr)`, gap 20–24px
  - Posts: `minmax(280px, 1fr)`
- **Seções da landing:** Padding vertical fluido `clamp(64px, 10vw, 100px)`; conteúdo centralizado com max-width 720–1200px

### Alinhamento e estrutura

- **App shell:** Sidebar fixa à esquerda + área principal com margin-left compensatória
- **Landing:** Nav fixa top com padding horizontal `clamp(20px, 5vw, 48px)`; hero centralizado com mockup max-width 1100px
- **Footer:** Grid 5 colunas (2fr brand + 4×1fr links); colapsa para 2 colunas em tablet, 1 em mobile

### Profundidade e elevação

| Nível | Sombra | Uso |
|---|---|---|
| **Flat / whisper** | `0 2px 8px rgba(0,0,0,0.28)` | Cards padrão, botões |
| **Medium lift** | `0 8px 32px rgba(0,0,0,0.38)` | Feature cards hover, pricing recommended |
| **High elevation** | `0 16px 48px rgba(0,0,0,0.45)` | Modais, hero mockup |
| **Glow accent** | `0 0 48px mint 35%` | CTAs hero, toast, pricing badge |

### Animações

- **Entrada:** `fadeUp` 0.6s com delays escalonados (0.08s incrementos) — hero e dashboard
- **Scroll reveal (landing):** IntersectionObserver adiciona `.visible` em `[data-animate]`
- **Interação:** Hover translateY -1px a -4px; active scale 0.97; FAQ max-height transition 0.35s

### Responsividade

- **≤1024px:** Grids 2/3 colunas colapsam para 1 coluna
- **≤768px:** Sidebar off-canvas com backdrop escuro; toggle hamburger visível
- **≤600px:** Footer single column; mockup sidebar vira barra horizontal

### Raio de cantos (referência rápida)

| Token | Valor | Descrição física |
|---|---|---|
| `--radius-card` | 20px | Generosamente arredondado — cards, modais, FAQ |
| `--radius-btn` | 16px | Suavemente arredondado — botões padrão |
| `--radius-sm` | 10px | Subtamente arredondado — inputs, avatares, thumbs |
| `--radius-pill` | 999px | Pill-shaped — badges, search, chips, hashtags |

---

## Referência de implementação

| Asset | Caminho |
|---|---|
| Tokens globais e componentes | `static/css/custom.css` |
| Landing page específica | `static/css/landing.css` |
| Shell do app | `templates/base.html` |
| Landing | `templates/core/landing.html` |
| Dashboard | `templates/core/dashboard.html` |

---

## Prompting para novas telas (Stitch / IA)

Ao gerar novas telas para o PostFlow, descreva:

1. **Modo escuro obrigatório** com fundo Midnight Navy e radiais mint no topo
2. **CTA primário** em Fresh Mint (`#63D18F`) com glow sutil
3. **Cards** Soft Charcoal Surface com bordas Steel Border e cantos 20px
4. **Tipografia** Plus Jakarta Sans para títulos/ações, DM Sans para corpo
5. **Ícones** SVG stroke 2px, estilo line-art minimalista
6. **Plataformas sociais** sempre com suas cores oficiais como acento contextual, nunca como fundo dominante
7. **Densidade** equilibrada — grids com gap 16–24px, padding de página 28px

# Detection Automatique du Stack Technique

## Fichiers de Detection

Lire ces fichiers dans l'ordre pour detecter le stack :

### 1. CLAUDE.md (priorite maximale)

```
Glob("CLAUDE.md") → lire section "Stack Technique" ou "Architecture"
```

Si CLAUDE.md contient le stack, c'est la source de verite. Ne pas chercher plus loin.

### 2. package.json (frontend + backend Node)

```json
// Frontend
"react-native" ou "expo" → React Native / Expo
"react" (sans react-native) → React Web
"vue" → Vue.js
"next" → Next.js
"nuxt" → Nuxt.js
"svelte" → SvelteKit
"angular" → Angular

// Backend
"@supabase/supabase-js" → Supabase
"firebase" ou "firebase-admin" → Firebase
"express" → Express.js
"fastify" → Fastify
"@nestjs/core" → NestJS

// Build
"vite" → Vite
"webpack" → Webpack
"turbo" → Turborepo (monorepo)
```

### 3. Fichiers de config specifiques

| Fichier | Stack detecte |
|---------|---------------|
| `supabase/config.toml` | Supabase |
| `firebase.json` | Firebase |
| `app.json` avec "expo" | Expo / React Native |
| `vite.config.ts` | Vite |
| `next.config.js` | Next.js |
| `nuxt.config.ts` | Nuxt |
| `netlify.toml` | Netlify deploy |
| `vercel.json` | Vercel deploy |
| `docker-compose.yml` | Docker |
| `prisma/schema.prisma` | Prisma ORM |
| `drizzle.config.ts` | Drizzle ORM |

### 4. Structure de dossiers

| Dossier | Indice |
|---------|--------|
| `supabase/migrations/` | Supabase avec migrations |
| `functions/` + `firebase.json` | Firebase Functions |
| `supabase/functions/` | Supabase Edge Functions (Deno) |
| `pages/` ou `app/` | Framework routing basé fichiers |
| `src/components/` | SPA classique |
| `packages/` | Monorepo |

### 5. Framework SYM (agents disponibles)

```
Glob("~/.claude/agents/sym-*.md") → Framework SYM installe
```

Si SYM est detecte, les executeurs du CDC peuvent reference les agents SYM directement.

## Mapping Stack → Executeurs

### Supabase Backend

| Tache | Executeur generique | Agent SYM |
|-------|---------------------|-----------|
| Schema/tables | Agent DB migration | sym-db-migration |
| RLS + RPC | Agent DB SQL | sym-db-sql |
| Auth (OAuth, MFA) | Agent Auth | sym-be-auth |
| Storage (buckets) | Agent Storage | sym-be-storage |
| Realtime | Agent Realtime | sym-be-realtime |
| Edge Functions | Agent Edge | sym-be-edge |

### Firebase Backend

| Tache | Executeur generique | Outil |
|-------|---------------------|-------|
| Firestore schema | Claude Code direct | firebase CLI |
| Security Rules | Claude Code direct | rules files |
| Cloud Functions | Claude Code direct | functions/ |
| Auth config | Claude Code direct | firebase console |

### React Native / Expo Frontend

| Tache | Executeur generique | Agent SYM |
|-------|---------------------|-----------|
| Types + Services | Agent frontend core | sym-fe-core |
| Custom hooks | Agent hooks React | sym-fe-hook-react |
| Components + Screens | Agent UI React | sym-fe-ui-react |

### Vue.js Frontend

| Tache | Executeur generique | Agent SYM |
|-------|---------------------|-----------|
| Types + Services | Agent frontend core | sym-fe-core |
| Composables | Agent composables Vue | sym-fe-composable-vue |
| Components + Pages | Agent UI Vue | sym-fe-ui-vue |

### Next.js / React Web

| Tache | Executeur generique | Outil |
|-------|---------------------|-------|
| Types + Services | Agent frontend core | sym-fe-core |
| Custom hooks | Agent hooks React | sym-fe-hook-react |
| Components + Pages | Claude Code direct | Next.js conventions |

### Transverse (tout stack)

| Tache | Executeur generique | Agent SYM |
|-------|---------------------|-----------|
| Integration cross-layer | Agent integration | sym-integ |
| Audit securite | Agent securite | sym-security |
| Performance | Agent performance | sym-perf |
| Tests | Agent tests | sym-test-mobile / sym-test-web |
| Build / validation | Agent build | sym-build |
| Deployment | Agent deploy | sym-deploy |

## Output Detection

Apres detection, produire ce brief :

```markdown
## Stack Detecte

| Couche | Technologie | Source detection |
|--------|-------------|-----------------|
| Frontend | [tech] | [fichier qui l'a confirme] |
| Backend | [tech] | [fichier qui l'a confirme] |
| DB | [tech] | [fichier qui l'a confirme] |
| Deploy | [tech] | [fichier qui l'a confirme] |
| Framework agents | [SYM / aucun] | [presence ~/.claude/agents/] |

## Executeurs Disponibles

| Type | Executeur | Disponible |
|------|-----------|------------|
| DB migration | [nom] | oui/non |
| DB SQL/RLS | [nom] | oui/non |
| Frontend core | [nom] | oui/non |
| UI components | [nom] | oui/non |
| Skills Cowork | .claude/skills/ | oui |
| Taches planifiees | /schedule | oui |
```

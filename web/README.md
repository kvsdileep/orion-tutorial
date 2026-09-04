# Curriculum site

The Next.js companion to the lessons: eighteen chapter pages with interactive demos, a curriculum overview, and a playground that shows the shipped orchestrator.

## Run locally

```bash
cd web
npm install
npm run dev
```

## Keep the code panels in sync

Chapter code comes from the lesson files. After editing a lesson, run from the repo root:

```bash
uv run orion sync-web
```

Only cells whose tag line ends with `web` are copied. Prose and demo transcripts in `lib/chapters/*.ts` are written by hand.

## Deploy

The site deploys from this repository on Vercel.

| Setting | Value |
|---|---|
| Framework preset | Next.js |
| Root directory | `web` |
| Build command | `npm run build` |
| Install command | `npm install` |
| Environment variables | none |
| Production branch | `main` |

Import the repository in the Vercel dashboard (Add New Project, pick the GitHub repo, set Root Directory to `web`). Every push to `main` deploys to production; every other branch gets a preview URL. The production URL is whatever Vercel assigns to the project; record it here after the first deploy.

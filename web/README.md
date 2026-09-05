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

Production: https://orion-tutorial-brown.vercel.app (Vercel project `orion-tutorial`, team `dileep-growthschools-projects`).

The project has Root Directory `web` and the repo root is linked to it (`.vercel/`, gitignored). To deploy from this machine:

```bash
npx vercel deploy --prod --yes   # run from the repo root
```

To have every push to `main` deploy on its own, connect GitHub once in the Vercel dashboard: Project Settings, Git, Connect Git Repository, pick `kvsdileep/orion-tutorial`. That needs a GitHub login connection on the Vercel account (Account Settings, Login Connections).

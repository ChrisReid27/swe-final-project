Deploying frontend to Vercel (beginner-friendly)

Overview
- The frontend is a Vite + React app. We'll build a production bundle with `npm run build` and deploy that bundle on Vercel.
- The frontend expects an environment variable `VITE_API_BASE_URL` that points to your deployed backend API root (for example `https://my-backend.up.railway.app/api`).

Steps
1. Push your repository to GitHub (if not already).
2. Log in to Vercel and click "New Project" → Import Git Repository → choose your repo.
3. In the project settings, set the Environment Variables:
   - `VITE_API_BASE_URL` = `https://<your-backend-domain>/api` (replace with the URL of your deployed backend).
4. Build settings (Vercel usually auto-detects):
   - Framework Preset: `Other` or `Vite` if available.
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Click Deploy. Vercel will run `npm install` and `npm run build` and serve the static output.

Local testing
- To run locally using the backend hosted elsewhere, create a `.env` file in `frontend/` with:

```
VITE_API_BASE_URL=https://<your-backend-domain>/api
```

- Then run:

```bash
npm install
npm run dev
```

Notes
- Vite exposes env vars prefixed with `VITE_` to client code; `VITE_API_BASE_URL` is already used by `src/api/client.js`.
- If your backend is at the same host as Vercel project (not likely), you can omit `https://` and use relative paths — but explicit absolute URL is clearer.
- Make sure the deployed backend has CORS and CSRF configured to allow requests from your Vercel domain. See `backend/DEPLOY.md`.

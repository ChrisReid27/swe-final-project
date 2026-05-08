Deploy notes for backend (Django)

Overview
- This file lists the minimal steps and environment variables required to deploy the Django backend to a platform like Railway or Render.

Required environment variables
- `SECRET_KEY` — a long random string. Keep secret.
- `DEBUG` — `False` in production (string `'False'` or `'0'`).
- `ALLOWED_HOSTS` — comma-separated hosts, e.g. `example.com,api.example.com`.
- `CSRF_TRUSTED_ORIGINS` — comma-separated origins including scheme, e.g. `https://your-frontend.vercel.app`.

Quick deploy checklist
1. Connect repository to Railway (or your chosen host).
2. For Railway specifically:
	 - Create a new project and connect your GitHub repo.
	 - Add the PostgreSQL plugin (or create a managed Postgres database) so you have a `DATABASE_URL` provided by Railway.
	 - In Project Settings → Environment Variables, set:
		 - `SECRET_KEY` — your secret key
		 - `DEBUG` — `False`
		 - `ALLOWED_HOSTS` — comma-separated hostnames for your app
		 - `CSRF_TRUSTED_ORIGINS` — include your frontend origin (e.g. `https://<your-vercel-app>.vercel.app`)
		 - `DATABASE_URL` — provided by Railway Postgres (or your DB provider)
3. Ensure the host uses Python and installs from `requirements.txt`.
4. The default start command is provided by `Procfile`, which now runs migrations before starting the app: `web: python manage.py migrate --noinput && gunicorn gridquiz.wsgi --bind 0.0.0.0:$PORT --log-file -`.
5. If your host does not honor the `Procfile`, make sure migrations run on startup or run them manually on the host. Railway provides a console or you can run:

```
railway run python manage.py migrate
```

6. Collect static files on the host:

```
railway run python manage.py collectstatic --noinput
```

Local testing commands
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Notes
- If you plan to use Railway's ephemeral filesystem, use a managed DB (Postgres) and configure `DATABASES` accordingly.
- Frontend must be configured to call the backend API URL (set in frontend environment or code).

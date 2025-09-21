# Render Deployment (Django + Postgres)

- Prereqs: Postgres database and Web Service on Render. This repo includes `render.yaml` and `Procfile`.
- Key env vars:
  - `DEBUG=False`
  - `SECRET_KEY` (auto-generated in render.yaml or set manually)
  - `DATABASE_URL` (auto-wired from Render Postgres)
  - `ALLOWED_HOSTS`: include Render domain and localhost
  - `CORS_ALLOWED_ORIGINS`: frontend origins (Vercel or custom domain)
  - `CSRF_TRUSTED_ORIGINS`: same as CORS
- Build/Start:
  - Build installs requirements and runs `collectstatic`
  - Start uses `gunicorn config.wsgi:application`
- After first deploy: run migrations from Render shell
  - `python manage.py migrate`
- Media files: currently stored on disk at `media/` (ephemeral on Render). For persistence, configure S3-compatible storage.
- Frontend config (Vercel): set `NEXT_PUBLIC_BACKEND_URL` to your Render URL (no trailing slash).

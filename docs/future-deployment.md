# Future Deployment Notes (not yet deployed)

This document is planning-only. Nothing in this repository has been deployed,
and this restoration explicitly did not deploy anything.

## Likely service shape on Railway (or similar PaaS)

- **Web service**: the Flask app (`app/web/web_application.py`) as a single
  web process (`gunicorn` recommended over the Flask dev server for anything
  beyond local testing).
- **Database**: a managed MySQL instance (Railway offers MySQL as an add-on)
  — the schema in `database/plant_disease_sql_script.sql` would need to be
  applied to it.
- **Model artifact**: the ~228 MB `.pth` file cannot reasonably live in the
  git repo or a typical container image layer without care. Options: fetch
  it at container-start from a release asset / object storage URL via an
  environment variable, or use a persistent volume.
- **Environment variables needed**: `MYSQL_HOST`, `MYSQL_USER`,
  `MYSQL_PASSWORD`, `MYSQL_DATABASE`, `FLASK_SECRET_KEY`, and a
  `MODEL_PATH` (or a download URL for the model artifact).
- **Persistent storage**: uploaded images and generated statistics charts are
  currently written to local disk (`static/uploaded_images/`,
  `static/images/`) — on an ephemeral container filesystem these would need
  to move to object storage or a mounted volume.

## Blockers inherited from the 2020 architecture

- The app was built for Python 3.6-era PyTorch/Flask with no pinned
  dependency versions recorded — a modern environment will need dependency
  testing before it can be trusted to behave identically (see the main
  README's "Running the historical project" section).
- No containerization, health checks, or process manager existed originally.
- The MySQL connection logic assumes a local/trusted network MySQL instance,
  not a managed cloud database with TLS requirements — this would need minor
  connection-string changes, not a redesign.

No deployment, infrastructure creation, or paid service was set up as part of
this restoration.

# Contract (read first)

- Do not delete or rename existing working files unless explicitly instructed.
- Prefer modifying existing files over creating new ones.
- Keep changes minimal and reversible.
- When adding new files, keep them in the intended repo structure.
- After changes, validate locally: build container + run + check port.
- If unsure about an existing convention, search the repo first and follow it.
- Do not hardcode subscription IDs, tenant IDs, or secrets; use pipeline variables.

# Repo Intent

This repository is a reusable template for Python web apps (Flask, Streamlit, Dash) deployed as containers to Azure Web App via Azure DevOps (ACR + pipeline).

# Repo Map (target)

```text
repo-root/
├─ src/app.py
├─ requirements.txt
├─ appconfig.json
├─ Dockerfile
├─ docker/entrypoint.sh
├─ .devcontainer/devcontainer.json
└─ azure-pipelines.yml
```

# Configuration: appconfig.json

`appconfig.json` is the source of truth for runtime behavior.

- `app_type`: `flask` | `streamlit` | `dash`
- `app_module`: default `src.app`
- `port`: default `8000`

Environment variables may override these values at runtime.

# Local Validation Checklist

```bash
pip install -r requirements.txt
```

```bash
docker build -t local-app .
```

```bash
docker run --rm -p 8000:8000 local-app
```

```bash
# Flask
docker run --rm -e APP_TYPE=flask -p 8000:8000 local-app
```

```bash
# Streamlit
docker run --rm -e APP_TYPE=streamlit -p 8000:8000 local-app
```

```bash
# Dash
docker run --rm -e APP_TYPE=dash -p 8000:8000 local-app
```

Manual check: Open http://localhost:8000

# Change Policy

- Do not hardcode secrets or IDs.
- Use Azure DevOps variables for resource names and service connections.
- Pipeline changes must keep PR validation and main deployment intact.
- Prefer minimal changes; avoid restructuring the repo without explicit reason.

# How to Add a New App

1. Put app in `src/app.py`.
2. Set `appconfig.json` appropriately.
   - Flask exports `app`.
   - Dash exports `server`.
   - Streamlit runs `src/app.py`.
3. Add dependencies to `requirements.txt`.
4. Validate locally (build/run).
5. Commit and push; pipeline builds/pushes/deploys.

# When modifying deployment

- Azure Web App for Containers needs `WEBSITES_PORT=8000` and the container must listen on `PORT=8000`.
- Flask/Dash should use `gunicorn`.
- Streamlit must run with `--server.address 0.0.0.0` and `--server.port 8000`.

# Project architecture

Developer machine -> Dev Container -> Azure DevOps Pipeline -> Build Docker image -> Push to Azure Container Registry (ACR) -> Deploy to Azure Web App for Containers.

# Dev environment

- Use `.devcontainer/devcontainer.json` with Python 3.12, `azure-cli`, and `azd`.
- Keep local development and container runtime aligned to port `8000`.
- Put framework app code in `src/app.py` and use `appconfig.json` for runtime selection.

# Local testing

```bash
docker build -t local-app .
docker run -p 8000:8000 local-app
```

# Deployment flow

commit -> pipeline -> docker build -> ACR push -> Web App deploy

# How to add new apps

1. Create `src/app.py`.
2. Update `appconfig.json`.
3. Update `requirements.txt`.
4. Commit and push.

# Quick local validation

```bash
./scripts/validate_local.sh
```

# Run locally with logs

```bash
./scripts/run_local.sh
```

# Create a new app in 30 seconds

```bash
python scripts/new_app.py --type flask
```

or

```bash
python scripts/new_app.py --type streamlit
```

Makefile shortcuts:

```bash
make new-flask
make new-streamlit
make validate
make run
```

Then validate:

```bash
./scripts/validate_local.sh
```

Or run interactively:

```bash
./scripts/run_local.sh
```

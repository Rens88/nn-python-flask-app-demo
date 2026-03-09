# Python Web App Template for Azure Containers

This repository is evolving into a reusable template for Python web apps (Flask, Streamlit, Dash) deployed as containers to Azure Web App for Containers through Azure DevOps and ACR.

## Runtime model

- Source app entrypoint: `src/app.py`
- Shared brand palette: `src/brand.py`
- Runtime config: `appconfig.json`
- Container startup: `docker/entrypoint.sh`
- Container build: `Dockerfile`
- CI/CD: `azure-pipelines.yml`

## Brand assets

- Logos live in `static/images/`
  - `teamnl_logo_transparant.png` (symbol + TeamNL + Olympic rings)
  - `teamnl_sport_science_centre_LOGO.png` (TeamNL Sport Science Centre wordmark)
- TeamNL color palette constants are versioned in `src/brand.py`.

`appconfig.json` defaults:

```json
{
  "app_type": "streamlit",
  "app_module": "src.app",
  "port": 8000
}
```

Environment variables (`APP_TYPE`, `APP_MODULE`, `PORT`) can override these values.

## Local run without Docker (Windows friendly)

Command Prompt:

```bat
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/app.py --server.address 0.0.0.0 --server.port 8000
```

Open `http://localhost:8000`.

## Local container validation (Docker required)

Windows prerequisites:

```bat
where docker
docker --version
docker info
```

If any of these fail, install/start Docker Desktop and open a new terminal.

Windows Command Prompt one-command launcher:

```bat
scripts\run_local.cmd
```

Manual Docker commands:

```bat
docker build -t local-app .
docker run --rm -p 8000:8000 local-app
```

Framework-specific overrides:

```bat
docker run --rm -e APP_TYPE=flask -p 8000:8000 local-app
docker run --rm -e APP_TYPE=streamlit -p 8000:8000 local-app
docker run --rm -e APP_TYPE=dash -p 8000:8000 local-app
```

## Azure deployment paths

- Existing `azd`-based deployment remains in `azure.yaml` + `infra/`.
- Azure DevOps container pipeline path is defined in `azure-pipelines.yml`:
  - Build image
  - Push to ACR
  - Deploy to Azure Web App for Containers (Dev and Prod)

## Developer productivity scripts

Create a new app in about 30 seconds:

```bash
python scripts/new_app.py --type flask
python scripts/new_app.py --type streamlit
```

Makefile shortcuts:

```bash
make new-flask
make new-streamlit
make validate
make run
```

Validate container locally:

```bash
./scripts/validate_local.sh
```

Run locally with streaming container logs:

```bash
./scripts/run_local.sh
```

Windows Command Prompt:

```bat
scripts\run_local.cmd
```

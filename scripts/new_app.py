#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

FLASK_TEMPLATE = '''from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return {"status": "ok", "framework": "flask"}
'''

STREAMLIT_TEMPLATE = '''import streamlit as st

st.set_page_config(page_title="New Streamlit App")

st.title("New Streamlit App")

st.write({
    "status": "ok",
    "framework": "streamlit"
})
'''

REQUIRED_PACKAGES = {
    "flask": ["flask", "gunicorn"],
    "streamlit": ["streamlit"],
}


def ensure_src_app(app_type: str, force: bool) -> None:
    src_dir = Path("src")
    src_dir.mkdir(parents=True, exist_ok=True)
    app_file = src_dir / "app.py"

    if app_file.exists() and not force:
        print("src/app.py already exists. Use --force to overwrite.")
        sys.exit(1)

    content = FLASK_TEMPLATE if app_type == "flask" else STREAMLIT_TEMPLATE
    app_file.write_text(content, encoding="utf-8")


def ensure_appconfig(app_type: str) -> None:
    appconfig_path = Path("appconfig.json")
    data: dict[str, object]

    if appconfig_path.exists():
        try:
            parsed = json.loads(appconfig_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(
                f"appconfig.json exists but is invalid JSON: {exc}. Fix it first.",
                file=sys.stderr,
            )
            sys.exit(1)

        if not isinstance(parsed, dict):
            print("appconfig.json must contain a JSON object.", file=sys.stderr)
            sys.exit(1)
        data = parsed
    else:
        data = {}

    data["app_type"] = app_type
    data["port"] = 8000
    data.setdefault("app_module", "src.app")

    appconfig_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def parse_requirement_name(line: str) -> str | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    if "#" in stripped:
        stripped = stripped.split("#", 1)[0].strip()

    if stripped.startswith(("-e ", "--", "git+", "http://", "https://")):
        return None

    match = re.match(r"^([A-Za-z0-9_.-]+)", stripped)
    if not match:
        return None
    return match.group(1).lower()


def ensure_requirements(app_type: str) -> None:
    req_path = Path("requirements.txt")
    existing_lines = req_path.read_text(encoding="utf-8").splitlines() if req_path.exists() else []

    existing_packages = {
        package
        for line in existing_lines
        if (package := parse_requirement_name(line)) is not None
    }

    required = REQUIRED_PACKAGES[app_type]
    changed = False
    for dep in required:
        dep_key = dep.lower()
        if dep_key not in existing_packages:
            existing_lines.append(dep)
            existing_packages.add(dep_key)
            changed = True

    if not req_path.exists() or changed:
        req_path.write_text("\n".join(existing_lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a minimal Flask or Streamlit app.")
    parser.add_argument("--type", required=True, choices=["flask", "streamlit"], dest="app_type")
    parser.add_argument("--force", action="store_true", help="Overwrite src/app.py if it exists")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_src_app(args.app_type, args.force)
    ensure_appconfig(args.app_type)
    ensure_requirements(args.app_type)
    print(f"Created {args.app_type} app scaffold at src/app.py and updated config/dependencies.")


if __name__ == "__main__":
    main()

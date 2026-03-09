.PHONY: new-flask new-streamlit validate run

new-flask:
	python scripts/new_app.py --type flask

new-streamlit:
	python scripts/new_app.py --type streamlit

validate:
	./scripts/validate_local.sh

run:
	./scripts/run_local.sh

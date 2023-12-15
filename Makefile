init:
	python3.11 -m venv .venv
	. .venv/bin/activate && pip install pip-tools && pip install -r requirements/local.txt

cdev:
	. .venv/bin/activate && pip-compile --upgrade --extra=local --generate-hashes --allow-unsafe --output-file=requirements/local.txt pyproject.toml

cprod:
	. .venv/bin/activate && pip-compile --upgrade --extra=production --generate-hashes --allow-unsafe --output-file=requirements/production.txt pyproject.toml

local:
	docker compose -f local.yml up -d

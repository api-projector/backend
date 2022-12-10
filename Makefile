# -- poetry --

install:
	@poetry install --remove-untracked

lint:
	black --check .
	mypy .
	flake8 .
	DJANGO_ENV=build python server/manage.py makemigrations --dry-run --check
	xenon --max-absolute A \
        --max-modules A \
        --max-average A \
        --exclude server/apps/core/graphql/fields/query_connection.py \
        server
	poetry check
	pip check
	#safety check --bare
	polint -i location,unsorted server/locale
	dennis-cmd lint --errorsonly server/locale

test:
	@pytest

# -- django --

make-messages:
	@python server/manage.py makemessages --ignore=.venv/* -l en -l ru --no-location

compile-messages:
	@python server/manage.py compilemessages

make-migrations:
	@python server/manage.py makemigrations

migrate:
	@python server/manage.py migrate

generate-graphql-schema:
	@python server/manage.py graphql_schema --schema server.gql.schema --out tests/schema.graphql

# -- precommit --

pre-commit:
	@pre-commit

pre-commit-install:
	@pre-commit install
	@pre-commit install --hook-type commit-msg

pre-commit-update:
	@pre-commit autoupdate

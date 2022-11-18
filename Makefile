install-deps:
	@poetry install --remove-untracked

lint:
	black --check .
	mypy .
	flake8 .
#	DJANGO_ENV=production python manage.py check --deploy --fail-level WARNING
	DJANGO_ENV=build python manage.py makemigrations --dry-run --check
	xenon --max-absolute A \
        --max-modules A \
        --max-average A \
        --exclude server/apps/core/graphql/fields/query_connection.py \
        server
	poetry check
	pip check
	#safety check --bare --full-report
	polint -i location,unsorted locale
	dennis-cmd lint --errorsonly locale

test:
	@pytest

# -- django --

generate-locale:
	@python manage.py makemessages --ignore=.venv/* -l en -l ru --no-location

compile-messages:
	@python manage.py compilemessages

make-migrations:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

generate-graphql-schema:
	@python manage.py graphql_schema --schema server.gql.schema --out tests/schema.graphql

# -- precommit --

pre-commit:
	@pre-commit

pre-commit-install:
	@pre-commit install
	@pre-commit install --hook-type commit-msg

pre-commit-update:
	@pre-commit autoupdate

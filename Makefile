export COMPOSE_PROJECT_NAME=api-projector
export DOCKER_DEFAULT_PLATFORM=linux/amd64
-include config.env

COMPOSE_ARGS=-f tools/compose/docker-compose.yml
COMPOSE_ALL_FILE=tools/compose/docker-compose.all.yml

# -- poetry --

install:
	@poetry install --remove-untracked

lint:
	black --check .
	mypy .
	flake8 .
	DJANGO_ENV=build python src/manage.py makemigrations --dry-run --check
	xenon --max-absolute A \
        --max-modules A \
        --max-average A \
        --exclude src/apps/core/graphql/fields/query_connection.py \
        src
	poetry check
	pip check
	#safety check --bare
	polint -i location,unsorted src/locale
	dennis-cmd lint --errorsonly src/locale

test:
	@pytest

# -- django --

make-messages:
	@python src/manage.py makemessages --ignore=.venv/* -l en -l ru --no-location

compile-messages:
	@python src/manage.py compilemessages

make-migrations:
	@python src/manage.py makemigrations

migrate:
	@python src/manage.py migrate

generate-graphql-schema:
	@python src/manage.py graphql_schema --schema src.gql.schema --out tests/schema.graphql

# -- precommit --

pre-commit:
	@pre-commit

pre-commit-install:
	@pre-commit install
	@pre-commit install --hook-type commit-msg

pre-commit-update:
	@pre-commit autoupdate

up:
	docker compose ${COMPOSE_ARGS} up --remove-orphans

up-all:
	docker compose ${COMPOSE_ARGS} -f ${COMPOSE_ALL_FILE} up --build --remove-orphans

down:
	docker compose ${COMPOSE_ARGS} down

down-all:
	docker compose ${COMPOSE_ARGS} -f ${COMPOSE_ALL_FILE} down

stop:
	docker compose ${COMPOSE_ARGS} stop

stop-all:
	docker compose ${COMPOSE_ARGS} -f ${COMPOSE_ALL_FILE} stop

# -- postgresql --

download-pg-dump:
	rsync -L -av --progress ${POSTGRES_DUMP} tools/compose/dumps/pg.dump

# -- local postgresql --

local-drop-db:
	dropdb --u admin --if-exists ${POSTGRES_DATABASE}

local-create-db:
	createdb --u admin ${POSTGRES_DATABASE}

local-restore-dump: local-drop-db local-create-db
	pg_restore -U admin -d ${POSTGRES_DATABASE} -Fc --disable-triggers tools/compose/dumps/pg.dump

# -- docker postgresql --

drop-pg-db:
	docker compose ${COMPOSE_ARGS} exec postgres dropdb -U ${POSTGRES_USER} --if-exists ${POSTGRES_DB}

create-pg-db:
	docker compose ${COMPOSE_ARGS} exec postgres createdb -U ${POSTGRES_USER} ${POSTGRES_DB}

restore-pg-dump: drop-pg-db create-pg-db
	docker compose ${COMPOSE_ARGS} exec -T postgres pg_restore --no-owner -C -U ${POSTGRES_USER} -d ${POSTGRES_DB} -Fc --disable-triggers < tools/compose/dumps/pg.dump

# -- couchdb --

download-couchdb-dump:
	rsync -L -av ${COUCHDB_DUMP} tools/compose/dumps/couchdb.tar.gz

restore-couchdb-dump: download-couchdb-dump
	rm -rf tools/compose/couchdb/data
	mkdir tools/compose/couchdb/data
	tar -zxvf tools/compose/dumps/couchdb.tar.gz -C tools/compose/couchdb/data

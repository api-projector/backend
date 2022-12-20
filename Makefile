COMPOSE_FILE=tools/compose/docker-compose.yml
COMPOSE_ALL_FILE=tools/compose/docker-compose.all.yml

export COMPOSE_PROJECT_NAME=api-projector
export DOCKER_DEFAULT_PLATFORM=linux/amd64
include config.env

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
        server
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
	docker compose -f ${COMPOSE_FILE} up --remove-orphans

up-all:
	docker compose -f ${COMPOSE_FILE} -f ${COMPOSE_ALL_FILE} up --build --remove-orphans

down:
	docker compose -f ${COMPOSE_FILE} down

down-all:
	docker compose -f ${COMPOSE_FILE} -f ${COMPOSE_ALL_FILE} down

stop:
	docker compose -f ${COMPOSE_FILE} stop

stop-all:
	docker compose -f ${COMPOSE_FILE} -f ${COMPOSE_ALL_FILE} stop

# -- postgresql --

download-pg-dump:
	rsync -L -av --progress ${POSTGRES_DUMP} dumps/pg.dump

# -- local postgresql --

local-drop-db:
	dropdb --u admin --if-exists ${POSTGRES_DATABASE}

local-create-db:
	createdb --u admin ${POSTGRES_DATABASE}

local-restore-dump: local-drop-db local-create-db
	pg_restore -U admin -d ${POSTGRES_DATABASE} -Fc --disable-triggers dumps/pg.dump

# -- docker postgresql --

drop-pg-db:
	docker compose exec postgres dropdb -U ${POSTGRES_USER} --if-exists ${POSTGRES_DB}

create-pg-db:
	docker compose exec postgres createdb -U ${POSTGRES_USER} ${POSTGRES_DB}

restore-pg-dump: drop-pg-db create-pg-db
	docker compose exec -T postgres pg_restore -U ${POSTGRES_USER} -d ${POSTGRES_DB} -Fc --disable-triggers < dumps/pg.dump

# -- couchdb --

download-couchdb-dump:
	rsync -L -av ${COUCHDB_DUMP} dumps/couchdb.tar.gz

restore-couchdb-dump: download-couchdb-dump
	rm -rf couchdb/data
	mkdir couchdb/data
	tar -zxvf dumps/couchdb.tar.gz -C couchdb/data

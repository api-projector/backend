include config.env

export DOCKER_DEFAULT_PLATFORM=linux/amd64
export COMPOSE_PROJECT_NAME=api-projector

up:
	docker compose up --remove-orphans

up-all:
	docker compose -f docker-compose.yml -f docker-compose.all.yml up --build --remove-orphans

down:
	docker compose down

down-all:
	docker compose -f docker-compose.yml -f docker-compose.all.yml down

stop:
	docker compose stop

stop-all:
	docker compose -f docker-compose.yml -f docker-compose.all.yml stop

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

include config.env

COMPOSE_PROJECT=api-projector

up:
	@docker compose -p ${COMPOSE_PROJECT} up --remove-orphans

down:
	@docker compose -p ${COMPOSE_PROJECT} down

stop:
	@docker compose -p ${COMPOSE_PROJECT} stop

download-pg-dump:
	@rsync -L -av --progress ${POSTGRES_DUMP} dumps/

# -- local postgresql

restore-dump: drop-db create-db restore-dump

drop-db:
	@dropdb --u admin --if-exists ${POSTGRES_DATABASE}

create-db:
	@createdb --u admin ${POSTGRES_DATABASE}

restore-dump:
	@pg_restore -U admin -d ${POSTGRES_DATABASE} -Fc --disable-triggers ./dumps/latest.dump

# -- couchdb

download-couchdb-backup:
	@rsync -L -av ${COUCHDB_DUMP} .

restore-couchdb-dump: download_backup
	@rm -rf data && mkdir data && tar -zxvf latest.tar.gz -C data

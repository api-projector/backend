COMPOSE_PROJECT=api-projector

compose-up:
	@docker compose -p ${COMPOSE_PROJECT} up --remove-orphans

download-dump:
	@rsync -L -av --progress jworker02:/mnt/volumes/pg/backup/api_projector/latest.dump dumps/

# -- local postgresql

restore-dump: drop-db create-db restore-dump

drop-db:
	@dropdb --u admin --if-exists api_projector

create-db:
	@createdb --u admin api_projector

restore-dump:
	@pg_restore -U admin -d api_projector -Fc --disable-triggers ./dumps/latest.dump

# -- couchdb

download-couchdb-backup:
	@rsync -L -av root@162.55.208.173:/mnt/storage/api-projector/couchdb/backups/latest.tar.gz .

restore-couchdb-dump: download_backup
	@rm -rf data && mkdir data && tar -zxvf latest.tar.gz -C data

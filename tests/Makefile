STORAGE_ADDRESS := 162.55.208.173

install_deps:
	@poetry install --remove-untracked

generate_test_graphql_schema:
	@./manage.py graphql_schema --schema server.gql.schema --out tests/schema.graphql

lint:
	@./scripts/lint.sh

test:
	@pytest

generate_locale:
	@./manage.py makemessages --ignore=.venv/* -l en -l ru --no-location

compile_messages:
	@./manage.py compilemessages

pre_commit:
	@pre-commit

install_pre_commit:
	@pre-commit install && pre-commit install --hook-type commit-msg

update_pre_commit:
	@pre-commit autoupdate

download_pg_dump:
	@rsync -Lav --progress root@${STORAGE_ADDRESS}:/mnt/storage/pg/backup/api_projector/latest.dump .

download_couchdb_dump:
	@rsync -Lav --progress root@${STORAGE_ADDRESS}:/mnt/storage/api-projector/couchdb/backups/latest.tar.gz .

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![CI/CD](https://github.com/api-projector/backend/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/api-projector/backend/actions/workflows/ci-cd.yml)

# Api Projector Backend

## Developing

### Prerequisite
- python 3.10
- poetry

### Getting started 
```bash
git clone git@github.com:api-projector/backend.git
cd backend
make install_pre_commit

cp server/settings/environments/development.py.example server/settings/environments/development.py # prepare default config


poetry install # install deps 
poetry shell # activate the python env

python manage.py migrate # apply migrations to sqlite
python manage.py runserver # run development server 
```

Visit http://localhost:8000 in your browser. The app should be up & running.

### Tests
For tests pytest testing tool is used.

```bash
make test
```

### Code-base structure
```bash
< PROJECT ROOT >
   |
   |-- .github/                              # GitHub workflows
   |    |-- ...
   | 
   |-- ci/                                   # CI related files 
   |    |-- docker-compose.yml               # Run test environment  
   |
   |-- docker/                               # Files to build docker image 
   |    |-- nginx                            # Nginx files
   |    |    |-- nginx.conf                  # Nginx config 
   |    |    |-- uwsgi_params                # Include file for uwsgi params
   |    |
   |    |-- server                           # Server command scripts 
   |    |    |-- backend.sh                  # Run django 
   |    |    |-- celery_beat.sh              # Run celery beat 
   |    |    |-- celery_worker.sh            # Run celery worker 
   |    |    |-- flower.sh                   # Run flower 
   |    | 
   |    |-- .dockerignore.production         # Docker ignore files for production image. Exclude tests 
   |    |-- Dockerfile                       # Dockerfile to test, production image build 
   |    
   |-- locale/      
   |    |-- ...                              # Locale files
   |
   |-- scripts/                              # Tools
   |    |-- lint.sh                          # Lint script 
   |
   |-- server/
   |    |-- apps/                            # Django apps 
   |    |    |-- core                        # Core utils
   |    |    |    |-- ...
   |    |    |
   |    |    |-- media                       # Images, files app 
   |    |    |    |-- ...
   |    |    |
   |    |    |-- projects                    # Projects app
   |    |    |    |-- ...
   |    |    | 
   |    |    |-- user                        # Users app  
   |    |    |    |--..
   |    |    | 
   |    |-- settings/                        # Application settings 
   |    |    |-- components/                 # Settings grouped by components  
   |    |    |    |-- ...     
   |    |    |   
   |    |    |-- environments/               # Specific settings for envs
   |    |    |    |-- build.py               # Docker build settings
   |    |    |    |-- development.py.example # Draft for local development settings (should be cloned to development.py and updated to your environment)
   |    |    |    |-- production.py          # Production settings
   |    |    |    |-- test.py                # CI tests settings
   |    |    |  
   |    |-- celery_app.py                    # Celery entrypoint
   |    |-- gql.py                           # GraphQL routing
   |    |-- urls.py                          # Django routing
   |    |-- wsgi.py                          # WSGI app server entrypoint
   |                               
   |-- tests/                                # Tests folder
   |    |-- ...
   | 
   |-- ...
   |-- .pre-commit-config.yaml               # Pre commit config. To install run: "make install_pre_commit"
   |-- pyproject.toml                        # Poetry deps, tools settings
   |-- setup.cfg                             # Tools settings
   |-- Makefile                              # Useful scripts. To use run: "make <command>" 
   |-- ... 
```

### Django application structure
```bash
< APP ROOT >
   |
   |-- admin/                              # admin panel related modules 
   |    |-- inlines/                       # inlines
   |    |    | ...
   |    |-- ... 
   |    
   |-- graphql/                            # graphql related modules 
   |    |-- mutations
   |    |    |-- ...
   |    |    |-- main.py                   # mutations registration
   |    |-- queries/
   |    |
   |    |    |-- ...
   |    |    |-- main.py                   # queries registration
   |    |
   |    |-- types/                         # graphql types
   |    |    |-- ... 
   |
   |-- logic/                              # business layer logic
   |    |-- commands/ 
   |    |    |-- ...
   |    |    |-- main.py                   # commands registration 
   |    |
   |    |-- queries/
   |    |    |-- ...
   |    |    |-- main.py                   # queries registration 
   |    |
   |    |-- services/ 
   |    |    |-- ...                       # business layer services
   |    |
   |    |-- interfaces/ 
   |    |    |-- ...                       # business layer interfaces 
   |    
   |-- management/                         # django commands
   |    |-- ...                       
   |
   |-- migrations/                         # django database migrations 
   |    |-- ...                       
   | 
   |-- models/                             # models
   |    |-- managers/                      # models managers
   |    |    |-- ...
   |    |
   |    |-- ...
   |
   |-- pages/                              # django views modules
   |    |-- views                          # views 
   |    |     |-- ...
   |    |
   |    |-- urls.py                        # urls routing registration  
   |    
   |-- services/
   |    |-- ...                            # infrastructure layer services
   |
   |-- tasks/
   |    |-- ...                            # async tasks 
   | 
   |-- apps.py                             # application config 
```

### Architecture
The application architecture is implemented as CQRS. The main idea - using commands and queries for communication between layers.

#### Layers
- **business**: main logic, commands, queries, business services,..
- **infrastructure**: auth, couchdb access, graphql, admin,..
 
#### Core ideas
- create command/query and send it to the command/query bus:
```python
from apps.core.logic import commands
from apps.core.logic import queries 

command_result = commands.execute_command(MyCommand(param="test"))
query_result = queries.execute_query(MyQuery(id=1))
```

- no any business logic at admin, django commands, graphql, async tasks,...
- command/query must be simple data object with primitive types
- command/query must return result


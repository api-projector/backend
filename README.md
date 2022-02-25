[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

# Api Projector Backend

## Developing

### Prerequisite
- python 3.10
- poetry

### Setup developing
```bash
git clone git@github.com:api-projector/backend.git
cd backend

cp server/settings/environments/development.py.example server/settings/environments/development.py

poetry install # install deps 
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
   |
```

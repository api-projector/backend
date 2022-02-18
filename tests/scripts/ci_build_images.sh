#!/usr/bin/env sh

set -o errexit
set -o nounset

docker login -u gitlab-ci-token -p $CI_JOB_TOKEN registry.gitlab.com
docker pull $DOCKER_CACHE_IMAGE || true

docker build --cache-from $DOCKER_CACHE_IMAGE -t $DOCKER_TEST_IMAGE -t $DOCKER_CACHE_IMAGE --target test -f deploy/Dockerfile .

cat deploy/.dockerignore.production >> .dockerignore
APP_VERSION=$(cat VERSION)
docker build --cache-from $DOCKER_CACHE_IMAGE -t $DOCKER_IMAGE --target production -f deploy/Dockerfile --build-arg APP_VERSION=${APP_VERSION} .

docker push $DOCKER_TEST_IMAGE
docker push $DOCKER_IMAGE
docker push $DOCKER_CACHE_IMAGE

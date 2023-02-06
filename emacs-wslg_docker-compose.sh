#!/bin/bash
# -*- shell-script -*-
# This script's limitation.
# - can't access to the directories not mounted in docker-compose.yml

# docker-compose.yml's path
COMPOSE_FILE_PATH=~/Codes/emacs-wslg/docker-compose.yml

# defined as default container name in above docker-compose.yml
CONTAINER_NAME=emacs-wslg

function docker_compose_up-d(){
    docker compose \
           -f ${COMPOSE_FILE_PATH} \
           up -d
}

function docker_exec(){
    docker exec \
           -it \
           -w "$(pwd | sed 's:'$HOME':/root:')" \
           ${CONTAINER_NAME} \
           /usr/local/bin/emacs "$@"
}

# try exec or up and exec if failed
docker_exec "$@" || (docker_compose_up-d && docker_exec "$@")

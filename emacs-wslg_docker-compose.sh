#!/bin/bash
# -*- shell-script -*-
# automatically mounts / into /mnt/host
# workdir is corresponds directory in /mnt/host

# docker-compose.yml's path
COMPOSE_FILE_PATH=~/Codes/emacs-wslg/docker-compose.yml

function docker_compose_up-d(){
    docker compose \
           -f ${COMPOSE_FILE_PATH} \
           up -d
}

function docker_exec(){
    docker exec \
           -it \
           -w "$(pwd | sed 's:^/:/mnt/host/:')" \
           emacs-wslg \
           /usr/local/bin/emacs "$@"
}

# try exec or up and exec if failed
docker_exec "$@" && : || (docker_compose_up-d && docker_exec "$@")

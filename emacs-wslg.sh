#!/bin/bash
# -*- shell-script -*-

function inShortTime(){
    local launch=$1
    local restarttime=$2
    [ $(($(date +%s) - launch)) -lt $restarttime ]
}
# try exec or up and exec if failed in 10 seconds
# ignore when execed after 10 seconds
restarttime=10
launch=$(date "+%s")

# automatically mounts / into /mnt/host
# workdir is corresponds directory in /mnt/host
function docker_run_d(){
    docker run \
           --rm \
           --name emacs-wslg \
           -d \
           --entrypoint /usr/bin/sleep \
           -v /:/mnt/host \
           -w "$(pwd | sed 's:^/:/mnt/host/:')" \
           -v ~:/root \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           -v /mnt/wslg:/mnt/wslg \
           -e DISPLAY \
           -e WAYLAND_DISPLAY \
           -e XDG_RUNTIME_DIR \
           -e PULSE_SERVER \
           peccu/emacs-wslg:latest \
           infinity
}

docker exec emacs-wslg emacs "$@" \
    || (\
        inShortTime $launch $restarttime \
            && docker_run_d \
            && docker exec emacs-wslg emacs "$@" \
    )

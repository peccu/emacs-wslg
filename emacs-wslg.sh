#!/bin/bash
# -*- shell-script -*-

# automatically mounts / into /mnt/host
# workdir is corresponds directory in /mnt/host
docker run \
       --rm \
       --name emacs-wslg \
       -it \
       --entrypoint emacs \
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
       "$@"

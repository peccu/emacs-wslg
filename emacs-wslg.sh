#!/bin/bash
# -*- shell-script -*-

# automatically mounts pwd into /app
docker run \
       --rm \
       --name emacs-wslg \
       -it \
       --entrypoint emacs \
       -v $(pwd):/app \
       -w /app \
       -v ~:/root \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       -v /mnt/wslg:/mnt/wslg \
       -e DISPLAY \
       -e WAYLAND_DISPLAY \
       -e XDG_RUNTIME_DIR \
       -e PULSE_SERVER \
       peccu/emacs-wslg:latest \
       "$@"

# emacs-wslg

xwidget enabled Emacs for WSLg.

This docker image can launch emacs with GUI and xwidget.

## Requirements

- WSL2
- Ubuntu 22.04
- some packages in host ubuntu (not tested)
  - `libgtk-3-0`
  - `libgif7`
  - `libwebkit2gtk-4.0-37`

## Usage

launch emacs container with mounts and environments for WSLg.

This sample additionally mounts home directory into `/root`.

- reuse container

run with `sleep infinity`

```bash
docker run \
       --rm \
       --name emacs-wslg \
       -d \
       -v ~:/root \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       -v /mnt/wslg:/mnt/wslg \
       -e DISPLAY \
       -e WAYLAND_DISPLAY \
       -e XDG_RUNTIME_DIR \
       -e PULSE_SERVER \
       peccu/emacs-wslg:latest
```

and exec emacs in it.

```bash
docker exec -it emacs emacs &
```

- launch container each time

```bash
docker run \
       --rm \
       --name emacs-wslg \
       -it \
       --entrypoint emacs \
       -v ~:/root \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       -v /mnt/wslg:/mnt/wslg \
       -e DISPLAY \
       -e WAYLAND_DISPLAY \
       -e XDG_RUNTIME_DIR \
       -e PULSE_SERVER \
       peccu/emacs-wslg:latest
```

- bash scripts
  - always run a new container (copy [`emacs-wslg.sh`](./emacs-wslg.sh) into `/usr/local/bin/emacs-wslg` and add execute permission)
    - this automatically mounts current working directory (`pwd`) into `/app`
```sh
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
```
  - reuse the container with docker-compose version
    - copy [`emacs-wslg_docker-compose.sh`](./emacs-wslg_docker-compose.sh) into `/usr/local/bin/emacs-wslg`
    - add execute permission `sudo chmod +x /usr/local/bin/emacs-wslg`
    - change docker-compose.yml path in the file
    - this script cannot mount current working directory
```sh
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
```

## Some info

Based version is Emacs 29 (emacs-29 branch from emacs mirror git repo).

## TODO
- [ ] emacs server and emacsclient
  - change CMD or ENTRYPOINT into emacs server
- [ ] more emacs versions
- [x] script sample
- [ ] test host dependencies
- [ ] change user in container from root to user


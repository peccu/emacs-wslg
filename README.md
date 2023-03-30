# emacs-wslg

xwidget enabled Emacs for WSLg.

This docker image can launch emacs with GUI and xwidget.

## Requirements

- WSL2
- Ubuntu 22.04

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
  - use exists container or reuse already running container (copy [`emacs-wslg.sh`](./emacs-wslg.sh) into `/usr/local/bin/emacs-wslg` and add execute permission)
    - this automatically mounts current working directory (`pwd`) into `/app`
```sh
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
```
  - reuse the container with docker-compose version
    - copy [`emacs-wslg_docker-compose.sh`](./emacs-wslg_docker-compose.sh) into `/usr/local/bin/emacs-wslg`
    - add execute permission `sudo chmod +x /usr/local/bin/emacs-wslg`
    - change docker-compose.yml path in the file
    - host's root dir (`/`) is mounted in `/mnt/host`
```sh
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
```

## Some info

Based version is Emacs 29 (emacs-29 branch from emacs mirror git repo).

WSLg related document is [here](https://github.com/microsoft/wslg/blob/main/samples/container/Containers.md)

## TODO
- [ ] emacs server and emacsclient
  - change CMD or ENTRYPOINT into emacs server
- [ ] more emacs versions
- [x] script sample
- [x] test host dependencies
  - emacs can run without runtime libs like libgtk
- [ ] change user in container from root to user


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
       --name emacs \
       -d \
       -v ~:/root \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       -v /mnt/wslg:/mnt/wslg \
       -e DISPLAY \
       -e WAYLAND_DISPLAY \
       -e XDG_RUNTIME_DIR \
       -e PULSE_SERVER \
       peccu/wslg-emacs:latest
```

and exec emacs in it.

```bash
docker exec -it emacs emacs &
```

- launch container each time

```bash
docker run \
       --rm \
       --name emacs \
       -it \
       --entrypoint emacs \
       -v ~:/root \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       -v /mnt/wslg:/mnt/wslg \
       -e DISPLAY \
       -e WAYLAND_DISPLAY \
       -e XDG_RUNTIME_DIR \
       -e PULSE_SERVER \
       peccu/wslg-emacs:latest
```

## Some info

Based version is Emacs 29 (emacs-29 branch from emacs mirror git repo).

## TODO
- [ ] emacs server and emacsclient
  - change CMD or ENTRYPOINT into emacs server
- [ ] more emacs versions 
- [ ] script sample
- [ ] test host dependencies

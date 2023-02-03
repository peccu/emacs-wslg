FROM peccu/emacs-wslg:latest as built

RUN cd /tmp/emacs \
  && checkinstall --pkgversion=29 -y

FROM ubuntu:22.04

COPY --from=built /tmp/emacs/src/emacs /usr/local/bin
COPY --from=built /tmp/emacs/emacs_29-1_arm64.deb

# COPY --from=built /tmp/emacs /tmp/emacs

RUN apt-get update \
  && apt-get install -y \
  libgtk-3-0 \
  libgif7 \
  libwebkit2gtk-4.0-37

RUN echo \
    git \
    build-essential \
    libgtk-3-dev \
    libgnutls28-dev \
    libtiff5-dev \
    libgif-dev \
    libjpeg-dev \
    libpng-dev \
    libxpm-dev \
    libncurses-dev \
    texinfo \
    autoconf \
    adwaita-icon-theme-full \
    libwebkit2gtk-4.0-dev \
    checkinstall \
    porg


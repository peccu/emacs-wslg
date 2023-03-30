FROM ubuntu:22.04 as build

RUN apt-get update -y

# install dependencies
RUN apt-get install -y \
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
    porg

# clone
RUN cd /tmp \
    && git clone --single-branch \
    --branch emacs-29 \
    https://github.com/emacs-mirror/emacs.git
# build
RUN cd /tmp/emacs \
    && ./autogen.sh \
    && ./configure \
        --with-pgtk \
        --with-xwidgets \
    && make -j$(nproc)
# install
RUN cd /tmp/emacs \
        && porg -lp emacs-wslg -- make install \
        && porg -f emacs-wslg > installed-files
        # && ls /var/lib/porg/emacs-wslg
# build deb
# https://www.internalpointers.com/post/build-binary-deb-package-practical-guide
# https://stackoverflow.com/questions/8003739/is-there-a-way-to-automatically-determine-dependencies-when-setting-up-a-dpkg-co
ADD control /tmp/emacs-wslg_29.0.60-1_amd64/debian/
ADD changelog /tmp/emacs-wslg_29.0.60-1_amd64/debian/
RUN cat /tmp/emacs/installed-files \
    | tail -n +2 \
    | xargs -I{} dirname {} \
    | sort -u \
    | xargs -I{} mkdir -p /tmp/emacs-wslg_29.0.60-1_amd64/debian/tmp{} \
    && cat /tmp/emacs/installed-files \
    | tail -n +2 \
    | xargs -I{} cp {} /tmp/emacs-wslg_29.0.60-1_amd64/debian/tmp{} \
    && cd /tmp/emacs-wslg_29.0.60-1_amd64 \
    && mkdir debian/tmp/DEBIAN \
    && dpkg-shlibdeps debian/tmp/usr/local/bin/emacs \
    && dpkg-gencontrol -v29.0.60 \
    && dpkg-deb --build --root-owner-group debian/tmp /tmp

FROM ubuntu:22.04

RUN apt-get update -y

# for vGPU container
ENV LD_LIBRARY_PATH=/usr/lib/wsl/lib
RUN apt-get install -y mesa-utils
# CMD /usr/bin/glxinfo -B

# these packages will be installed via deb's dependencies
# RUN apt-get install -y \
#     libgtk-3-0 \
#     libgif7 \
#     libwebkit2gtk-4.0-37

# install Takao font
RUN apt-get install -y \
    fontconfig \
    fonts-takao \
    && fc-cache -fv

COPY --from=build /tmp/emacs-wslg_29.0.60_amd64.deb /tmp/emacs/
RUN apt install -y /tmp/emacs/emacs-wslg_29.0.60_amd64.deb \
    && rm -rf /tmp/emacs

STOPSIGNAL SIGKILL
VOLUME ["/root"]
WORKDIR /root
ENTRYPOINT ["/usr/bin/sleep", "infinity"]

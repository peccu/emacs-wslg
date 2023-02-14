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
    checkinstall \
    porg

# clone
RUN cd /tmp \
    && git clone --single-branch \
    --branch emacs-29 \
    https://github.com/emacs-mirror/emacs.git
RUN cd /tmp/emacs \
    && ./autogen.sh \
    && ./configure \
        --with-pgtk \
        --with-xwidgets \
    && make -j$(nproc) \
    && checkinstall -y \
        --pkgname=emacs-wslg \
        --pkgversion=29 \
        --requires="libgtk-3-0, libgif7, libwebkit2gtk-4.0-37" \
        --install=no
# build deb for rpm (with alien)
# requires are for yum package's name
RUN apt-get install -y alien
RUN cd /tmp/emacs \
        && echo before move \
        && ls \
        && mv ./$(ls emacs-wslg*.deb) ../ \
        && echo after move \
        && ls \
        && echo moved list \
        && ls ../ \
        && echo checkinstall start \
        && checkinstall -y \
        --pkgname=emacs-wslg \
        --pkgversion=29 \
        --requires="gtk3, webkitgtk4, giflib, librsvg2" \
        --install=no \
        && echo "==================== built for alien ====================" \
        && ls \
        && echo run alien \
        && fakeroot alien --to-rpm $(ls emacs-wslg*.deb) \
        && echo "==================== rpm generated ====================" \
        && ls \
        && echo remove deb \
        && echo $(ls emacs-wslg*.deb) \
        && rm $(ls emacs-wslg*.deb) \
        && mv $(ls ../emacs-wslg*.deb) ./
# not supported in debian (requires rpm)
# # create rpm packages too
# RUN cd /tmp/emacs \
#     && checkinstall -y \
#         --type=rpm \
#         --pkgname=emacs-wslg \
#         --pkgversion=29 \
#         --install=no
# RUN cd /tmp/emacs && ls
        # --requires="libgtk-3-0, libgif7, libwebkit2gtk-4.0-37" \
RUN cd /tmp/emacs \
        && porg -lp emacs-wslg --make install \
        && porg -f emacs-wslg > installed-files
# ls /var/lib/porg/emacs-wslg

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

COPY --from=build /tmp/emacs/emacs-wslg_29-1_amd64.deb /tmp/emacs/
COPY --from=build /tmp/emacs/emacs-wslg-29-2.x86_64.rpm /tmp/emacs/
COPY --from=build /tmp/emacs/installed-files /tmp/emacs/
# COPY --from=build /tmp/emacs/emacs-wslg-29-1.x86_64.rpm /tmp/emacs/
RUN apt install -y /tmp/emacs/emacs-wslg_29-1_amd64.deb

STOPSIGNAL SIGKILL
VOLUME ["/root"]
WORKDIR /root
ENTRYPOINT ["/usr/bin/sleep", "infinity"]

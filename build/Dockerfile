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


FROM amazon/aws-cli:latest as build-amazon

# for emacs
RUN yum install -y \
        gzip \
        autoconf \
        make \
        gcc \
        texinfo \
        gtk3-devel \
        webkitgtk4-devel \
        gnutls-devel \
        ncurses-devel \
        libjpeg-turbo-devel \
        libpng-devel \
        libXpm-devel \
        libtiff-devel \
        giflib-devel \
        sqlite-devel \
        librsvg2-devel

# rpmbuild
RUN yum install -y \
        rpm-build \
        rpmdevtools \
        && rpmdev-setuptree


RUN yum install -y \
        jansson-devel \
        libgccjit-devel \
        libotf-devel \
        systemd-devel

# rename directory because source is not released zip
RUN cd /root/rpmbuild/SOURCES \
        && curl -LO https://github.com/emacs-mirror/emacs/archive/refs/heads/emacs-29.zip \
        && unzip emacs-29.zip >/dev/null \
        && rm emacs-29.zip \
        && mv emacs-emacs-29 emacs-29.0.60 \
        && zip -r emacs-29.zip emacs-29.0.60 >/dev/null \
        && rm -rf emacs-29.0.60

        # && cd .. \
        # && spectool -g -R SPECS/emacs.spec \
        # && cd SOURCES \
ADD emacs.spec /root/rpmbuild/SPECS/
# RUN cd /root/rpmbuild/ \
#         && echo skip \
#         && list="$(rpmbuild -bb SPECS/emacs.spec 2>&1 | grep 'is needed by' | awk '{print $1}')" \
#         && echo $list \
#         && if [ ! -z "$list" ] ; then yum install -y $list; fi

RUN cd /root/rpmbuild \
        && rpmbuild -bb SPECS/emacs.spec


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

COPY --from=build /tmp/emacs/emacs-wslg_29.0.60_amd64.deb /tmp/emacs/
COPY --from=build-amazon /root/rpmbuild/RPMS/x86_64/emacs-29.0.60-1.amzn2.x86_64.rpm /tmp/emacs/

RUN apt install -y /tmp/emacs/emacs-wslg_29-1_amd64.deb

STOPSIGNAL SIGKILL
VOLUME ["/root"]
WORKDIR /root
ENTRYPOINT ["/usr/bin/sleep", "infinity"]

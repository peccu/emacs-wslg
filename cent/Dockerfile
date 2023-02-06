FROM centos:7 as checkinstall

# for checkinstall
RUN yum install -y \
        patch \
        make \
        gcc \
        gettext \
        which \
        rpm-build \
        rpmdevtools
# https://topic.alibabacloud.com/a/centos-method-of-using-checkinstall-to-make-rpm-package_1_18_20056714.html
# setup rpmbuild
RUN rpmdev-setuptree

# https://www.patrickmin.com/linux/tip.php?name=checkinstall_fedora_13
ADD checkinstall.patch /tmp
RUN cd /tmp \
        && curl -LO http://checkinstall.izto.org/files/source/checkinstall-1.6.2.tar.gz \
        && tar xf checkinstall-1.6.2.tar.gz \
        && patch -p0 < checkinstall.patch \
        && cd checkinstall-1.6.2 \
        && make \
        && make install \
        && checkinstall -y \
        --type=rpm \
        --requires="rpm-build, rpmdevtools, which" \
        && mv /root/rpmbuild/RPMS/x86_64/checkinstall-1.6.2-1.x86_64.rpm ../

FROM centos:7 as build

RUN yum install -y git-core
# clone
RUN cd /tmp \
    && git clone --single-branch \
    --branch emacs-29 \
    https://github.com/emacs-mirror/emacs.git

# for emacs
RUN yum install -y \
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

# build emacs
RUN cd /tmp/emacs \
        && ./autogen.sh \
        && ./configure \
        --with-pgtk \
        --with-xwidgets \
        && make -j$(nproc) \
        && make install

# setup checkinstall
COPY --from=checkinstall /tmp/checkinstall-1.6.2-1.x86_64.rpm /tmp
RUN cd /tmp \
        && yum install -y checkinstall-1.6.2-1.x86_64.rpm \
        && cd /usr/local/lib64 \
        && echo "/usr/local/lib64" > /etc/ld.so.conf.d/installwatch.conf \
        && ldconfig \
        && ln -s ../lib/installwatch.so \
        && rpmdev-setuptree
RUN cd /tmp/emacs \
        && checkinstall -y \
        --type=rpm \
        --pkgname=emacs-wslg \
        --pkgversion=29 \
        --install=no \
        -- make install
        # --requires="gtk3, webkitgtk4" \
RUN cd /tmp/emacs && ls

FROM centos:7 as runtime

# libEGL warning: DRI2: failed to open swrast (search paths /usr/lib64/dri)
# EGLDisplay Initialization failed: EGL_NOT_INITIALIZED

COPY --from=build /tmp/emacs/src/emacs /usr/local/bin/
# COPY --from=build /tmp/emacs/emacs-wslg-29-1.x86_64.rpm /tmp/emacs
# RUN yum install -y /tmp/emacs/emacs-wslg-29-1.x86_64.rpm

# for vGPU container
ENV LD_LIBRARY_PATH=/usr/lib/wsl/lib
# RUN apt-get install -y mesa-utils
# CMD /usr/bin/glxinfo -B

# these packages will be installed via deb's dependencies
RUN yum install -y \
        gtk3 \
        webkitgtk4 \
        giflib \
        librsvg2

# # RUN apt-get install -y \
# #     libgtk-3-0 \
# #     libgif7 \
# #     libwebkit2gtk-4.0-37

# # # install Takao font
# # RUN apt-get install -y \
# #     fontconfig \
# #     fonts-takao \
# #     && fc-cache -fv
RUN yum install -y \
        fontconfig \
        ipa-gothic-fonts \
        ipa-mincho-fonts \
        ipa-pmincho-fonts \
        ipa-pgothic-fonts \
        && fc-cache -fv

# STOPSIGNAL SIGKILL
# VOLUME ["/root"]
# WORKDIR /root
# ENTRYPOINT ["/usr/bin/sleep", "infinity"]

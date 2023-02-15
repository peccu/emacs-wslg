FROM amazon/aws-cli:latest as build-amazon

# for emacs
RUN yum install -y \
        autoconf \
        gcc \
        giflib-devel \
        gnutls-devel \
        gtk3-devel \
        gzip \
        jansson-devel \
        libXpm-devel \
        libgccjit-devel \
        libjpeg-turbo-devel \
        libotf-devel \
        libpng-devel \
        librsvg2-devel \
        libtiff-devel \
        make \
        ncurses-devel \
        sqlite-devel \
        systemd-devel \
        texinfo \
        webkitgtk4-devel

# rpmbuild
RUN yum install -y \
        rpm-build \
        rpmdevtools \
        && rpmdev-setuptree

RUN cd /root/rpmbuild/SOURCES \
        && curl -LO https://github.com/emacs-mirror/emacs/archive/refs/heads/emacs-29.zip \
        && unzip emacs-29.zip >/dev/null \
        && rm emacs-29.zip \
        && mv emacs-emacs-29 emacs-29.0.60 \
        && zip -r emacs-29.zip emacs-29.0.60 >/dev/null \
        && rm -rf emacs-29.0.60 \
        && cd ..

ADD emacs.spec /root/rpmbuild/SPECS/

# download sources. but current Source's directory name does not contain version number
# RUN cd /root/rpmbuild \
#         && spectool -g -R SPECS/emacs.spec

# install build requires
# RUN cd /root/rpmbuild \
#         && list="$(rpmbuild -bb SPECS/emacs.spec 2>&1 | grep 'is needed by' | awk '{print $1}')" \
#         && echo $list \
#         && if [ ! -z "$list" ] ; then yum install -y $list; fi

RUN cd /root/rpmbuild \
        && rpmbuild -bb SPECS/emacs.spec

FROM amazon/aws-cli:latest as runtime-amazon

COPY --from=build /root/rpmbuild/RPMS/x86_64/emacs-29.0.60-1.amzn2.x86_64.rpm /tmp/emacs/
RUN yum install -y /tmp/emacs/emacs-29.0.60-1.amzn2.x86_64.rpm

# for vGPU container
ENV LD_LIBRARY_PATH=/usr/lib/wsl/lib
# CMD /usr/bin/glxinfo -B


FROM centos:7 as build-centos

# for emacs
RUN yum install -y \
        autoconf \
        gcc \
        giflib-devel \
        gnutls-devel \
        gtk3-devel \
        gzip \
        jansson-devel \
        libXpm-devel \
        libgccjit-devel \
        libjpeg-turbo-devel \
        libotf-devel \
        libpng-devel \
        librsvg2-devel \
        libtiff-devel \
        make \
        ncurses-devel \
        sqlite-devel \
        systemd-devel \
        texinfo \
        webkitgtk4-devel

# rpmbuild
RUN yum install -y \
        rpm-build \
        rpmdevtools \
        && rpmdev-setuptree

RUN cd /root/rpmbuild/SOURCES \
        && curl -LO https://github.com/emacs-mirror/emacs/archive/refs/heads/emacs-29.zip \
        && unzip emacs-29.zip >/dev/null \
        && rm emacs-29.zip \
        && mv emacs-emacs-29 emacs-29.0.60 \
        && zip -r emacs-29.zip emacs-29.0.60 >/dev/null \
        && rm -rf emacs-29.0.60 \
        && cd ..

ADD emacs.spec /root/rpmbuild/SPECS/

# download sources. but current Source's directory name does not contain version number
# RUN cd /root/rpmbuild \
#         && spectool -g -R SPECS/emacs.spec

# install build requires
# RUN cd /root/rpmbuild \
#         && list="$(rpmbuild -bb SPECS/emacs.spec 2>&1 | grep 'is needed by' | awk '{print $1}')" \
#         && echo $list \
#         && if [ ! -z "$list" ] ; then yum install -y $list; fi

RUN cd /root/rpmbuild \
        && rpmbuild -bb SPECS/emacs.spec









# FROM centos:7 as runtime
# COPY --from=build /tmp/emacs/src/emacs /usr/local/bin/
# COPY --from=build /tmp/emacs/emacs-wslg-29-2.x86_64.rpm /tmp/emacs
# RUN yum install -y /tmp/emacs/emacs-wslg-29-2.x86_64.rpm


# # these packages will be installed via deb's dependencies
# RUN yum install -y \
#         gtk3 \
#         webkitgtk4 \
#         giflib \
#         librsvg2
# for vGPU container
# RUN yum install -y mesa-libGLw

# # install fonts
# RUN yum install -y \
#         fontconfig \
#         ipa-gothic-fonts \
#         ipa-mincho-fonts \
#         ipa-pmincho-fonts \
#         ipa-pgothic-fonts \
#         && fc-cache -fv

# STOPSIGNAL SIGKILL
# VOLUME ["/root"]
# WORKDIR /root
# ENTRYPOINT ["/usr/bin/sleep", "infinity"]

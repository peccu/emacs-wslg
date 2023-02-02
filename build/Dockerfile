FROM ubuntu:22.04
# install Takao font
RUN apt update -y
RUN apt install -y \
    fontconfig \
    fonts-takao \
    && fc-cache -fv

# install dependencies
RUN apt install -y \
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
    libwebkit2gtk-4.0-dev

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
    && make -j8 \
    && make install

# cleanup
RUN rm -rf /tmp/emacs

# for vGPU container
ENV LD_LIBRARY_PATH=/usr/lib/wsl/lib
RUN apt install -y mesa-utils
# CMD /usr/bin/glxinfo -B

STOPSIGNAL SIGKILL
VOLUME ["/root"]
WORKDIR /root
ENTRYPOINT ["/usr/bin/sleep", "infinity"]

%global _hardened_build 1
%global __python %{__python3}

# This file is encoded in UTF-8.  -*- coding: utf-8 -*-
Summary:       GNU Emacs text editor
Name:          emacs
Epoch:         1
Version:       29.0.60
Release:       1%{?dist}
License:       GPLv3+ and CC0
URL:           http://www.gnu.org/software/emacs/
Source0:       https://github.com/emacs-mirror/emacs/archive/refs/heads/emacs-29.zip

BuildRequires: atk-devel
BuildRequires: autoconf
BuildRequires: bzip2
BuildRequires: cairo
BuildRequires: cairo-devel
BuildRequires: dbus-devel
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: gcc
BuildRequires: giflib-devel
BuildRequires: glibc-devel
BuildRequires: gnupg2
BuildRequires: gnutls-devel
BuildRequires: gtk3-devel
BuildRequires: gzip
BuildRequires: harfbuzz-devel
BuildRequires: jansson-devel
BuildRequires: libX11-devel
BuildRequires: libXau-devel
BuildRequires: libXpm-devel
BuildRequires: libXrender-devel
%if "%{dist}" == ".amzn2"
BuildRequires: libgccjit-devel
%endif
%if "%{dist}" == ".el7"
# needs `yum install -y centos-release-scl`
BuildRequires: devtoolset-9-libgccjit-devel
%endif
BuildRequires: libjpeg-turbo
BuildRequires: libjpeg-turbo-devel
BuildRequires: libotf-devel
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel
BuildRequires: libtiff-devel
BuildRequires: libxml2-devel
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: systemd-devel
BuildRequires: texinfo
BuildRequires: webkitgtk4-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: zlib-devel

%ifarch %{ix86}
BuildRequires: util-linux
%endif

# Emacs requires info for info mode, rhbz#1989264
Requires:      info
# Emacs doesn't run without dejavu-sans-mono-fonts, rhbz#732422
Requires:      dejavu-sans-mono-fonts
%if "%{dist}" == ".amzn2"
Requires: libgccjit-devel
%endif
%if "%{dist}" == ".el7"
Requires: devtoolset-9-libgccjit-devel
%endif
Requires:      gtk3
Requires:      webkitgtk4
Requires:      giflib
Requires:      librsvg2
Requires:      mesa-libGLw

%define site_lisp %{_datadir}/emacs/site-lisp
%define site_start_d %{site_lisp}/site-start.d
%define bytecompargs -batch --no-init-file --no-site-file -f batch-byte-compile
%define pkgconfig %{_datadir}/pkgconfig
%define emacs_libexecdir %{_libexecdir}/emacs/%{version}/%{_host}
%define native_lisp %{_libdir}/emacs/%{version}/native-lisp

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with support for X windows.

%prep
%setup -q

pwd
ls
bash autogen.sh

%ifarch %{ix86}
%define setarch setarch %{_arch} -R
%else
%define setarch %{nil}
%endif

%build
whoami

LDFLAGS=-Wl,-z,relro;  export LDFLAGS;

%if "%{dist}" == ".el7"
source /opt/rh/devtoolset-9/enable
PKG_CONFIG_PATH=/usr/lib64/pkgconfig:$PKG_CONFIG_PATH
export PKG_CONFIG_PATH
%endif

./configure --with-dbus --with-gif --with-jpeg --with-png --with-rsvg \
           --with-tiff --with-xpm --with-x-toolkit=gtk3 --with-gpm=no \
           --with-xwidgets --with-modules --with-harfbuzz --with-cairo --with-json \
           --with-native-compilation
%{setarch} %make_build bootstrap NATIVE_FULL_AOT=1
%{setarch} %make_build

%install
%make_install

%files
/usr/local/bin/*
/usr/local/include/emacs-module.h
/usr/local/lib/emacs/%{version}/native-lisp/*
/usr/local/libexec/emacs/%{version}/x86_64-pc-linux-gnu/*
/usr/local/lib/systemd/user/emacs.service
/usr/local/share/applications/*
/usr/local/share/emacs/%{version}/*
/usr/local/share/emacs/site-lisp/subdirs.el
/usr/local/share/icons/hicolor/*
/usr/local/share/info/*
/usr/local/share/man/man1/*
/usr/local/share/metainfo/emacs.metainfo.xml

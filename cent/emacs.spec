%global _hardened_build 1

# This file is encoded in UTF-8.  -*- coding: utf-8 -*-
Summary:       GNU Emacs text editor
Name:          emacs
Epoch:         1
Version:       29.0
Release:       1%{?dist}
License:       GPLv3+ and CC0
URL:           http://www.gnu.org/software/emacs/
Source0:       https://github.com/emacs-mirror/emacs/archive/refs/heads/emacs-29.zip

BuildRequires: gcc
BuildRequires: atk-devel
BuildRequires: cairo-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: dbus-devel
BuildRequires: giflib-devel
BuildRequires: glibc-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libjpeg-turbo
BuildRequires: libtiff-devel
BuildRequires: libX11-devel
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel
BuildRequires: libXrender-devel
BuildRequires: libXt-devel
BuildRequires: libXpm-devel
BuildRequires: ncurses-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: zlib-devel
BuildRequires: gnutls-devel
BuildRequires: librsvg2-devel
BuildRequires: m17n-lib-devel
BuildRequires: libotf-devel
BuildRequires: libselinux-devel
BuildRequires: alsa-lib-devel
BuildRequires: gpm-devel
BuildRequires: liblockfile-devel
BuildRequires: libxml2-devel
BuildRequires: autoconf
BuildRequires: bzip2
BuildRequires: cairo
BuildRequires: texinfo
BuildRequires: gzip
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: libacl-devel
BuildRequires: harfbuzz-devel
BuildRequires: jansson-devel
BuildRequires: systemd-devel
BuildRequires: libgccjit-devel

BuildRequires: gtk3-devel
BuildRequires: webkitgtk4-devel

BuildRequires: gnupg2

# For lucid
BuildRequires: Xaw3d-devel

# for Patch3
BuildRequires: pkgconfig(systemd)

%ifarch %{ix86}
BuildRequires: util-linux
%endif
BuildRequires: make

# Emacs requires info for info mode, rhbz#1989264
Requires:      info
# Emacs doesn't run without dejavu-sans-mono-fonts, rhbz#732422
Requires:      desktop-file-utils
Requires:      dejavu-sans-mono-fonts
Requires:      libgccjit
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      emacs-common = %{epoch}:%{version}-%{release}
Provides:      emacs(bin) = %{epoch}:%{version}-%{release}

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

%package common
Summary:       Emacs common files
# The entire source code is GPLv3+ except lib-src/etags.c which is
# also BSD.  Manual (info) is GFDL.
License:       GPLv3+ and GFDL and BSD
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      %{name}-filesystem = %{epoch}:%{version}-%{release}
Recommends:    enchant2
Provides:      %{name}-el = %{epoch}:%{version}-%{release}
Obsoletes:     emacs-el < 1:24.3-29
# transient.el is provided by emacs in lisp/transient.el
Provides:      emacs-transient = 0.3.7
# the existing emacs-transient package is obsoleted by emacs 28+, last package
# version as of the release of emacs 28.1 is obsoleted
Obsoletes:     emacs-transient < 0.3.0-4

%description common
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package contains all the common files needed by emacs, emacs-lucid
or emacs-nox.

%prep
%setup -q

autoconf

%ifarch %{ix86}
%define setarch setarch %{_arch} -R
%else
%define setarch %{nil}
%endif

%build
export CFLAGS="-DMAIL_USE_LOCKF %{build_cflags}"
%set_build_flags

# Build GTK+ binary
mkdir build-gtk && cd build-gtk
ln -s ../configure .

LDFLAGS=-Wl,-z,relro;  export LDFLAGS;

%configure --with-dbus --with-gif --with-jpeg --with-png --with-rsvg \
           --with-tiff --with-xpm --with-x-toolkit=gtk3 --with-gpm=no \
           --with-xwidgets --with-modules --with-harfbuzz --with-cairo --with-json \
           --with-native-compilation
%{setarch} %make_build bootstrap NATIVE_FULL_AOT=1
%{setarch} %make_build
cd ..

# Create pkgconfig file
cat > emacs.pc << EOF
sitepkglispdir=%{site_lisp}
sitestartdir=%{site_start_d}

Name: emacs
Description: GNU Emacs text editor
Version: %{epoch}:%{version}
EOF

# Create macros.emacs RPM macro file
cat > macros.emacs << EOF
%%_emacs_version %{version}
%%_emacs_ev %{?epoch:%{epoch}:}%{version}
%%_emacs_evr %{?epoch:%{epoch}:}%{version}-%{release}
%%_emacs_sitelispdir %{site_lisp}
%%_emacs_sitestartdir %{site_start_d}
%%_emacs_bytecompile /usr/bin/emacs -batch --no-init-file --no-site-file --eval '(progn (setq load-path (cons "." load-path)))' -f batch-byte-compile
EOF

%install
cd build-gtk
%make_install
cd ..

# Let alternatives manage the symlink
rm %{buildroot}%{_bindir}/emacs
touch %{buildroot}%{_bindir}/emacs

# Do not compress the files which implement compression itself (#484830)
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-compr.el.gz
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-cmpr-hook.el.gz

# Make sure movemail isn't setgid
chmod 755 %{buildroot}%{emacs_libexecdir}/movemail

mkdir -p %{buildroot}%{site_lisp}

# This solves bz#474958, "update-directory-autoloads" now finally
# works the path is different each version, so we'll generate it here
echo "(setq source-directory \"%{_datadir}/emacs/%{version}/\")" \
 >> %{buildroot}%{site_lisp}/site-start.el

mv %{buildroot}%{_bindir}/{etags,etags.emacs}
mv %{buildroot}%{_mandir}/man1/{ctags.1.gz,gctags.1.gz}
mv %{buildroot}%{_mandir}/man1/{etags.1.gz,etags.emacs.1.gz}
mv %{buildroot}%{_bindir}/{ctags,gctags}
# BZ 927996
mv %{buildroot}%{_infodir}/{info.info.gz,info.gz}

mkdir -p %{buildroot}%{site_lisp}/site-start.d

# Default initialization file
mkdir -p %{buildroot}%{_sysconfdir}/skel

# Install pkgconfig file
mkdir -p %{buildroot}/%{pkgconfig}
install -p -m 0644 emacs.pc %{buildroot}/%{pkgconfig}

# Install rpm macro definition file
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 0644 macros.emacs %{buildroot}%{_rpmconfigdir}/macros.d/

# After everything is installed, remove info dir
rm -f %{buildroot}%{_infodir}/dir

#
# Create file lists
#
rm -f *-filelist {common,el}-*-files

( TOPDIR=${PWD}
  cd %{buildroot}

  find .%{_datadir}/emacs/%{version}/lisp \
    .%{_datadir}/emacs/%{version}/lisp/leim \
    .%{_datadir}/emacs/site-lisp \( -type f -name '*.elc' -fprint $TOPDIR/common-lisp-none-elc-files \) -o \( -type d -fprintf $TOPDIR/common-lisp-dir-files "%%%%dir %%p\n" \) -o \( -name '*.el.gz' -fprint $TOPDIR/el-bytecomped-files -o -fprint $TOPDIR/common-not-comped-files \)

)

# Sorted list of info files
%define info_files auth autotype bovine calc ccmode cl dbus dired-x ebrowse ede ediff edt efaq eieio eintr elisp emacs-gnutls emacs-mime emacs epa erc ert eshell eudc eww flymake forms gnus htmlfontify idlwave ido mairix-el message mh-e modus-themes newsticker nxml-mode octave-mode org pcl-cvs pgg rcirc reftex remember sasl sc semantic ses sieve smtpmail speedbar srecode todo-mode tramp transient url vhdl-mode vip viper widget wisent woman

for info_f in %info_files; do
    echo "%{_infodir}/${info_f}.info*" >> info-filelist
done
# info.gz is a rename of info.info.gz and thus needs special handling
echo "%{_infodir}/info*" >> info-filelist

# Put the lists together after filtering  ./usr to /usr
sed -i -e "s|\.%{_prefix}|%{_prefix}|" *-files
cat common-*-files > common-filelist
cat el-*-files common-lisp-dir-files > el-filelist

# Remove old icon
rm %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document23.svg

# Install all the pdmp with fingerprints
gtk_pdmp="emacs-$(./build-gtk/src/emacs --fingerprint 2>&1 | sed 's/.* //').pdmp"
install -p -m 0644 build-gtk/src/emacs.pdmp %{buildroot}%{emacs_libexecdir}/${gtk_pdmp}

# Install native compiled Lisp of all builds
gtk_comp_native_ver=$(ls -1 build-gtk/native-lisp)
cp -ar build-gtk/native-lisp/${gtk_comp_native_ver} %{buildroot}%{native_lisp}
(TOPDIR=${PWD}
 cd %{buildroot}
 find .%{native_lisp}/${gtk_comp_native_ver} \( -type f -name '*eln' -fprintf $TOPDIR/gtk-eln-filelist "%%%%attr(755,-,-) %%p\n" \) -o \( -type d -fprintf $TOPDIR/gtk-dirs "%%%%dir %%p\n" \)
)
echo %{emacs_libexecdir}/${gtk_pdmp} >> gtk-eln-filelist

# remove leading . from filelists
sed -i -e "s|\.%{native_lisp}|%{native_lisp}|" *-eln-filelist *-dirs

# remove exec permissions from eln files to prevent the debuginfo extractor from
# trying to extract debuginfo from them
find %{buildroot}%{_libdir}/ -name '*eln' -type f | xargs chmod -x

# ensure native files are newer than byte-code files
# see: https://bugzilla.redhat.com/show_bug.cgi?id=2157979#c11
find %{buildroot}%{_libdir}/ -name '*eln' -type f | xargs touch

%check

%preun
%{_sbindir}/alternatives --remove emacs %{_bindir}/emacs-%{version} || :

%posttrans
%{_sbindir}/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-%{version} 80 || :

%preun common
%{_sbindir}/alternatives --remove emacs.etags %{_bindir}/etags.emacs || :

%posttrans common
%{_sbindir}/alternatives --install %{_bindir}/etags emacs.etags %{_bindir}/etags.emacs 80 \
       --slave %{_mandir}/man1/etags.1.gz emacs.etags.man %{_mandir}/man1/etags.emacs.1.gz || :

%files -f gtk-eln-filelist -f gtk-dirs
%{_bindir}/emacs-%{version}
%attr(0755,-,-) %ghost %{_bindir}/emacs
%{_metainfodir}/%{name}.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/emacs.png
%{_datadir}/icons/hicolor/scalable/apps/emacs.svg
%{_datadir}/icons/hicolor/scalable/apps/emacs.ico
%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document.svg

%files common -f common-filelist -f el-filelist -f info-filelist
%config(noreplace) %{_sysconfdir}/skel/.emacs
%{_rpmconfigdir}/macros.d/macros.emacs
%license etc/COPYING
%doc doc/NEWS BUGS README
%{_bindir}/ebrowse
%{_bindir}/emacsclient
%{_bindir}/etags.emacs
%{_bindir}/gctags
%{_mandir}/man1/ebrowse.1*
%{_mandir}/man1/emacs.1*
%{_mandir}/man1/emacsclient.1*
%{_mandir}/man1/etags.emacs.1*
%{_mandir}/man1/gctags.1*
%dir %{_datadir}/emacs/%{version}
%{_datadir}/emacs/%{version}/etc
%{_datadir}/emacs/%{version}/site-lisp
%dir %{emacs_libexecdir}/
%{emacs_libexecdir}/movemail
%{emacs_libexecdir}/hexl
%{emacs_libexecdir}/rcs2log
%{_userunitdir}/emacs.service
%attr(0644,root,root) %config(noreplace) %{_datadir}/emacs/site-lisp/default.el
%attr(0644,root,root) %config %{_datadir}/emacs/site-lisp/site-start.el
%{pkgconfig}/emacs.pc

%files filesystem
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/site-lisp
%dir %{_datadir}/emacs/site-lisp/site-start.d

%define kbddir %{_prefix}/lib/kbd

Name:   	kbd
Version:	1.12
Release:	%mkrel 1
Summary:	Keyboard and console utilities for Linux
License:	GPL
Group:  	Terminals
URL:    	ftp://ftp.win.tue.nl/pub/linux-local/utils/kbd/
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kbd/kbd-%version.tar.bz2
Source1:	ftp://ftp.kernel.org/pub/linux/utils/kbd/kbd-%version.tar.bz2.sign
Source2:	ucwfonts.tar.bz2
# mandriva keyboard updates
Patch0: 	kbd-1.12-mandriva.patch
# tilde with twosuperior in french keyboard
Patch1: 	kbd-1.12-tilde_twosuperior_french_kbd.patch
# some modifications to cover PPC using Linux keycodes
Patch2: 	kbd-1.12-ppc_using_linux_keycodes.patch
# thai support, I tried to convert it from console-tools package
# (support added by Pablo), using also updated thay_ksym patch from
# debian and the following patches from:
# http://linux.thai.net/~thep/th-console/console-tools/console-tools-thai_ksym.patch
# http://linux.thai.net/~thep/th-console/console-data/console-data-thai_orig-1999.08.29.patch
Patch3: 	kbd-1.12-thai_ksym_deb.patch
Patch4: 	kbd-1.12-data_thai.patch
# input characters in utf8 mode when console is set to utf8 mode
Patch5: 	kbd-1.12-stty_iutf8.patch
BuildRoot:	%_tmppath/%name-buildroot
BuildRequires:	gcc
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel
BuildRequires:	make

%description
This package contains utilities to load console fonts and keyboard maps.
It also includes a number of different fonts and keyboard maps.

%prep
%setup -q -a 2
%patch0 -p1
%patch1 -p1
%ifarch ppc ppc64
%patch2 -p1
%endif
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
./configure --datadir=%kbddir --mandir=%_mandir
%make

%install
rm -rf %buildroot
make DESTDIR=%buildroot install

# keep compatibility with console-tools
ln -s fr-latin9.map.gz \
      %buildroot/usr/lib/kbd/keymaps/i386/azerty/fr-latin0.map.gz

%find_lang %name

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(0755,root,root,0755)
%{_bindir}/chvt
%{_bindir}/deallocvt
%{_bindir}/dumpkeys
%{_bindir}/fgconsole
%{_bindir}/getkeycodes
%{_bindir}/kbd_mode
%{_bindir}/kbdrate
%{_bindir}/loadunimap
%{_bindir}/mapscrn
%{_bindir}/openvt
%{_bindir}/psfaddtable
%{_bindir}/psfgettable
%{_bindir}/psfstriptable
%{_bindir}/psfxtable
%{_bindir}/resizecons
%{_bindir}/setfont
%{_bindir}/setkeycodes
%{_bindir}/setleds
%{_bindir}/setmetamode
%{_bindir}/showconsolefont
%{_bindir}/showkey
%{_bindir}/unicode_start
%{_bindir}/unicode_stop
/bin/loadkeys
%defattr(0644,root,root,0755)
%{_mandir}/man1/chvt.1*
%{_mandir}/man1/deallocvt.1*
%{_mandir}/man1/dumpkeys.1*
%{_mandir}/man1/fgconsole.1*
%{_mandir}/man1/kbd_mode.1*
%{_mandir}/man1/loadkeys.1*
%{_mandir}/man1/openvt.1*
%{_mandir}/man1/psfaddtable.1*
%{_mandir}/man1/psfgettable.1*
%{_mandir}/man1/psfstriptable.1*
%{_mandir}/man1/psfxtable.1*
%{_mandir}/man1/setleds.1*
%{_mandir}/man1/setmetamode.1*
%{_mandir}/man1/showkey.1*
%{_mandir}/man1/unicode_start.1*
%{_mandir}/man1/unicode_stop.1*
%{_mandir}/man5/keymaps.5*
%{_mandir}/man8/getkeycodes.8*
%{_mandir}/man8/kbdrate.8*
%{_mandir}/man8/loadunimap.8*
%{_mandir}/man8/mapscrn.8*
%{_mandir}/man8/resizecons.8*
%{_mandir}/man8/setfont.8*
%{_mandir}/man8/setkeycodes.8*
%{_mandir}/man8/showconsolefont.8*
%{kbddir}

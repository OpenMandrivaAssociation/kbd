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
BuildRoot:	%_tmppath/%name-buildroot
BuildRequires:	gcc
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel
BuildRequires:	make

%description
This package contains utilities to load console fonts and keyboard maps.
It also includes a number of different fonts and keyboard maps.

%prep
%setup -q

%build
./configure --datadir=%kbddir --mandir=%_mandir
%make

%install
rm -rf %buildroot
make DESTDIR=%buildroot install
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

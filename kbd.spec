%define kbddir /usr/lib/kbd
%define mdv_keymaps_ver 20081113

Name:		kbd
Version:	1.15.5
Release:	1
Summary:	Keyboard and console utilities for Linux
License:	GPLv2+
Group:		Terminals
URL:		http://www.kbd-project.org/
Source0:	ftp://ftp.altlinux.org/pub/people/legion/kbd/%{name}-%{version}.tar.gz
Source2:	ucwfonts.tar.bz2
Source3:	ftp://ftp.linux-france.org/pub/macintosh/kbd-mac-fr-4.1.tar.gz
Source5:	kbd-mdv-keymaps-%{mdv_keymaps_ver}.tar.bz2
Source6:	configure_keyboard.sh
Source7:	setsysfont
# mandriva keyboard updates
Patch0:		kbd-1.15-mandriva.patch
# tilde with twosuperior in french keyboard
Patch1:		kbd-1.15-tilde_twosuperior_french_kbd.patch
# some modifications to cover PPC using Linux keycodes
Patch2:		kbd-1.12-ppc_using_linux_keycodes.patch
# thai support, I tried to convert it from console-tools package
# (support added by Pablo), see these patches as reference:
# http://linux.thai.net/~thep/th-console/console-tools/console-tools-thai_ksym.patch
# http://linux.thai.net/~thep/th-console/console-data/console-data-thai_orig-1999.08.29.patch
# (note: thai_ksym patch not needed anymore, it's merged in kbd)
Patch4:		kbd-1.12-data_thai.patch
# avoid kbd scheme for loadkeys, we use unicode_start in configure_keyboard.sh
Patch5:		kbd-1.14.1-unicode_start_no_loadkeys.patch
# (fc) remove unneeded calls in unicode_stop
Patch6:		kbd-1.15-remove-unneeded-calls.patch
# (fc) allow to wait for VT switch in userland (Novell bug #540482) (Gentoo)
Patch7:		kbd-1.12-chvt-userwait.patch

# Fedora patches
# Patch0: puts additional information into man pages
Patch100:         kbd-1.15-keycodes-man.patch
# Patch1: sparc modifications
Patch101:         kbd-1.15-sparc.patch
# Patch2: adds default unicode font to unicode_start script
Patch102:         kbd-1.15-unicode_start.patch
# Patch3: add missing dumpkeys option to man page
Patch103:         kbd-1.15.3-dumpkeys-man.patch
# Patch4: fixes loadkeys regression (already upstream)
Patch104:         kbd-1.15.5-loadkeys-regression.patch
# Patch5: fixes decimal separator in Swiss German keyboard layout, bz 882529
Patch105:         kbd-1.15.5-sg-decimal-separator.patch

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel
BuildRequires:	make
Conflicts:	initscripts <= 8.54-2mdv2008.0
Conflicts:	util-linux < 2.13
Obsoletes:	console-tools <= 0.2.3-64
Obsoletes:	libconsole0 <= 0.2.3-64
Obsoletes:	libconsole0-devel <= 0.2.3-64
Obsoletes:	libconsole0-static-devel <= 0.2.3-64
Obsoletes:	lib64console0 <= 0.2.3-64
Obsoletes:	lib64console0-devel <= 0.2.3-64
Obsoletes:	lib64console0-static-devel <= 0.2.3-64

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
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%patch100 -p1 -b .keycodes-man~
%patch101 -p1 -b .sparc~
%patch102 -p1 -b .unicode_start~
%patch103 -p1 -b .dumpkeys-man~
%patch104 -p1 -b .loadkeys-regression~
%patch105 -p1 -b .sg-decimal-separator~

mkdir mac_frnew; cd mac_frnew
tar -zxf %{SOURCE3}
gunzip mac-fr-ext_new.kmap.gz
mv mac-fr-ext_new.kmap ../data/keymaps/mac/all/mac-fr-ext_new.map
cd ..; rm -rf mac_frnew

pushd data
tar -jxf %{SOURCE5}
cp keymaps/i386/include/delete.inc keymaps/i386/include/delete.map
popd

%build
%configure2_5x	--datadir=%{kbddir} \
		--localedir=%{_localedir} \
		--enable-nls \
		--enable-optional-progs \
		--disable-rpath

%make

%install
%makeinstall_std localedir=%{_localedir}

# keep some keymap/consolefonts compatibility with console-tools
ln -s fr-latin9.map.gz \
	%{buildroot}%{kbddir}/keymaps/i386/azerty/fr-latin0.map.gz
ln -s us-acentos.map.gz \
	%{buildroot}%{kbddir}/keymaps/i386/qwerty/us-intl.map.gz
ln -s mac-us.map.gz \
	%{buildroot}%{kbddir}/keymaps/mac/all/mac-br-abnt2.map.gz
ln -s mac-us.map.gz \
	%{buildroot}%{kbddir}/keymaps/mac/all/mac-gr.map.gz
ln -s mac-us.map.gz \
	%{buildroot}%{kbddir}/keymaps/mac/all/mac-no-latin1.map.gz
ln -s mac-us.map.gz \
	%{buildroot}%{kbddir}/keymaps/mac/all/mac-cz-us-qwertz.map.gz
ln -s mac-us.map.gz \
	%{buildroot}%{kbddir}/keymaps/mac/all/mac-hu.map.gz
ln -s mac-us.map.gz \
	%{buildroot}%{kbddir}/keymaps/mac/all/mac-Pl02.map.gz
ln -s mac-us.map.gz \
	%{buildroot}%{kbddir}/keymaps/mac/all/mac-ru1.map.gz
ln -s mac-us.map.gz \
	%{buildroot}%{kbddir}/keymaps/mac/all/mac-jp106.map.gz
ln -s iso07u-16.psfu.gz \
	%{buildroot}%{kbddir}/consolefonts/iso07.f16.psfu.gz
ln -s lat2-16.psfu.gz \
	%{buildroot}%{kbddir}/consolefonts/lat2-sun16.psfu.gz
ln -s lat5-16.psfu.gz \
	%{buildroot}%{kbddir}/consolefonts/lat5u-16.psfu.gz

# Our initscripts/drakx-kbd-mouse-x11 may want to load these directly as
# they were like this when using console-tools (GRP_TOGGLE), so we do
# this to keep compatibility (#32284)
for toggle_file in alt_shift_toggle caps_toggle ctrl_alt_toggle \
                   ctrl_shift_toggle lwin_toggle menu_toggle \
                   rwin_toggle toggle
do
	cp %{buildroot}%{kbddir}/keymaps/i386/include/$toggle_file.inc \
	   %{buildroot}%{kbddir}/keymaps/i386/include/$toggle_file.map
	gzip %{buildroot}%{kbddir}/keymaps/i386/include/$toggle_file.map
done

install -m644 %{SOURCE6} -D %{buildroot}%{_sysconfdir}/profile.d/40configure_keyboard.sh

mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/init.d

# some scripts expects setfont, unicode_{start,stop} and loadkeys inside /bin
mkdir -p %{buildroot}/bin
mv %{buildroot}/%{_bindir}/unicode_{start,stop} %{buildroot}/bin
ln -s ../../bin/unicode_start %{buildroot}/%{_bindir}/unicode_start
ln -s ../../bin/unicode_stop %{buildroot}/%{_bindir}/unicode_stop
mv %{buildroot}/%{_bindir}/{loadkeys,setfont,kbd_mode} %{buildroot}/bin
ln -s ../../bin/kbd_mode %{buildroot}/%{_bindir}/kbd_mode
ln -s ../../bin/loadkeys %{buildroot}/%{_bindir}/loadkeys
ln -s ../../bin/setfont %{buildroot}/%{_bindir}/setfont

install -m755 %{SOURCE7} -D %{buildroot}/sbin/setsysfont

%find_lang %{name}

%triggerun -- kbd < 1.15-5mdv
  /sbin/chkconfig --del keytable
exit 0


%files -f %{name}.lang
%{_bindir}/chvt
%{_bindir}/deallocvt
%{_bindir}/dumpkeys
%{_bindir}/fgconsole
%{_bindir}/getkeycodes
%{_bindir}/kbd_mode
%{_bindir}/kbdrate
%{_bindir}/loadkeys
%{_bindir}/loadunimap
%{_bindir}/mapscrn
%{_bindir}/openvt
%{_bindir}/psfaddtable
%{_bindir}/psfgettable
%{_bindir}/psfstriptable
%{_bindir}/psfxtable
%ifarch %{ix86} x86_64
%{_bindir}/resizecons
%endif
%{_bindir}/setfont
%{_bindir}/setkeycodes
%{_bindir}/setleds
%{_bindir}/setmetamode
%{_bindir}/showconsolefont
%{_bindir}/showkey
%{_bindir}/unicode_start
%{_bindir}/unicode_stop
%{_bindir}/clrunimap
%{_bindir}/getunimap
%{_bindir}/kbdinfo
%{_bindir}/outpsfheader
%{_bindir}/screendump
%{_bindir}/setlogcons
%{_bindir}/setpalette
%{_bindir}/setvesablank
%{_bindir}/setvtrgb
%{_bindir}/spawn_console
%{_bindir}/spawn_login
%{_bindir}/vlock
%config(noreplace) %{_sysconfdir}/profile.d/40configure_keyboard.sh
/bin/loadkeys
/bin/setfont
/bin/unicode_start
/bin/unicode_stop
/bin/kbd_mode
/sbin/setsysfont
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
%{_mandir}/man1/vlock.1*
%{_mandir}/man5/keymaps.5*
%{_mandir}/man8/getkeycodes.8*
%{_mandir}/man8/kbdrate.8*
%{_mandir}/man8/loadunimap.8*
%{_mandir}/man8/mapscrn.8*
%{_mandir}/man8/resizecons.8*
%{_mandir}/man8/setfont.8*
%{_mandir}/man8/setkeycodes.8*
%{_mandir}/man8/showconsolefont.8*
%{_mandir}/man1/codepage.1*
%{_mandir}/man1/screendump.1*
%{_mandir}/man1/splitfont.1*
%{_mandir}/man8/clrunimap.8*
%{_mandir}/man8/getunimap.8*
%{_mandir}/man8/mk_modmap.8*
%{_mandir}/man8/setlogcons.8*
%{_mandir}/man8/setvesablank.8*
%{_mandir}/man8/setvtrgb.8*
%{_mandir}/man8/vcstime.8*
%{kbddir}

%define kbddir /lib/kbd

Summary:	Keyboard and console utilities for Linux
Name:		kbd
Version:	2.0.2
Release:	1
License:	GPLv2+
Group:		Terminals
Url:		http://www.kbd-project.org/
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kbd/%{name}-%{version}.tar.xz
Source1:	vlock.pamd
Source2:	ucwfonts.tar.bz2
Source3:	ftp://ftp.linux-france.org/pub/macintosh/kbd-mac-fr-4.1.tar.gz
Source5:	kbd-distro-keymaps-20130823.tar.xz
Source6:	configure_keyboard.sh
# From Fedora
Source102:	kbd-latsun-fonts.tar.bz2
Source103:	kbd-latarcyrheb-16-fixed.tar.bz2
Source104:	fr-dvorak.tar.bz2
Source105:	kbd-latarcyrheb-32.tar.bz2
Source106:	xml2lst.pl
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
# (proyvind): systemd has become more restrictive about permissions for
#	      /dev/console, and since loadkeys are trying to grab it even when
#	      it's not even supposed to nor have any use of doing so, this
#	      causes problems for when we just wanna print out keymap to stdout
Patch8:		kbd-2.0.0-really-print-to-stdout-when-supposed-to.patch

# Fedora patches
# Patch0: puts additional information into man pages
Patch100:	kbd-1.15-keycodes-man.patch
# Patch1: sparc modifications
Patch101:	kbd-1.15-sparc.patch
# Patch2: adds default unicode font to unicode_start script
Patch102:	kbd-1.15-unicode_start.patch
# Patch3: add missing dumpkeys option to man page
Patch103:	kbd-1.15.3-dumpkeys-man.patch
# Patch4: fixes decimal separator in Swiss German keyboard layout, bz 882529
Patch104:	kbd-1.15.5-sg-decimal-separator.patch
# Patch5: implement PAM account and password management, backported from upstream
Patch105:	kbd-1.15.5-vlock-more-pam.patch
# Patch6: adds xkb and legacy keymaps subdirs to loadkyes search path, bz 1028207 
Patch106:	kbd-1.15.5-loadkeys-search-path.patch

# SuSE patches
Patch200:         kbd-1.15.2-prtscr_no_sigquit.patch
Patch201:         kbd-1.15.2-dumpkeys-ppc.patch
Patch202:         kbd-1.15.5-unicode_scripts.patch
Patch203:         kbd-1.15.2-docu-X11R6-xorg.patch
Patch204:         kbd-1.15.2-sv-latin1-keycode10.patch
Patch205:         kbd-1.15.2-setfont-no-cruft.patch
Patch206:         kbd-1.15.2-dumpkeys-C-opt.patch

BuildRequires:	bison
BuildRequires:	console-setup
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(xkeyboard-config)
BuildRequires:	pkgconfig(check)
Provides:	vlock = %{version}-%{release}
Obsoletes:	vlock <= 0:2.2.2-8

%description
This package contains utilities to load console fonts and keyboard maps.
It also includes a number of different fonts and keyboard maps.

%prep
%setup -q -a 2  -a 102 -a 103 -a 104 -a 105
cp -fp %{SOURCE106} .

%patch0 -p1
%patch1 -p1
%ifarch ppc ppc64
%patch2 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1 -b .stdout~

%patch100 -p1 -b .keycodes-man~
%patch101 -p1 -b .sparc~
%patch102 -p1 -b .unicode_start~
%patch103 -p1 -b .dumpkeys-man~
%patch104 -p1 -b .sg-decimal-separator~
%patch105 -p1 -b .vlock-more-pam~
%patch106 -p1 -b .loadkeys-search-path~


%patch200 -p1
#patch201 -p1
%patch202 -p1
#patch203 -p1
%patch204 -p1
%patch205 -p1
#patch206 -p0

mkdir mac_frnew; cd mac_frnew
tar -zxf %{SOURCE3}
gunzip mac-fr-ext_new.kmap.gz
mv mac-fr-ext_new.kmap ../data/keymaps/mac/all/mac-fr-ext_new.map
cd ..; rm -rf mac_frnew

pushd data
tar -jxf %{SOURCE5}
cp keymaps/i386/include/delete.inc keymaps/i386/include/delete.map
popd

# 7-bit maps are obsolete; so are non-euro maps
pushd data/keymaps/i386
mv qwerty/fi.map qwerty/fi-old.map
cp qwerty/fi-latin9.map qwerty/fi.map
cp qwerty/pt-latin9.map qwerty/pt.map
cp qwerty/sv-latin1.map qwerty/se-latin1.map

mv azerty/fr.map azerty/fr-old.map
cp azerty/fr-latin9.map azerty/fr.map

cp azerty/fr-latin9.map azerty/fr-latin0.map # legacy alias

# Rename conflicting keymaps
mv dvorak/no.map dvorak/no-dvorak.map
mv fgGIod/trf.map fgGIod/trf-fgGIod.map
mv olpc/es.map olpc/es-olpc.map
mv olpc/pt.map olpc/pt-olpc.map
mv qwerty/cz.map qwerty/cz-qwerty.map
popd

# remove obsolete "gr" translation
pushd po
rm -f gr.po gr.gmo
popd

# Convert to utf-8
iconv -f iso-8859-1 -t utf-8 < "ChangeLog" > "ChangeLog_"
mv "ChangeLog_" "ChangeLog"

%build
%configure \
	--datadir=%{kbddir} \
	--localedir=%{_localedir} \
	--enable-nls \
	--enable-optional-progs

%make

%install
%makeinstall_std localedir=%{_localedir}

# keep some keymap/consolefonts compatibility with console-tools
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
ln -s lat5-16.psfu.gz \
	%{buildroot}%{kbddir}/consolefonts/lat5u-16.psfu.gz

# ro_win.map.gz is useless
rm %{buildroot}%{kbddir}/keymaps/i386/qwerty/ro_win.map.gz

# Create additional name for Serbian latin keyboard
ln -s sr-cy.map.gz %{buildroot}%{kbddir}/keymaps/i386/qwerty/sr-latin.map.gz

# The rhpl keyboard layout table is indexed by kbd layout names, so we need a
# Korean keyboard
ln -s us.map.gz %{buildroot}%{kbddir}/keymaps/i386/qwerty/ko.map.gz

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

# Move binaries which we use before /usr is mounted from %{_bindir} to /bin.
mkdir -p %{buildroot}/bin
for binary in setfont dumpkeys kbd_mode unicode_start unicode_stop loadkeys ; do
  mv %{buildroot}%{_bindir}/$binary %{buildroot}/bin/
done

# Some microoptimization
sed -e 's,\<kbd_mode\>,/bin/kbd_mode,g;s,\<setfont\>,/bin/setfont,g' -i \
        %{buildroot}/bin/unicode_start

# Convert X keyboard layouts to console keymaps
mkdir -p %{buildroot}%{kbddir}/keymaps/xkb
perl xml2lst.pl < /usr/share/X11/xkb/rules/base.xml > layouts-variants.lst
while read line; do
  XKBLAYOUT=`echo "$line" | cut -d " " -f 1`
  XKBVARIANT=`echo "$line" | cut -d " " -f 2`
  ckbcomp "$XKBLAYOUT" "$XKBVARIANT" | gzip > %{buildroot}%{kbddir}/keymaps/xkb/"$XKBLAYOUT"-"$XKBVARIANT".map.gz
done < layouts-variants.lst

install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/vlock

%find_lang %{name}

%triggerun -- kbd < 1.15-5mdv
  /sbin/chkconfig --del keytable
exit 0

%files -f %{name}.lang
%{_bindir}/chvt
%{_bindir}/deallocvt
%{_bindir}/fgconsole
%{_bindir}/getkeycodes
%{_bindir}/kbdrate
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
%{_bindir}/setkeycodes
%{_bindir}/setleds
%{_bindir}/setmetamode
%{_bindir}/showconsolefont
%{_bindir}/showkey
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
%config(noreplace) %{_sysconfdir}/pam.d/vlock
%config(noreplace) %{_sysconfdir}/profile.d/40configure_keyboard.sh
/bin/dumpkeys
/bin/kbd_mode
/bin/loadkeys
/bin/setfont
/bin/unicode_start
/bin/unicode_stop
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

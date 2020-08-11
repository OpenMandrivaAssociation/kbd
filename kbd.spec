%define kbd_datadir %{_exec_prefix}/lib/kbd

Summary:	Keyboard and console utilities for Linux
Name:		kbd
Version:	2.3.0
Release:	1
License:	GPLv2+
Group:		Terminals
Url:		http://www.kbd-project.org/
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kbd/%{name}-%{version}.tar.xz
Source1:	kbd-latsun-fonts.tar.bz2
Source2:	kbd-latarcyrheb-32.tar.bz2
Source3:	xml2lst.pl
Source4:	vlock.pamd
Source5:	kbdinfo.1
Source6:	cz-map.patch
# From suse
Source10:	genmap4systemd.sh
# Patch0: puts additional information into man pages
Patch0:		kbd-1.15-keycodes-man.patch
# Patch1: sparc modifications
Patch1:		kbd-1.15-sparc.patch
# Patch2: adds default unicode font to unicode_start script
Patch2:		kbd-1.15-unicode_start.patch
# Patch3: add missing dumpkeys option to man page
Patch3:		kbd-1.15.3-dumpkeys-man.patch
# Patch4: fixes decimal separator in Swiss German keyboard layout, bz 882529
Patch4:		kbd-1.15.5-sg-decimal-separator.patch
# Patch5: adds xkb and legacy keymaps subdirs to loadkyes search path, bz 1028207 
Patch5:		kbd-1.15.5-loadkeys-search-path.patch
# Patch6: don't hardcode font used in unicode_start, take it from vconsole.conf,
#   bz 1101007
Patch6:		kbd-2.0.2-unicode-start-font.patch
# Patch7: fixes issues found by static analysis
Patch7:		kbd-2.0.4-covscan-fixes.patch
BuildRequires:	bison
BuildRequires:	console-setup
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(xkeyboard-config)
BuildRequires:	pkgconfig(check)
BuildRequires:	pigz
Requires(pre):	filesystem
Provides:	vlock = %{version}-%{release}
Obsoletes:	vlock <= 0:2.2.2-8
Provides:	open = 1.4-33
Obsoletes:	open < 1.4-33

%description
This package contains utilities to load console fonts and keyboard maps.
It also includes a number of different fonts and keyboard maps.

%prep
%setup -q -a 1 -a 2
cp -fp %{SOURCE3} .
cp -fp %{SOURCE6} .
cp -fp %{SOURCE10} .
%patch0 -p1 -b .keycodes-man
%patch1 -p1 -b .sparc
%patch2 -p1 -b .unicode_start
%patch3 -p1 -b .dumpkeys-man
%patch4 -p1 -b .sg-decimal-separator
%patch5 -p1 -b .loadkeys-search-path
%patch6 -p1 -b .unicode-start-font
%patch7 -p1 -b .covscan-fixes
autoreconf -f

# 7-bit maps are obsolete; so are non-euro maps
cd data/keymaps/i386
cp qwerty/pt-latin9.map qwerty/pt.map
cp qwerty/sv-latin1.map qwerty/se-latin1.map

mv azerty/fr.map azerty/fr-old.map
cp azerty/fr-latin9.map azerty/fr.map

cp azerty/fr-latin9.map azerty/fr-latin0.map # legacy alias

# Rename conflicting keymaps
mv fgGIod/trf.map fgGIod/trf-fgGIod.map
mv olpc/es.map olpc/es-olpc.map
mv olpc/pt.map olpc/pt-olpc.map
mv qwerty/cz.map qwerty/cz-qwerty.map
cd -

# remove obsolete "gr" translation
cd po
rm -f gr.po gr.gmo
cd -

# Convert to utf-8
iconv -f iso-8859-1 -t utf-8 < "ChangeLog" > "ChangeLog_"
mv "ChangeLog_" "ChangeLog"

%build
%configure \
	--datadir=%{kbd_datadir} \
	--localedir=%{_localedir} \
	--enable-nls \
	--enable-optional-progs

%make_build

%install
%make_install localedir=%{_localedir}

# Move binaries which we use before /usr is mounted from %{_bindir} to /bin.
mkdir -p %{buildroot}/bin
for binary in setfont dumpkeys kbd_mode unicode_start unicode_stop loadkeys ; do
  mv %{buildroot}%{_bindir}/$binary %{buildroot}/bin/
done

# ro_win.map.gz is useless
rm -f %{buildroot}%{kbd_datadir}/keymaps/i386/qwerty/ro_win.map.gz

# Create additional name for Serbian latin keyboard
ln -s sr-cy.map.gz %{buildroot}%{kbd_datadir}/keymaps/i386/qwerty/sr-latin.map.gz

# The rhpl keyboard layout table is indexed by kbd layout names, so we need a
# Korean keyboard
ln -s us.map.gz %{buildroot}%{kbd_datadir}/keymaps/i386/qwerty/ko.map.gz

# Define default console font
ln -s LatGrkCyr-8x16.psfu.gz \
	%{buildroot}%{kbd_datadir}/consolefonts/default.psfu.gz

# Some microoptimization
sed -i -e 's,\<kbd_mode\>,/bin/kbd_mode,g;s,\<setfont\>,/bin/setfont,g' \
        %{buildroot}/bin/unicode_start

# install kbdinfo manpage
install -m644 %{SOURCE5} %{buildroot}%{_mandir}/man1/kbdinfo.1

# Install PAM configuration for vlock
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/vlock

# Move original keymaps to legacy directory
mkdir -p %{buildroot}%{kbd_datadir}/keymaps/legacy
mv %{buildroot}%{kbd_datadir}/keymaps/{amiga,atari,i386,include,mac,ppc,sun} %{buildroot}%{kbd_datadir}/keymaps/legacy

# Convert X keyboard layouts to console keymaps
mkdir -p %{buildroot}%{kbd_datadir}/keymaps/xkb
perl xml2lst.pl < /usr/share/X11/xkb/rules/base.xml > layouts-variants.lst
while read line; do
  XKBLAYOUT="$(echo "$line" | cut -d " " -f 1)"
  echo "$XKBLAYOUT" >> layouts-list.lst
  XKBVARIANT="$(echo "$line" | cut -d " " -f 2)"
  ckbcomp "$XKBLAYOUT" "$XKBVARIANT" | gzip > %{buildroot}%{kbd_datadir}/keymaps/xkb/"$XKBLAYOUT"-"$XKBVARIANT".map.gz
done < layouts-variants.lst

# Convert X keyboard layouts (plain, no variant)
cat layouts-list.lst | sort -u >> layouts-list-uniq.lst
while read line; do
  ckbcomp "$line" | gzip > %{buildroot}%{kbd_datadir}/keymaps/xkb/"$line".map.gz
done < layouts-list-uniq.lst

# wipe converted layouts which cannot input ASCII (#1031848)
zgrep -L "U+0041" %{buildroot}%{kbd_datadir}/keymaps/xkb/* | xargs rm -f

# Rename the converted default fi (kotoistus) layout (#1117891)
gunzip %{buildroot}%{kbd_datadir}/keymaps/xkb/fi.map.gz
mv %{buildroot}%{kbd_datadir}/keymaps/xkb/fi.map %{buildroot}%{kbd_datadir}/keymaps/xkb/fi-kotoistus.map
gzip %{buildroot}%{kbd_datadir}/keymaps/xkb/fi-kotoistus.map

# Fix converted cz layout - add compose rules
gunzip %{buildroot}%{kbd_datadir}/keymaps/xkb/cz.map.gz
patch %{buildroot}%{kbd_datadir}/keymaps/xkb/cz.map < %{SOURCE6}
gzip %{buildroot}%{kbd_datadir}/keymaps/xkb/cz.map

# Rename the converted default fi (kotoistus) layout (#1117891), if exists
if [ -f "%{buildroot}%{kbd_datadir}/keymaps/xkb/fi.map.gz" ]; then
  gunzip %{buildroot}%{kbd_datadir}/keymaps/xkb/fi.map.gz
  mv %{buildroot}%{kbd_datadir}/keymaps/xkb/fi.map %{buildroot}%{kbd_datadir}/keymaps/xkb/fi-kotoistus.map
  gzip %{buildroot}%{kbd_datadir}/keymaps/xkb/fi-kotoistus.map
fi

# Fix converted cz layout - add compose rules, if exists
if [ -f "%{buildroot}%{kbd_datadir}/keymaps/xkb/cz.map.gz" ]; then
  gunzip %{buildroot}%{kbd_datadir}/keymaps/xkb/cz.map.gz
  patch %{buildroot}%{kbd_datadir}/keymaps/xkb/cz.map < %{SOURCE6}
  gzip %{buildroot}%{kbd_datadir}/keymaps/xkb/cz.map
f

# Link open to openvt
ln -s openvt %{buildroot}%{_bindir}/open

# Generate entries for systemd's /usr/share/systemd/kbd-model-map
mkdir -p  %{buildroot}%{_datadir}/systemd
sh ./genmap4systemd.sh %{buildroot}/%{kbd_datadir}/keymaps/xkb \
  > %{buildroot}%{_datadir}/systemd/kbd-model-map.xkb-generated

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/chvt
%{_bindir}/deallocvt
%{_bindir}/fgconsole
%{_bindir}/getkeycodes
%{_bindir}/kbdrate
%{_bindir}/loadunimap
%{_bindir}/mapscrn
%{_bindir}/openvt
%{_bindir}/open
%{_bindir}/psfaddtable
%{_bindir}/psfgettable
%{_bindir}/psfstriptable
%{_bindir}/psfxtable
%ifarch %{ix86} %{x86_64}
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
%{_mandir}/man1/kbdinfo.1*
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
%{kbd_datadir}
%{_datadir}/systemd/kbd-model-map.xkb-generated

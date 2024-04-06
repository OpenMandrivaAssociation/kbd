%ifnarch %{riscv}
# (tpg) optimize it a bit
%global optflags %{optflags} -Oz --rtlib=compiler-rt
%endif

#define beta rc1

Summary:	Keyboard and console utilities for Linux
Name:		kbd
Version:	2.6.4
Release:	%{?beta:0.%{beta}.}2
License:	GPLv2+
Group:		Terminals
Url:		http://www.kbd-project.org/
Source0:	https://kernel.org/pub/linux/utils/kbd/%{name}-%{version}%{?beta:-%{beta}}.tar.xz
Source1:	xml2lst.pl
Source2:	vlock.pamd
Source3:	kbdinfo.1

# From suse
Source10:	genmap4systemd.sh
# Patch0: puts additional information into man pages
Patch0:		kbd-1.15-keycodes-man.patch
# Patch1: sparc modifications
Patch1:		kbd-1.15-sparc.patch
# Patch2: adds default unicode font to unicode_start script
Patch2:		kbd-1.15-unicode_start.patch
# Patch3: fixes decimal separator in Swiss German keyboard layout, bz 882529
Patch3:		kbd-1.15.5-sg-decimal-separator.patch
# Patch4: adds xkb and legacy keymaps subdirs to loadkyes search path, bz 1028207 
Patch4:		kbd-1.15.5-loadkeys-search-path.patch
# Patch5: don't hardcode font used in unicode_start, take it from vconsole.conf,
#   bz 1101007
Patch5:		kbd-2.0.2-unicode-start-font.patch
# Patch6: fixes issues found by static analysis
Patch6:		https://src.fedoraproject.org/rpms/kbd/raw/rawhide/f/kbd-2.4.0-covscan-fixes.patch

BuildRequires:	bison
BuildRequires:	console-setup
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(xkeyboard-config)
BuildRequires:	pkgconfig(check)
BuildRequires:	pigz
Requires:	ncurses
Requires(pre):	filesystem
Provides:	vlock = %{version}-%{release}
Obsoletes:	vlock <= 0:2.2.2-8
Provides:	open = 1.4-33
Obsoletes:	open < 1.4-33

%description
This package contains utilities to load console fonts and keyboard maps.
It also includes a number of different fonts and keyboard maps.

%package legacy
Summary:	Legacy data for %{name} package
BuildArch:	noarch

%description legacy
The %{name}-legacy package contains original keymaps for kbd package.
Please note that %{name}-legacy is not helpful without kbd.

%prep
%setup -q -n %{name}-%{version}%{?beta:-%{beta}}
cp -fp %{S:1} .
cp -fp %{S:10} .
%patch0 -p1 -b .keycodes-man
%patch1 -p1 -b .sparc
%patch2 -p1 -b .unicode_start
%patch3 -p1 -b .sg-decimal-separator
%patch4 -p1 -b .loadkeys-search-path
%patch5 -p1 -b .unicode-start-font
%patch6 -p1 -b .covscan-fixes
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

%build
%configure \
	--datadir=%{_datadir} \
	--localedir=%{_localedir} \
	--enable-nls \
	--enable-optional-progs

%make_build

%install
%make_install localedir=%{_localedir}

# ro_win.map.gz is useless
rm -f %{buildroot}%{_datadir}/keymaps/i386/qwerty/ro_win.map.gz

# Create additional name for Serbian latin keyboard
ln -s sr-cy.map.gz %{buildroot}%{_datadir}/keymaps/i386/qwerty/sr-latin.map.gz

# The rhpl keyboard layout table is indexed by kbd layout names, so we need a
# Korean keyboard
ln -s us.map.gz %{buildroot}%{_datadir}/keymaps/i386/qwerty/ko.map.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=2015972
# xkb Arabic layout is 'ara', not 'fa', langtable tells us to use 'ara'
ln -s fa.map.gz %{buildroot}%{_datadir}/keymaps/i386/qwerty/ara.map.gz

# Some microoptimization
sed -i -e 's,\<kbd_mode\>,%{_bindir}/kbd_mode,g;s,\<setfont\>,%{_bindir}/setfont,g' \
        %{buildroot}%{_bindir}/unicode_start

# Install PAM configuration for vlock
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{S:2} %{buildroot}%{_sysconfdir}/pam.d/vlock

# install kbdinfo manpage
install -m644 %{S:3} %{buildroot}%{_mandir}/man1/kbdinfo.1

# Move original keymaps to legacy directory
mkdir -p %{buildroot}%{_datadir}/keymaps/legacy
mv %{buildroot}%{_datadir}/keymaps/{amiga,atari,i386,include,mac,ppc,sun} %{buildroot}%{_datadir}/keymaps/legacy

# Make sure Perl has a locale where uc/lc works for unicode codepoints
# see e.g. https://perldoc.perl.org/perldiag.html#Wide-character-(U%2b%25X)-in-%25s
export LC_ALL=C.utf-8
# Convert X keyboard layouts to console keymaps
mkdir -p %{buildroot}%{_datadir}/keymaps/xkb
perl xml2lst.pl < %{_datadir}/X11/xkb/rules/base.xml > layouts-variants.lst
while read line; do
    XKBLAYOUT=$(echo "$line" | cut -d " " -f 1)
    echo "$XKBLAYOUT" >> layouts-list.lst
    XKBVARIANT=$(echo "$line" | cut -d " " -f 2)
    ckbcomp "$XKBLAYOUT" "$XKBVARIANT" > /tmp/"$XKBLAYOUT"-"$XKBVARIANT".map
# skip converted layouts which cannot input ASCII (rh#1031848)
    grep -q "U+0041" /tmp/"$XKBLAYOUT"-"$XKBVARIANT".map && \
    gzip -cn9 /tmp/"$XKBLAYOUT"-"$XKBVARIANT".map > %{buildroot}%{_datadir}/keymaps/xkb/"$XKBLAYOUT"-"$XKBVARIANT".map.gz
    rm /tmp/"$XKBLAYOUT"-"$XKBVARIANT".map
done < layouts-variants.lst

# Convert X keyboard layouts (plain, no variant)
cat layouts-list.lst | sort -u >> layouts-list-uniq.lst
while read line; do
    ckbcomp "$line" > /tmp/"$line".map
    grep -q "U+0041" /tmp/"$line".map && \
    gzip -cn9 /tmp/"$line".map > %{buildroot}%{_datadir}/keymaps/xkb/"$line".map.gz
    rm /tmp/"$line".map
done < layouts-list-uniq.lst

[ ! "$(ls -A %{buildroot}%{_datadir}/keymaps/xkb)" ] && "Xkb keymaps are missing!" && exit 1

# Link open to openvt
ln -s openvt %{buildroot}%{_bindir}/open

# Generate entries for systemd's /usr/share/systemd/kbd-model-map
mkdir -p  %{buildroot}%{_datadir}/systemd
sh ./genmap4systemd.sh %{buildroot}/%{_datadir}/keymaps/xkb \
  > %{buildroot}%{_datadir}/systemd/kbd-model-map.xkb-generated

# remove library used only for tests
rm -f %{buildroot}%{_libdir}/libtswrap*
rm -f %{buildroot}%{_prefix}/lib/debug/%{_libdir}/libtswrap*

%find_lang %{name}

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/pam.d/vlock
%{_bindir}/*
%{_datadir}/consolefonts
%{_datadir}/consoletrans
%{_datadir}/keymaps
%{_datadir}/unimaps
%exclude %{_datadir}/keymaps/legacy
%{_datadir}/systemd/kbd-model-map.xkb-generated
%doc %{_mandir}/*/*
%ghost /usr/lib/kbd.rpmmoved

%files legacy
%{_datadir}/keymaps/legacy

# Get rid of the traditional /usr/lib/kbd directory structure.
# It makes much more sense to keep all consolefonts (kbd + console-setup + ...)
# in one place
# Unfortunately this is even more tricky than usual because the right place
# (/usr/share/consolefonts etc.) already exists from console-setup, so a simple
# os.rename("/usr/lib/kbd", ...) won't do the trick.
# Then again, since nothing outside of kbd is supposed to put stuff there, we can
# take a nasty shortcut...
%pretrans -p <lua>
st = posix.stat("/usr/lib/kbd")
if st and st.type == "directory" then
  status = os.rename("/usr/lib/kbd", "/usr/lib/kbd.rpmmoved")
end

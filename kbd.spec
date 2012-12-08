%define kbddir /usr/lib/kbd
%define mdv_keymaps_ver 20081113

Name:   	kbd
Version:	1.15.3
Release:	6
Summary:	Keyboard and console utilities for Linux
License:	GPL
Group:  	Terminals
URL:    	ftp://ftp.kernel.org/pub/linux/utils/kbd/
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kbd/kbd-%{version}.tar.bz2
Source2:	ucwfonts.tar.bz2
Source3:	ftp://ftp.linux-france.org/pub/macintosh/kbd-mac-fr-4.1.tar.gz
Source5:	kbd-mdv-keymaps-%{mdv_keymaps_ver}.tar.bz2
Source6:	configure_keyboard.sh
Source7:	setsysfont
# mandriva keyboard updates
Patch0: 	kbd-1.15-mandriva.patch
# tilde with twosuperior in french keyboard
Patch1: 	kbd-1.15-tilde_twosuperior_french_kbd.patch
# some modifications to cover PPC using Linux keycodes
Patch2: 	kbd-1.12-ppc_using_linux_keycodes.patch
# thai support, I tried to convert it from console-tools package
# (support added by Pablo), see these patches as reference:
# http://linux.thai.net/~thep/th-console/console-tools/console-tools-thai_ksym.patch
# http://linux.thai.net/~thep/th-console/console-data/console-data-thai_orig-1999.08.29.patch
# (note: thai_ksym patch not needed anymore, it's merged in kbd)
Patch4: 	kbd-1.12-data_thai.patch
# avoid kbd scheme for loadkeys, we use unicode_start in configure_keyboard.sh
Patch5: 	kbd-1.14.1-unicode_start_no_loadkeys.patch
# (fc) remove unneeded calls in unicode_stop
Patch6:		kbd-1.15-remove-unneeded-calls.patch
# (fc) allow to wait for VT switch in userland (Novell bug #540482) (Gentoo)
Patch7:		kbd-1.12-chvt-userwait.patch
# (tpg) fix es translation, probably will be dropped on next release
Patch8:		kbd-1.15.3-fix-es-translation.patch
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
%patch8 -p1

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
%configure2_5x	\
	--datadir=%{kbddir} \
	--mandir=%{_mandir} \
	--enable-nls \
	--localedir=%{_datadir}/locale \
	--enable-optional-progs \
	--disable-rpath

%make

%install
%makeinstall_std \
	localedir=%{_datadir}/locale

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

mkdir -p %{buildroot}/%{_sysconfdir}/profile.d
install -m 644 %{SOURCE6} \
	%{buildroot}/%{_sysconfdir}/profile.d/40configure_keyboard.sh

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

mkdir %{buildroot}/sbin
install -m 0755 %{SOURCE7} %{buildroot}/sbin

%find_lang %{name}

%triggerun -- kbd < 1.15-5mdv
  /sbin/chkconfig --del keytable
exit 0


%files -f %{name}.lang
%defattr(0755,root,root,0755)
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
%ifarch %{ix86}
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
#config(noreplace) %{_sysconfdir}/profile.d/40configure_keyboard.sh
#we need replace it
%config %{_sysconfdir}/profile.d/40configure_keyboard.sh
/bin/loadkeys
/bin/setfont
/bin/unicode_start
/bin/unicode_stop
/bin/kbd_mode
/sbin/setsysfont
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


%changelog
* Sun Jun 19 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.15.3-1mdv2011.0
+ Revision: 686039
- update to new version 1.15.3
- Patch8: fix es translations
- nuke rpath
- enable building od optional programs
- update file list

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.15.2-4
+ Revision: 666005
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.15.2-3mdv2011.0
+ Revision: 606249
- rebuild

  + Frederic Crozat <fcrozat@mandriva.com>
    - Patch7 (Gentoo): allow to wait for VT switch in userland (Novell bug #540482)

* Thu Apr 15 2010 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.15.2-1mdv2010.1
+ Revision: 535180
- Updated to version 1.15.2

* Sun Jan 24 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.15.1-1mdv2010.1
+ Revision: 495591
- update to new version 1.15.1
- drop patch 3, fixed by upstream

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - files in /etc/profile.d should not be executable, but should have an order prefix

* Fri Oct 16 2009 Frederic Crozat <fcrozat@mandriva.com> 1.15-5mdv2010.0
+ Revision: 457933
- Remove keytable initscripts, handled by udev now
- Patch6: remove unneeded calls in unicode_stop

* Fri Oct 09 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.15-4mdv2010.0
+ Revision: 456447
- kbd-1.15-mandriva.patch: patching qwerty-layout to include euro breaks
  jp106 keymap as it doesn't include AltGr table, use an alternative
  qwerty-layout without euro/currency sign only for it (#34213).

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.15-3mdv2010.0
+ Revision: 425481
- rebuild

* Tue Feb 10 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.15-2mdv2009.1
+ Revision: 339179
- Rediff and rename some patches (update version in patch names, use
  same extension, smaller name description).
- Revert BuildRoot tag change to default value as proposed in
  http://wiki.mandriva.com/en/Policies/RpmSpecProposal
- Removed autoreconf call, not needed.
- Cosmetics.

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.15-1mdv2009.1
+ Revision: 325688
- 1.15
- nuke upstream implemented/redundant patches
- rediff some patches
- fix build with -Werror=format-security (P6)
- fix locales (how long has this been broken?)

* Thu Dec 11 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.14.1-5mdv2009.1
+ Revision: 312634
- Obsolete libconsole0* packages derived from console-tools, like main
  console-tools package already obsoleted.

* Thu Nov 13 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.14.1-4mdv2009.1
+ Revision: 302770
- kbd-mdv-keymaps 20081113
  * remove following keymaps previously added from debian
    console-data-1.03 that don't work with kbd: gr-utf8.map,
    ro-academic.map, ro-comma.map

* Wed Nov 12 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.14.1-3mdv2009.1
+ Revision: 302386
- Change "main" keysym for keycode 7 bind on be-latin1 keymap (#43175).

* Tue Nov 11 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.14.1-2mdv2009.1
+ Revision: 302360
- Add upstream kbd fixes:
  * fix loadunimap ("loadunimap should use UNIMAPDIR")
  * re-add qwerty version of cz.map

* Tue Nov 11 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.14.1-1mdv2009.1
+ Revision: 302348
- Cosmetics.
- Updated to version 1.14.1
- kbd-mdv-keymaps 20081111:
  * removed UniCyr_8x14.psf, UniCyr_8x16.psf, UniCyr_8x8.psf,
    UniCyrExt_8x16.psf, by-cp1251.map, bywin-cp1251.map:
    same version included in kbd 1.14.1
  * removed pl1.map, ro.map, ro.uni.map, cz.map: updated version
    included in kbd 1.14.1
- Rediffed mandriva, unicode_start_no_loadkeys patches.
- Removed kbd-1.12-thai_ksym_deb.patch (merged).
- Removed kbd-1.12-unicode_only_in_linux_vt.patch (not needed anymore).
- Fixed bug of man pages always being installed despite optional
  programs being disabled.
- Fix build of getkeycodes, resizecons, setkeycodes (build always
  disabled).

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.12-15mdv2009.0
+ Revision: 221765
- rebuild

* Tue Feb 05 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.12-14mdv2008.1
+ Revision: 162526
- keytable.init: revert back to using .uni files. I thought that they
  could be removed and we should just start using "loadkeys -u", but
  some uni files have extra customizations that would be lost by
  removing them.
- Accordingly to Belgian keyboard layout, keycode 7 should be
  paragraph_sign, so fix be-latin1 with
  kbd-1.12-be-latin1-paragraph_sign-fix.patch

* Sun Jan 13 2008 Anssi Hannula <anssi@mandriva.org> 1.12-13mdv2008.1
+ Revision: 150908
- adapt obsoletes versioning on console-tools for the new release

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Nov 29 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.12-12mdv2008.1
+ Revision: 113910
- keytable initscript: avoid verbose loadkeys, and miscellaneous
  styling/indentation enhancements and fixes.
- unicode_{start,stop}: don't allow them to run if we're not in a linux
  vt, otherwise bugs can happen, like when you try to run kbd_mode
  inside X.
- Removed unused patch: keytable.init.ppc.patch

* Fri Nov 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1.12-11mdv2008.1
+ Revision: 109171
- fix missing ";" in the initscript

* Tue Nov 13 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.12-10mdv2008.1
+ Revision: 108539
- keytable.init:
  * test if /bin/loadkeys is executable, not only if it exists;
  * use loadkeys with "-u" option for cases when the keytable isn't
    unicode ready (#35028).

* Tue Nov 13 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.12-9mdv2008.1
+ Revision: 108467
- Added extra keymaps to kbd-mdv-keymaps from debian console-data-1.03:
  * i386/azerty: fr-x11, wo
  * i386/dvorak: dvorak-classic, dvorak-de, dvorak-lisp, dvorak-ru
  * i386/fgGIod: trfu
  * i386/qwerty: cz-us-qwerty, gr-utf8, lisp-us, lk201-us, no-standard,
                 ro-academic, ro-comma, trqu, us-intl.iso15
  * mac/all: ibook2-uk, ibook-it, mac-de2-ext, mac-fr2-ext,
             mac-ibook-de-deadkeys, mac-ibook-de, mac-macbook-de,
             mac-macbook-fr, mac-pl_m-ext1, mac-pl_m-ext,
             mac-us-dvorak, mac-us-ext, mac-us-std
  The addition of mac keymap files was suggested by Jerome Soyer
  (saispo).
- Fixed location of mac include files in kbd-mdv-keymaps.

* Thu Sep 27 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.12-8mdv2008.0
+ Revision: 93422
- setsysfont: send error output to stderr and trailing spaces cleanups,
  contributed by Jose Da Silva (#33845). Also while at it I discovered
  one small bug: to show the error message to tell the location of
  sysconfig.txt, setsysfont was looking for /usr/share/doc/initscripts-*
  as previously the directory had version in its name, it's no more this
  way since some changes happened in mandriva packaging stuff, so now
  hopefully use a more reliable check.

* Tue Sep 25 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.12-7mdv2008.0
+ Revision: 92713
- Consider all toggle definitions that could be loaded before with
  console-toools. There are additional toggle definitions that were not
  covered when keeping compatibility with previous console-tools package
  and current keytable initscript. Only shift_toggle.inc wasn't
  considered now because it doesn't have any definition. Reported in
  part by dok_cooker (in #mandriva-cooker irc channel on freenode).

* Tue Aug 14 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.12-6mdv2008.0
+ Revision: 63150
- Removed vt-is-UTF8, not needed anymore by our initscripts.

* Mon Aug 06 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.12-5mdv2008.0
+ Revision: 59383
- Copy some *.inc files to *.map to keep compatibility with
  initscripts/drakx-kbd-mouse-x11 (#32284).

* Fri Aug 03 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.12-4mdv2008.0
+ Revision: 58570
- Added compatibility symlinks for some console-tools fonts, to avoid
  problems on upgrades from console-tools:
  iso07.f16 -> iso07u-16
  lat2-sun16 -> lat2-16
  lat5u-16 -> lat5-16
  Reported by Rafal Prasal and Pascal Rigaux.

* Wed Aug 01 2007 Olivier Blin <oblin@mandriva.com> 1.12-3mdv2008.0
+ Revision: 57804
- package resizecons on ix86 only
- buildrequire flex
- update conflicting initscripts version
- remove console-tools provides
- buildrequire bison

  + Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Added missing conflicts to util-linux < 2.13 as seem by blino, now
      that we provide kbdrate with kbd.
    - Provide again kbdrate, as this will be removed from util-linux
      package.
    - Install back at /usr/lib/kbd, we depend on /usr/bin/locale on
      initialization inside initscripts so it doesn't matter, as we
      depend anyway on /usr to be mounted.
    - Added transitional provides for console-tools.
    - Cleanups.
    - Install kbd data files in /lib/kbd and with this remove the need to do
      workarounds in post or initscripts to load files before /usr is
      mounted.
    - Obsolete console-tools.
    - Made the same fixes to vt-is-UTF8.c as on console-tools package
      (bug #27948):
      * applied patch vt-is-UTF8_only_linux_vt based on an almost equal
        debian patch: don't allow vt-is-UTF8 run in a terminal different
        from linux vt.
      * applied patch fscanf_nonblock: vt-is-UTF8 detection of console mode
        is unreliable because it uses terminal input/output + escape codes.
        Other processes can be writing/reading from the same vt and messing
        with results expected by fscanf function inside is_in_UTF8_mode,
        making it possibly block waiting for data. I implemented a
        workaround by using fcntl to make it nonblock, I tried a cleaner
        solution but didn't found another way. (and linux could offer an
        ioctl to check its vc->vc_utf variable, see linux/drivers/char/vt.c,
        to avoid to using the current vt-is-UTF8 messy detection).
    - Added appropriate setsysfont script.
    - Removed uneeded stty_iutf8 patch.
    - Fixed keytable initscript for kbd.
    - We don't always use unicode_start as root (like in
      configure_keyboard.sh), so we can't use loadkeys
      (unicode_start_no_loadkeys patch).
    - Enable proper conflicts for initscripts, console-tools packages. Added
      a new meta provides, vt-tools.
    - Don't ship kbdrate, already in util-linux.
    - Copy font files to /etc/sysconfig/console in post scriptlet as made on
      console-tools (related to initscripts).
    - Adapted vt-is-UTF8 from console-tools.
    - Move some binaries into /bin as initscripts requires them.
    - Fixed macintosh keymap symlinks.
    - Added initscript, configure_keyboard.sh script and init.ppc patch from
      console-tools package.
    - Migrated keymaps from kbd-mdk-keymaps-20050108.tar.bz2 and
      ctools-cyr.tar.bz2 to kbd-mdv-keymaps-20070521.tar.bz2 (tried to adapt
      to kbd).
    - Added more symlinks to keymaps to map them to the ones present in
      console-tools (us-intl -> us-acentos, some for mac).
    - Added updated mac-fr keymap definition, it's also in a previous
      version on console-tools package:
      * french mac keymap v3 - console-data-1999.08.29-mac.patch.
    - Converted tilde-with-twosuperior-in-french-keyboard patch from console
      tools into tilde_twosuperior_french_kbd patch.
    - ppc-using-linux-keycodes console-tools patch ->
      ppc_using_linux_keycodes patch.
    - Migrated mandrake patch from console-tools (kbd-1.12-mandriva.patch).
    - Migrated thai support from console-tools (I hope it's right).
    - Added ucwfonts as it's also on console-tools.
    - Added stty_iutf8 patch, set console input mode when in utf8 (needs
      testing).
    - Import kbd


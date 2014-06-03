%define nsusr nagios
%define nsgrp nagios
%define cmdusr apache
%define cmdgrp apache
%define _disable_ld_no_undefined 1

Summary:    Host/service/network monitoring program
Name:       nagios
Version:    3.5.1
Release:    1
License:    GPLv2
Group:      Networking/Other
URL:        http://www.nagios.org/
Source0:    http://prdownloads.sourceforge.net/nagios/%{name}-%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}.tmpfiles
Source5:    favicon.ico
Patch1:     nagios-3.5.0-mdv-config.patch
Patch6:     nagios-DESTDIR.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:   apache
Requires:   nagios-plugins
BuildRequires:  gd-devel
BuildRequires:  imagemagick
BuildRequires:  jpeg-devel
BuildRequires:  libtool-devel
BuildRequires:  multiarch-utils >= 1.0.3
BuildRequires:  perl-devel
Epoch:      1

%description
Nagios is a program that will monitor hosts and services on your
network. It has the ability to email or page you when a problem
arises and when a problem is resolved. Nagios is written in C and
is designed to run under Linux (and some other *NIX variants) as a
background process, intermittently running checks on various
services that you specify.

The actual service checks are performed by separate "plugin"
programs which return the status of the checks to Nagios.

This package provide core programs for nagios. The web interface,
documentation, and development files are built as separate
packages

%package    www
Summary:    Provides the HTML and CGI files for the Nagios web interface
Group:      Networking/WWW
Requires:   %{name} = %{epoch}:%{version}-%{release}
Requires:   webserver
Requires:   freetype
Requires:   freetype2
Requires:   nail
Requires:   traceroute
Requires:   apache-mod_php
Requires:   %{name}-imagepaks
Obsoletes:  nagios-theme-nuvola
Obsoletes:  nagios-theme
Epoch:      %{epoch}

%description    www
Nagios is a program that will monitor hosts and services on your network. It
has the ability to email or page you when a problem arises and when a problem
is resolved. Nagios is written in C and is designed to run under Linux (and
some other *NIX variants) as a background process, intermittently running
checks on various services that you specify.

Several CGI programs are included with Nagios in order to allow you to view the
current service status, problem history, notification history, and log file via
the web. This package provides the HTML and CGI files for the Nagios web
interface. In addition, HTML documentation is included in this package

%package    devel
Group:      Development/C
Summary:    Provides include files that Nagios-related applications may compile against
Epoch:      %{epoch}

%description    devel
Nagios is a program that will monitor hosts and services on your network. It
has the ability to email or page you when a problem arises and when a problem
is resolved. Nagios is written in C and is designed to run under Linux (and
some other *NIX variants) as a background process, intermittently running
checks on various services that you specify.

This package provides include files that Nagios-related applications may
compile against.

%prep
%setup -q -n nagios
%patch1 -p1
%patch6 -p0

%build
%serverbuild

export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export FFLAGS="$FFLAGS -fPIC"
%configure2_5x \
    --with-httpd-conf=%{_webappconfdir} \
    --with-checkresult-dir=/var/spool/nagios/checkresults \
    --with-temp-dir=/tmp \
    --exec-prefix=%{_sbindir} \
    --bindir=%{_sbindir} \
    --sbindir=%{_libdir}/nagios/cgi \
    --libexecdir=%{_libdir}/nagios/plugins \
    --datadir=%{_datadir}/nagios \
    --sysconfdir=%{_sysconfdir}/nagios \
    --localstatedir=/var/log/nagios \
    --with-lockfile=/var/run/nagios/nagios.pid \
    --with-mail=/bin/mail \
    --with-nagios-user=%{nsusr} \
    --with-nagios-group=%{nsgrp} \
    --with-command-user=%{cmdusr} \
    --with-command-grp=%{cmdgrp} \
    --with-cgiurl=/nagios/cgi-bin \
    --with-htmurl=/nagios \
    --with-default-comments \
    --with-default-downtime \
    --with-default-extinfo \
    --with-default-retention \
    --with-default-status \
    --with-default-objects \
    --with-default-perfdata \
    --with-file-perfdata \
    --with-template-extinfo \
    --with-template-objects \
    --with-gd-lib=%{_libdir} \
    --with-gd-inc=%{_includedir} \
    --enable-embedded-perl \
    --with-perlcache

# bug
perl -pi -e "s|/var/log/nagios/spool/checkresults|/var/spool/nagios/checkresults|g" include/locations.h

# the helloworld one doesn't like -fPIE
perl -pi -e "s|-fPIE||g" module/Makefile

%make all

pushd contrib
    make daemonchk.cgi
    make traceroute.cgi
    make mini_epn
    make convertcfg
popd

%install
rm -rf %{buildroot}

install -d -m0755 %{buildroot}%{_webappconfdir}
install -d -m0755 %{buildroot}/var/spool/nagios/checkresults
install -d -m0755 %{buildroot}/var/run/nagios
install -d -m0755 %{buildroot}%{_includedir}/nagios

install -d -m0755 %{buildroot}%{_sysconfdir}/nagios/{servers,printers,switches,routers,conf.d,plugins.d}
install -d -m0755 %{buildroot}%{_libdir}/nagios/plugins/eventhandlers

make \
    DESTDIR=%{buildroot} \
    BINDIR=%{_sbindir} \
    CFGDIR=%{_sysconfdir}/nagios \
    CGIDIR=%{_libdir}/nagios/cgi \
    COMMAND_OPTS="" \
    HTMLDIR=%{_datadir}/nagios/www \
    INIT_OPTS="" \
    INSTALL=install \
    INSTALL_OPTS="" \
    LOGDIR=/var/log/nagios \
    STRIP=/bin/true \
    install-config \
    fullinstall

# fix docs
cp sample-config/README README.sample-config
cp sample-config/template-object/README README.template-object

# install headers
install -m0644 include/locations.h %{buildroot}%{_includedir}/nagios/

pushd contrib
    make \
    DESTDIR=%{buildroot} \
    BINDIR=%{_sbindir} \
    CFGDIR=%{_sysconfdir}/nagios \
    CGIDIR=%{_libdir}/nagios/cgi \
    COMMAND_OPTS="" \
    HTMLDIR=%{_datadir}/nagios/www \
    INIT_OPTS="" \
    INSTALL=install \
    INSTALL_OPTS="" \
    LOGDIR=/var/log/nagios \
    install
popd

# fix strange perms
find %{buildroot}%{_datadir}/nagios -type d | xargs chmod 755
find %{buildroot}%{_datadir}/nagios/www -type f | xargs chmod 644
chmod 755 \
    %{buildroot}%{_libdir}/nagios/cgi/* \
    %{buildroot}%{_sbindir}/*

# fix default config
perl -pi \
    -e "s|=/var/log/nagios/rw/|=/var/spool/nagios/|g" \
    %{buildroot}%{_sysconfdir}/nagios/*.cfg
perl -pi \
    -e "s|^physical_html_path=.*|physical_html_path=%{_datadir}/nagios/www|g" \
    %{buildroot}%{_sysconfdir}/nagios/cgi.cfg


# systemd
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/nagios.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_prefix}/lib/tmpfiles.d/nagios.conf
rm -f %{buildroot}%{_initrddir}/nagios

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# Nagios Apache configuration

ScriptAlias /%{name}/cgi-bin %{_libdir}/%{name}/cgi

<Directory %{_libdir}/%{name}/cgi>
    Require all granted
    Options ExecCGI
</Directory>

Alias /%{name} %{_datadir}/%{name}/www

<Directory %{_datadir}/%{name}/www>
    Require all granted
</Directory>
EOF

# install and fix event handlers
install -m0755 contrib/eventhandlers/disable_active_service_checks %{buildroot}%{_libdir}/nagios/plugins/eventhandlers/
install -m0755 contrib/eventhandlers/disable_notifications %{buildroot}%{_libdir}/nagios/plugins/eventhandlers/
install -m0755 contrib/eventhandlers/enable_active_service_checks %{buildroot}%{_libdir}/nagios/plugins/eventhandlers/
install -m0755 contrib/eventhandlers/enable_notifications %{buildroot}%{_libdir}/nagios/plugins/eventhandlers/
install -m0755 contrib/eventhandlers/submit_check_result %{buildroot}%{_libdir}/nagios/plugins/eventhandlers/
install -m0755 contrib/eventhandlers/distributed-monitoring/obsessive_svc_handler %{buildroot}%{_libdir}/nagios/plugins/eventhandlers/
install -m0755 contrib/eventhandlers/distributed-monitoring/submit_check_result_via_nsca %{buildroot}%{_libdir}/nagios/plugins/eventhandlers/
install -m0755 contrib/eventhandlers/redundancy-scenario1/handle-master-host-event %{buildroot}%{_libdir}/nagios/plugins/eventhandlers/
install -m0755 contrib/eventhandlers/redundancy-scenario1/handle-master-proc-event %{buildroot}%{_libdir}/nagios/plugins/eventhandlers/

find %{buildroot}%{_libdir}/nagios/plugins/eventhandlers -type f | \
    xargs perl -pi \
    -e 's|/usr/local/nagios/var/rw/|/var/spool/nagios/|;' \
    -e 's|/usr/local/nagios/libexec/eventhandlers|%{_libdir}/nagios/plugins/eventhandlers|g;' \
    -e 's|/usr/local/nagios/libexec/send_nsca|%{_libdir}/nagios/plugins/send_nsca|g;' \
    -e 's|/usr/local/nagios/test/var|/var/log/nagios|g;' \
    -e 's|/usr/local/nagios/etc/send_nsca.cfg|%{_sysconfdir}/nagios/send_nsca.cfg|g;' \
    -e 's|printfcmd="/bin/printf"|printfcmd="/usr/bin/printf"|;'

%multiarch_includes %{buildroot}%{_includedir}/nagios/locations.h

# install the favicon.ico
install -m 644 %{SOURCE5} %{buildroot}%{_datadir}/nagios/www

# automatic reloading for new plugins
install -d %buildroot%{_var}/lib/rpm/filetriggers
cat > %buildroot%{_var}/lib/rpm/filetriggers/nagios.filter << EOF
^.%{_sysconfdir}/nagios/plugins.d/.*\.cfg$
EOF
cat > %buildroot%{_var}/lib/rpm/filetriggers/nagios.script << EOF
#!/bin/sh
systemctl try-restart nagios.service
EOF
chmod 755 %buildroot%{_var}/lib/rpm/filetriggers/nagios.script

%pre
%_pre_useradd %{nsusr} /var/log/nagios /bin/sh
%{_bindir}/gpasswd -a %{cmdusr} %{nsgrp} >/dev/null 2>&1 || :

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{nsusr}

%files
%doc Changelog INSTALLING LEGAL README UPGRADING
%doc sample-config/mrtg.cfg
%{_unitdir}/nagios.service
%{_prefix}/lib/tmpfiles.d/nagios.conf
%{_sbindir}/*
%dir %{_sysconfdir}/nagios
%dir %{_sysconfdir}/nagios/conf.d
%dir %{_sysconfdir}/nagios/plugins.d
%dir %{_sysconfdir}/nagios/objects
%config(noreplace) %{_sysconfdir}/nagios/*.cfg
%config(noreplace) %{_sysconfdir}/nagios/objects/*.cfg
%attr(-,%{nsusr},%{nsgrp}) %dir /var/log/nagios
%attr(-,%{nsusr},%{nsgrp}) %dir /var/log/nagios/archives
%attr(2775,%{nsusr},%{cmdgrp}) %dir /var/spool/nagios
%attr(-,%{nsusr},%{nsgrp}) %dir /var/spool/nagios/checkresults
%attr(-,%{nsusr},%{nsgrp}) %dir /var/run/nagios
%dir %{_libdir}/nagios/plugins/eventhandlers
%{_libdir}/nagios/plugins/eventhandlers/*
%{_var}/lib/rpm/filetriggers/nagios.*

%files www
%config(noreplace) %{_webappconfdir}/nagios.conf
%{_libdir}/nagios/cgi
%{_datadir}/nagios/www

%files devel
%{multiarch_includedir}/nagios/locations.h
%{_includedir}/nagios


%changelog
* Thu Jul 12 2012 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.1-1mdv2012.0
+ Revision: 809010
- fix build
- sync with nagios-3.4.1-5.mga3.src.rpm

* Sun Jan 01 2012 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:3.3.1-1
+ Revision: 748649
- 3.3.1
  from mageia, thanks

* Sat Feb 05 2011 Funda Wang <fwang@mandriva.org> 1:3.2.3-2
+ Revision: 636326
- tighten BR

* Wed Oct 06 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.2.3-1mdv2011.0
+ Revision: 583635
- new version
- drop format error patch, merged upstream

* Sun Sep 05 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.2.2-1mdv2011.0
+ Revision: 576159
- new version

* Wed Aug 11 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.2.1-2mdv2011.0
+ Revision: 569136
- rebuild for new perl
- fix binaries perms

* Sat Mar 27 2010 Thierry Vignaud <tv@mandriva.org> 1:3.2.1-1mdv2010.1
+ Revision: 528045
- new release

* Wed Feb 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.2.0-7mdv2010.1
+ Revision: 507286
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- switch to "open to all" default access policy

* Sat Jan 16 2010 Funda Wang <fwang@mandriva.org> 1:3.2.0-6mdv2010.1
+ Revision: 492259
- rebuild for new libjpeg v8

* Fri Dec 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.2.0-5mdv2010.1
+ Revision: 473483
- better apache configuration

* Mon Nov 30 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.2.0-4mdv2010.1
+ Revision: 472077
- restrict default access permissions to localhost only, as per new policy

* Wed Sep 09 2009 Frederik Himpe <fhimpe@mandriva.org> 1:3.2.0-3mdv2010.0
+ Revision: 435783
- Rebuild for new perl

* Mon Aug 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.2.0-2mdv2010.0
+ Revision: 417293
- rebuilt against libjpeg v7

* Thu Aug 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.2.0-1mdv2010.0
+ Revision: 416025
- 3.2.0

* Sun Jul 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.1.2-2mdv2010.0
+ Revision: 397904
- merge README.mandriva and README.urpmi in a single README.mdv file, and use an herein document for it
- drop old 2006.0 menu entr
- cleanup %%files section
- drop overcomplex password generation at install-time, and ship a minimal apache configuration file, admins are supposed smart enough to configure suited protection themselves
- drop useless explicit dependencies
- spec cleanup
- build mini_epn
- allow translations in initscript
- drop useless optflag patch
- use make argument instead of a patch to avoid stripping
- no need to regenerate autotools suite

* Wed Jul 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.1.2-1mdv2010.0
+ Revision: 391239
- bump release
- 3.1.2

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - fix default physical_html_path in cgi.cfg

* Sun Jan 25 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.1.0-1mdv2009.1
+ Revision: 333546
- 3.1.0
- fix build with -Werror=format-security (P7)
- don't activate the check_for_updates feature per default (P8)

* Tue Dec 30 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.0.6-3mdv2009.1
+ Revision: 321471
- enable embedded perl
- substitute files only, not directories
- fix more file perms
- move web pages under %%{_datadir}/nagios/www, to avoid having plugins under web root

* Mon Dec 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.0.6-2mdv2009.1
+ Revision: 314622
- add file triggers to reload nagios when adding plugins
- rename apache configuration file according to webapps policy, while
  moving old one to avoid #45963
- rediff patch 0 for no fuzz
- fix init script logic: cmd and pid files should be deleted if present, not if missing

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Dec 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.6-1mdv2009.1
+ Revision: 309178
- 3.0.6 (Minor security fixes)

* Mon Nov 24 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.5-2mdv2009.1
+ Revision: 306324
- fix #45963 (Move of configuration file breaks custom configurations)

* Wed Nov 05 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.0.5-1mdv2009.1
+ Revision: 300019
- new version
- don't version apache configuration file

* Thu Oct 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.4-1mdv2009.1
+ Revision: 294138
- 3.0.4

* Fri Jul 04 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.0.3-2mdv2009.0
+ Revision: 231681
- yet another event handlers fix

* Thu Jun 26 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.3-1mdv2009.0
+ Revision: 229226
- 3.0.3

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed May 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.0.2-0.1mdv2009.0
+ Revision: 209800
- 3.0.2

* Thu May 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.0.1-2mdv2009.0
+ Revision: 207546
- change the dependency in initscript from mysql to ndo2db

* Wed Apr 02 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.0.1-1mdv2008.1
+ Revision: 191564
- new version (bugfix release)

* Fri Mar 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.0-1mdv2008.1
+ Revision: 187806
- final version

* Wed Feb 27 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:3.0-0.0.rc3.1mdv2008.1
+ Revision: 175745
- new version

* Thu Feb 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.rc2.3mdv2008.1
+ Revision: 168479
- make it build on cs4

* Mon Feb 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.rc2.2mdv2008.1
+ Revision: 165278
- fix deps

* Wed Jan 30 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.rc2.1mdv2008.1
+ Revision: 160236
- 3.0rc2
- drop P2, it's implemented upstream
- fix #36663 (Error message when installing any nagios plug-in)
- make it back portable (old menu system)
- added a README.Mandriva file that hopefully explains more...
- require a new nagios-conf package for tailoring nagios
- partly fix #36662
- fix #36650 (no LSB tags in init script)

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - own cgi dir, otherwise a restricted root umask make them unusable

* Tue Dec 18 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.rc1.1mdv2008.1
+ Revision: 132454
- 3.0rc1
- fix a %%postun error
- 3.0b7
- rediffed P6
- fix the apache config (duh!)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Thu Nov 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.b6.1mdv2008.1
+ Revision: 104437
- 3.0b6

* Fri Oct 12 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.b5.1mdv2008.1
+ Revision: 97364
- 3.0b5

* Fri Sep 28 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.b4.1mdv2008.0
+ Revision: 93545
- 3.0b4
- drop P3, it was allready applied

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.b3.4mdv2008.0
+ Revision: 83456
- whoops!, it was the other way around :)

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.b3.3mdv2008.0
+ Revision: 83454
- fix the apache config
- fix the %%pre and %%post scriptlets

* Fri Sep 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.b3.2mdv2008.0
+ Revision: 81569
- fix correct path to checkresults

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.0-0.0.b3.1mdv2008.0
+ Revision: 77372
- 3.0b3
- rediffed patches

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 1:2.9-5mdv2008.0
+ Revision: 70376
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago

* Tue Jul 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.9-4mdv2008.0
+ Revision: 55004
- use the new %%serverbuild macro

* Mon Jun 25 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.9-3mdv2008.0
+ Revision: 43826
- fix deps

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.9-2mdv2008.0
+ Revision: 39298
- use distro conditional -fstack-protector

* Tue Apr 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.9-1mdv2008.0
+ Revision: 13743
- 2.9
- 2.9


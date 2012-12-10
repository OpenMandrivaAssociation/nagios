%define nsusr nagios
%define nsgrp nagios
%define cmdusr apache
%define cmdgrp apache

Summary:	Host/service/network monitoring program
Name:		nagios
Version:	3.2.3
%if %mdkversion < 201000
%define subrel  1
%endif
Release:	%mkrel 2
License:	GPLv2
Group:		Networking/Other
URL:		http://www.nagios.org/
Source0:	http://prdownloads.sourceforge.net/nagios/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source4:	http://nagios.sourceforge.net/download/contrib/misc/mergecfg/mergecfg
Source5:	favicon.ico
Patch1:		nagios-scandir.diff
Patch5:		nagios-mdv_conf.diff
Patch6:		nagios-DESTDIR.diff
Patch8:		nagios-3.1.0-no_update_check_per_default_please.diff
Requires(post): rpm-helper nagios-conf
Requires(preun): rpm-helper nagios-conf
Requires(pre): rpm-helper apache-conf
Requires(postun): rpm-helper apache-conf
Requires:	apache-conf
Requires:	nagios-conf
Requires:	nagios-plugins
BuildRequires: 	gd-devel
BuildRequires:	imagemagick
BuildRequires:	jpeg-devel
BuildRequires:  libtool-devel
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	perl-devel
Obsoletes:	netsaint
Provides:	netsaint
Epoch:		1
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package	www
Summary:	Provides the HTML and CGI files for the Nagios web interface
Group:		Networking/WWW
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	webserver
Requires:	freetype
Requires:	freetype2
Requires:	nail
Requires:	traceroute
Requires:	%{name}-imagepaks
Requires:	%{name}-theme
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
Epoch:		%{epoch}

%description	www
Nagios is a program that will monitor hosts and services on your network. It
has the ability to email or page you when a problem arises and when a problem
is resolved. Nagios is written in C and is designed to run under Linux (and
some other *NIX variants) as a background process, intermittently running
checks on various services that you specify.

Several CGI programs are included with Nagios in order to allow you to view the
current service status, problem history, notification history, and log file via
the web. This package provides the HTML and CGI files for the Nagios web
interface. In addition, HTML documentation is included in this package

%package	theme-default
Summary:	Default Nagios theme
Group:		Networking/WWW
Requires(pre): rpm-helper apache-mod_php
Requires(postun): rpm-helper apache-mod_php
Requires:	apache-mod_php
Requires:	nagios-www = %{epoch}:%{version}-%{release}
Provides:	nagios-theme
Conflicts:	nagios-theme-nuvola

%description	theme-default
Original theme from Nagios.

%package	devel
Group:		Development/C
Summary:	Provides include files that Nagios-related applications may compile against
Epoch:		%{epoch}

%description	devel
Nagios is a program that will monitor hosts and services on your network. It
has the ability to email or page you when a problem arises and when a problem
is resolved. Nagios is written in C and is designed to run under Linux (and
some other *NIX variants) as a background process, intermittently running
checks on various services that you specify.

This package provides include files that Nagios-related applications may
compile against.

%prep
%setup -q
%patch1 -p0
%patch5 -p0
%patch6 -p0
%patch8 -p1

cp %{SOURCE1} nagios.init
cp %{SOURCE4} mergecfg
cp %{SOURCE5} favicon.ico

%build
%serverbuild

export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export FFLAGS="$FFLAGS -fPIC"
%define _disable_ld_no_undefined 1
%configure2_5x \
    --with-httpd-conf=%{_sysconfdir}/httpd/conf/webapps.d \
    --with-checkresult-dir=/var/spool/nagios/checkresults \
    --with-temp-dir=/tmp \
    --with-init-dir=%{_initrddir} \
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

%make all

pushd contrib
    make daemonchk.cgi
    make traceroute.cgi
    make mini_epn
    make convertcfg
popd

%install
rm -rf %{buildroot}

install -d -m0755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d -m0755 %{buildroot}/var/spool/nagios/checkresults
install -d -m0755 %{buildroot}/var/run/nagios
install -d -m0755 %{buildroot}%{_includedir}/nagios
install -d -m0755 %{buildroot}%{_initrddir}

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
    install \
    install-html \
    install-commandmode \
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


# install simplified init script
install -m0755 nagios.init %{buildroot}%{_initrddir}/nagios

# install the mergecfg script
install -m0755 mergecfg %{buildroot}%{_sbindir}/nagios-mergecfg

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# Nagios Apache configuration

ScriptAlias /%{name}/cgi-bin %{_libdir}/%{name}/cgi

<Directory %{_libdir}/%{name}/cgi>
    Order allow,deny
    Allow from all
    Options ExecCGI
</Directory>

Alias /%{name} %{_datadir}/%{name}/www

<Directory %{_datadir}/%{name}/www>
    Order allow,deny
    Allow from all
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

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

convert html/images/logofullsize.png -resize 16x16  %{buildroot}%{_miconsdir}/%{name}.png
convert html/images/logofullsize.png -resize 32x32  %{buildroot}%{_iconsdir}/%{name}.png
convert html/images/logofullsize.png -resize 48x48  %{buildroot}%{_liconsdir}/%{name}.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Nagios
Comment=%{summary}
Exec=%{_bindir}/www-browser http://localhost/%{name}/
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Monitoring;System;Monitor;
EOF

%multiarch_includes %{buildroot}%{_includedir}/nagios/locations.h

# install the favicon.ico
install -m0644 favicon.ico %{buildroot}%{_datadir}/nagios/www

cat > README.mdv << EOF
Mandriva Nagios package

The default configuration that used to come with this package now lives in the
nagios-conf package. You can easily adapt the nagios-conf package to suit your
specific taste. You may want to adjust the cgi.cfg, nagios.cfg and resource.cfg
configuration files found in the /etc/nagios directory.

The old nagios-plugins package used to come with all plugins in one single
package has been broken out into multiple sub packages. As of today Jan 14 2008
there are over 100 nagios plugins to your disposal. Here is a list of plugins 
you can install that stems from the nagios-plugins source:

 o nagios-check_adptraid
 o nagios-check_apache
 o nagios-check_apc_ups
 o nagios-check_appletalk
 o nagios-check_apt
 o nagios-check_arping
 o nagios-check_asterisk
 o nagios-check_axis
 o nagios-check_backup
 o nagios-check_bgp
 o nagios-check_bgpstate
 o nagios-check_breeze
 o nagios-check_by_ssh
 o nagios-check_ciscotemp
 o nagios-check_cluster
 o nagios-check_cluster2
 o nagios-check_compaq_insight
 o nagios-check_dhcp
 o nagios-check_dig
 o nagios-check_digitemp
 o nagios-check_disk
 o nagios-check_disk_smb
 o nagios-check_dlswcircuit
 o nagios-check_dns
 o nagios-check_dns_random
 o nagios-check_dummy
 o nagios-check_email_loop
 o nagios-check_file_age
 o nagios-check_flexlm
 o nagios-check_fping
 o nagios-check_frontpage
 o nagios-check_game
 o nagios-check_hpjd
 o nagios-check_hprsc
 o nagios-check_http
 o nagios-check_hw
 o nagios-check_ica_master_browser
 o nagios-check_ica_metaframe_pub_apps
 o nagios-check_ica_program_neigbourhood
 o nagios-check_icmp
 o nagios-check_ide_smart
 o nagios-check_ifoperstatus
 o nagios-check_ifstatus
 o nagios-check_inodes
 o nagios-check_ipxping
 o nagios-check_ircd
 o nagios-check_javaproc
 o nagios-check_ldap
 o nagios-check_linux_raid
 o nagios-check_load
 o nagios-check_log
 o nagios-check_log2
 o nagios-check_lotus
 o nagios-check_mailq
 o nagios-check_maxchannels
 o nagios-check_maxwanstate
 o nagios-check_mem
 o nagios-check_mrtg
 o nagios-check_mrtgext
 o nagios-check_mrtgtraf
 o nagios-check_ms_spooler
 o nagios-check_mssql
 o nagios-check_mysql
 o nagios-check_mysql_perf <- added from third part
 o nagios-check_mysql_query
 o nagios-check_nagios
 o nagios-check_netapp
 o nagios-check_nmap
 o nagios-check_nt
 o nagios-check_ntp
 o nagios-check_ntp_peer
 o nagios-check_ntp_time
 o nagios-check_nwstat
 o nagios-check_oracle
 o nagios-check_overcr
 o nagios-check_pcpmetric
 o nagios-check_pfstate
 o nagios-check_pgsql
 o nagios-check_ping
 o nagios-check_procs
 o nagios-check_qmailq
 o nagios-check_radius
 o nagios-check_rbl
 o nagios-check_real
 o nagios-check_remote_nagios_status
 o nagios-check_rpc
 o nagios-check_sendim
 o nagios-check_sensors
 o nagios-check_smart
 o nagios-check_smb
 o nagios-check_smtp
 o nagios-check_snmp
 o nagios-check_snmp_disk_monitor
 o nagios-check_snmp_printer
 o nagios-check_snmp_process_monitor
 o nagios-check_snmp_procs
 o nagios-check_sockets
 o nagios-check_ssh
 o nagios-check_swap
 o nagios-check_tcp
 o nagios-check_time
 o nagios-check_timeout
 o nagios-check_traceroute
 o nagios-check_ups
 o nagios-check_uptime
 o nagios-check_users
 o nagios-check_wave
 o nagios-check_wins

This break-out has been done to reduce the overall dependencies requirements, 
so if you don't need any of the check_mysql_* plugins you won't have to install
the mysql libraries, and so on.

Each of these packages comes with its own configuration file that contains the
needed command definition(s), let's give an example:

$ cat /etc/nagios/plugins.d/check_arping.cfg
# this plugin require suid bit. chmod 4550 /usr/lib64/nagios/plugins/contrib/check_arping.pl

# 'check_arping' command definition
define command{
	command_name    check_arping
	command_line    /usr/lib64/nagios/plugins/contrib/check_arping.pl -I $ARG1$ -H $HOSTADDRESS$
	}


So when you start the nagios daemon it will automatically load configuration
files found in the /etc/nagios/plugins.d and /etc/nagios/conf.d directories.

EOF

%if %mdkversion >= 200900
# automatic reloading for new plugins
# (see http://wiki.mandriva.com/en/Rpm_filetriggers)
install -d %buildroot%{_var}/lib/rpm/filetriggers
cat > %buildroot%{_var}/lib/rpm/filetriggers/nagios.filter << EOF
^.%{_sysconfdir}/nagios/plugins.d/.*\.cfg$
EOF
cat > %buildroot%{_var}/lib/rpm/filetriggers/nagios.script << EOF
#!/bin/sh
/etc/init.d/nagios condrestart
EOF
chmod 755 %buildroot%{_var}/lib/rpm/filetriggers/nagios.script
%endif

%pre
%{_sbindir}/useradd -r -M -s /bin/sh -d /var/log/nagios -c "system user for %{nsusr}" %{nsusr} >/dev/null 2>&1 || :
%{_bindir}/gpasswd -a %{cmdusr} %{nsgrp} >/dev/null 2>&1 || :

%post
if [ $1 = 1 ] ; then
    chown -R %{nsusr}:%{nsgrp} /var/log/nagios /var/spool/nagios /var/run/nagios >/dev/null 2>&1 || :
fi
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
if [ "$1" -ge "1" ]; then
    %{_initrddir}/%{name} condrestart >/dev/null 2>&1 || :
fi	
%_postun_userdel %{nsusr}

%pretrans www
# fix for old apache configuration
if [ -f %{_sysconfdir}/httpd/conf/webapps.d/12_nagios.conf ]; then
    mv %{_sysconfdir}/httpd/conf/webapps.d/12_nagios.conf \
    %{_sysconfdir}/httpd/conf/webapps.d/nagios.conf
    perl -pi -e 's|%{_datadir}/%{name}|%{_datadir}/%{name}/www|' \
        %{_sysconfdir}/httpd/conf/webapps.d/nagios.conf
fi

%post www
%if %mdkversion < 201010
%_post_webapp
%endif
%if %mdkversion < 200900
%update_menus
%endif

%postun www
%if %mdkversion < 201010
%_postun_webapp
%endif
%if %mdkversion < 200900
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changelog INSTALLING LEGAL README UPGRADING README.mdv
%doc sample-config/mrtg.cfg
%{_initrddir}/nagios
%{_sbindir}/*
%dir %{_sysconfdir}/nagios
%config(noreplace) %{_sysconfdir}/nagios/*.cfg
%dir %{_sysconfdir}/nagios/servers
%dir %{_sysconfdir}/nagios/printers
%dir %{_sysconfdir}/nagios/switches
%dir %{_sysconfdir}/nagios/routers
%dir %{_sysconfdir}/nagios/conf.d
%dir %{_sysconfdir}/nagios/plugins.d
%dir %{_sysconfdir}/nagios/objects
%config(noreplace) %{_sysconfdir}/nagios/objects/*.cfg
%attr(-,%{nsusr},%{nsgrp}) %dir /var/log/nagios
%attr(-,%{nsusr},%{nsgrp}) %dir /var/log/nagios/archives
%attr(2775,%{nsusr},%{cmdgrp}) %dir /var/spool/nagios
%attr(-,%{nsusr},%{nsgrp}) %dir /var/spool/nagios/checkresults
%attr(-,%{nsusr},%{nsgrp}) %dir /var/run/nagios
%dir %{_libdir}/nagios/plugins/eventhandlers
%{_libdir}/nagios/plugins/eventhandlers/*
%if %mdkversion >= 200900
%{_var}/lib/rpm/filetriggers/nagios.*
%endif

%files www
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/nagios.conf
%{_libdir}/nagios/cgi
%dir %{_datadir}/nagios/www
%dir %{_datadir}/nagios/www/images
%dir %{_datadir}/nagios/www/stylesheets
%{_datadir}/nagios/www/favicon.ico
%{_datadir}/nagios/www/robots.txt
%{_datadir}/nagios/www/contexthelp
%{_datadir}/nagios/www/docs
%{_datadir}/nagios/www/media
%{_datadir}/nagios/www/ssi
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop

%files theme-default
%defattr(-,root,root)
%{_datadir}/nagios/www/*.php
%{_datadir}/nagios/www/images/*
%{_datadir}/nagios/www/includes/*
%{_datadir}/nagios/www/stylesheets/*

%files devel
%defattr(-,root,root)
%multiarch %{multiarch_includedir}/nagios/locations.h

%{_includedir}/nagios


%changelog
* Sat Feb 05 2011 Funda Wang <fwang@mandriva.org> 1:3.2.3-2mdv2011.0
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

  + Olivier Blin <oblin@mandriva.com>
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


* Thu Jan 25 2007 Oden Eriksson <oeriksson@mandriva.com> 2.7-1mdv2007.0
+ Revision: 113174
- 2.7
- make it backportable

* Thu Nov 30 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.6-1mdv2007.1
+ Revision: 89047
- 2.6
- remove obsolete patches and add one new one
- remove obsolete sources
- generate a password if needed for the nagios web user
- added a README.urpmi file outlining the changes

* Wed Nov 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.5-5mdv2007.1
+ Revision: 84428
- Import nagios

* Wed Nov 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.5-6mdv2007.1
- use the www-browser script instead
- fix the xdg menu
- remove conditional build switches for unsupported distros
- bunzip sources

* Thu Sep 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.5-5mdv2007.0
- don't enforce ssl redirect

* Fri Aug 04 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.5-4mdv2007.0
- fix typo

* Thu Aug 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.5-3mdv2007.0
- fix xdg menu stuff

* Thu Aug 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.5-2mdv2007.0
- fix deps

* Sat Jul 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.5-1mdv2007.0
- 2.5 (Minor bugfixes)

* Mon Jul 03 2006 Emmanuel Andry <eandry@mandriva.org> 1:2.4-2mdv2007.0
- fix buildrequires

* Fri Jun 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.4-1mdv2007.0
- 2.4 (Minor bugfixes)
- rediffed P8

* Wed May 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.3.1-1mdk
- 2.3.1 (Major security fixes)

* Sun May 14 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.3-3mdk
- fix better apache config

* Thu May 11 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.3-2mdk
- fix deps
- relocate the /admin/nagios url to /nagios
- fix better apache config
- fix a menuentry

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.3-1mdk
- 2.3 (Minor security fixes)

* Sun Apr 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2-1mdk
- 2.2 (Minor bugfixes)

* Sat Apr 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-2mdk
- fix deps and #20711

* Tue Mar 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-1mdk
- 2.1 (Minor bugfixes)

* Thu Feb 23 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-3mdk
- install the apache config depending on distro

* Tue Feb 14 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-2mdk
- fix deps

* Wed Feb 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-1mdk
- 2.0 (Minor bugfixes)

* Wed Jan 11 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0rc2-1mdk
- 2.0rc2 (Minor bugfixes)
- rediffed P2

* Thu Dec 01 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0b6-1mdk
- 2.0b5 (Minor bugfixes)

* Tue Nov 15 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0b5-1mdk
- 2.0b5 (Minor bugfixes)
- remove strip calls (P8)

* Wed Oct 19 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0b4-2mdk
- fix #19312

* Thu Aug 04 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0b4-1mdk
- 2.0b4 (Minor bugfixes)
- fix %%post and %%postun for the nagios-www package
- fix deps

* Tue May 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0b4-0.20050530.1mdk
- use a recent snap (20050530)
- added a nice favicon.ico patch by PLD (S5 & P6)
- added a patch by Andreas Ericsson (P7)

* Thu May 26 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0b3-2mdk
- fix #13814

* Tue Apr 05 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0b3-1mdk
- 2.0b3
- added P5 to make the shipped minimalistic config work again

* Mon Apr 04 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0b2-4mdk
- use the %%mkrel macro

* Sat Feb 19 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0b2-3mdk
- added P4 to bring back some missing stuff
- handle the %%postun better

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0b2-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Thu Feb 10 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0b2-1mdk
- 2.0b2
- rediffed P0
- make it compile on x86_64

* Thu Feb 10 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0a1-0.20041024.3mdk
- set LC_ALL=C in the initscript in an attempt to fix #12740 like future issues
- fix deps and conditional %%multiarch

* Mon Nov 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0a1-0.20041024.2mdk
- added S2
- enhanced the init scipt a bit (S1)

* Mon Oct 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0a1-0.20041024.1mdk
- 20041024

* Mon Oct 04 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0a1-0.20041002.2mdk
- fix one typo

* Mon Oct 04 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0a1-0.20041002.1mdk
- cvs snap 20041002 of 2.0a1
- added the long forgotten eventhandlers
- new S2
- added P2 & P3
- misc spec file fixes

* Tue Jul 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2-4mdk
- added P1 to make it recognize the correct gd stuff

* Sat Jun 12 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2-3mdk
- rebuilt against new gd

* Sun May 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2-2mdk
- fix #9762 (revert changes in 1.2-1mdk)
- fix deps

* Wed Mar 03 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 1.2-1mdk
- 1.2
- fixed 12_nagios.conf


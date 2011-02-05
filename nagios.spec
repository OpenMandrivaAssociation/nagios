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

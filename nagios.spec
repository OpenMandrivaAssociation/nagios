%define nsusr nagios
%define nsgrp nagios
%define cmdusr apache
%define cmdgrp apache

Summary:	Host/service/network monitoring program
Name:		nagios
Version:	3.3.1
Release:	%mkrel 1
License:	GPLv2
Group:		Networking/Other
URL:		http://www.nagios.org/
Source0:	http://prdownloads.sourceforge.net/nagios/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source4:	http://nagios.sourceforge.net/download/contrib/misc/mergecfg/mergecfg
Source5:	favicon.ico
Patch1:         nagios-scandir.diff
Patch2:         nagios-mdv_conf.diff
Patch6:         nagios-DESTDIR.diff
Patch7:     	nagios-3.3.1-change-update-check-default.patch
Patch8:     	nagios-3.3.1-fix-html-install.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache
Requires:	nagios-plugins
BuildRequires: 	gd-devel
BuildRequires:	imagemagick
BuildRequires:	jpeg-devel
BuildRequires:  libtool-devel
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	perl-devel
Epoch:		1

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
Requires:	apache-mod_php
Requires:	nagios-www = %{epoch}:%{version}-%{release}
Provides:	nagios-theme
Conflicts:	nagios-theme-nuvola
BuildArch:  noarch

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
%setup -q -n nagios
%patch1 -p0
%patch2 -p0
%patch6 -p0
%patch7 -p1
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
    --with-httpd-conf=%{_webappconfdir} \
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

install -d -m0755 %{buildroot}%{_webappconfdir}
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

#multiarch_includes %{buildroot}%{_includedir}/nagios/locations.h

# install the favicon.ico
install -m0644 favicon.ico %{buildroot}%{_datadir}/nagios/www

# automatic reloading for new plugins
install -d %buildroot%{_var}/lib/rpm/filetriggers
cat > %buildroot%{_var}/lib/rpm/filetriggers/nagios.filter << EOF
^.%{_sysconfdir}/nagios/plugins.d/.*\.cfg$
EOF
cat > %buildroot%{_var}/lib/rpm/filetriggers/nagios.script << EOF
#!/bin/sh
/etc/init.d/nagios condrestart
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
%{_initrddir}/nagios
%{_sbindir}/*
%dir %{_sysconfdir}/nagios
%dir %{_sysconfdir}/nagios/servers
%dir %{_sysconfdir}/nagios/printers
%dir %{_sysconfdir}/nagios/switches
%dir %{_sysconfdir}/nagios/routers
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
%dir %{_datadir}/nagios/www
%dir %{_datadir}/nagios/www/images
%dir %{_datadir}/nagios/www/stylesheets
%{_datadir}/nagios/www/favicon.ico
%{_datadir}/nagios/www/robots.txt
%{_datadir}/nagios/www/contexthelp
%{_datadir}/nagios/www/docs
%{_datadir}/nagios/www/media
%{_datadir}/nagios/www/ssi

%files theme-default
%{_datadir}/nagios/www/*.php
%{_datadir}/nagios/www/images/*
%{_datadir}/nagios/www/includes/*
%{_datadir}/nagios/www/stylesheets/*

%files devel
#multiarch %{multiarch_includedir}/nagios/locations.h
%{_includedir}/nagios



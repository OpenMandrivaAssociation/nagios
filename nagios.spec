%define nsusr nagios
%define nsgrp nagios
%define cmdusr apache
%define cmdgrp apache

Summary:	Host/service/network monitoring program
Name:		nagios
Version:	3.1.2
%if %mdkversion < 201000
%define subrel  1
%endif
Release:	%mkrel 1
License:	GPLv2
Group:		Networking/Other
URL:		http://www.nagios.org/
Source0:	http://prdownloads.sourceforge.net/nagios/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source4:	http://nagios.sourceforge.net/download/contrib/misc/mergecfg/mergecfg
Source5:	favicon.ico
Source6:	README.Mandriva
Patch1:		nagios-scandir.diff
Patch5:		nagios-mdv_conf.diff
Patch6:		nagios-DESTDIR.diff
Patch7:		nagios-3.1.0-format_not_a_string_literal_and_no_format_arguments.diff
Patch8:		nagios-3.1.0-no_update_check_per_default_please.diff
Requires(post): rpm-helper nagios-conf
Requires(preun): rpm-helper nagios-conf
Requires(pre): rpm-helper apache-conf
Requires(postun): rpm-helper apache-conf
Requires:	apache-conf
Requires:	nagios-conf
Requires:	nagios-plugins
BuildRequires:	freetype2-devel
BuildRequires:	freetype-devel
BuildRequires: 	gd-devel
BuildRequires:	imagemagick
BuildRequires:	jpeg-devel
BuildRequires:  libtool
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	nail
BuildRequires:	perl-devel
BuildRequires:	png-devel
BuildRequires:	X11-devel
BuildRequires:	xpm-devel
BuildRequires:	zlib-devel
BuildRequires: 	gdbm-devel
BuildRequires: 	perl-devel
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
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper apache-mpm-prefork
Requires(postun): rpm-helper apache-mpm-prefork
Requires(post): %{name} = %{epoch}:%{version}-%{release}
Requires(preun): %{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	apache-mpm-prefork
Requires:	freetype
Requires:	freetype2
Requires:	nail
Requires:	perl
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
%patch7 -p0
%patch8 -p1

cp %{SOURCE1} nagios.init
cp %{SOURCE4} mergecfg
cp %{SOURCE5} favicon.ico
cp %{SOURCE6} README.Mandriva

%build
%serverbuild

export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export FFLAGS="$FFLAGS -fPIC"

./configure \
    --prefix=%{_prefix} \
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
find %{buildroot}%{_libdir}/nagios/cgi -type f | xargs chmod 755

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
    Options ExecCGI
    Allow from all
</Directory>

Alias /%{name} %{_datadir}/%{name}/www

<Directory %{_datadir}/%{name}/www>
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

%if %mdkversion == 200600
# install menu entry.
install -d %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} << EOF
?package(%{name}): \
needs=X11 \
section=System/Monitoring \
title="Nagios" \
longtitle="%{summary}" \
command="%{_bindir}/www-browser http://localhost/%{name}/" \
icon="%{name}.png"
EOF
%endif

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

cat > README.urpmi << EOF
The previous minimalistic config files is not needed anymore since nagios-2.6
works out of the box now. You will have to manually merge any changes you have
made in the config files.
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
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null 2>&1 || :
fi
%if %mdkversion < 200900
%update_menus
%endif

%postun www
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart >/dev/null 2>&1 || :
    fi
fi
%if %mdkversion < 200900
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changelog INSTALLING LEGAL README* UPGRADING README.urpmi sample-config/mrtg.cfg
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
%if %mdkversion == 200600
%{_menudir}/%{name}
%endif
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

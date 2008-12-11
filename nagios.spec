%define nsusr nagios
%define nsgrp nagios
%define cmdusr apache
%define cmdgrp apache

Summary:	Host/service/network monitoring program
Name:		nagios
Version:	3.0.6
Release:	%mkrel 1
License:	GPLv2
Group:		Networking/Other
URL:		http://www.nagios.org/
Source0:	http://prdownloads.sourceforge.net/nagios/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source4:	http://nagios.sourceforge.net/download/contrib/misc/mergecfg/mergecfg
Source5:	favicon.ico
Source6:	README.Mandriva
Patch0:		nagios-optflags.diff
Patch1:		nagios-scandir.diff
Patch4:		nagios-no_strip.diff
Patch5:		nagios-mdv_conf.diff
Patch6:		nagios-DESTDIR.diff
Requires(post): rpm-helper nagios-conf
Requires(preun): rpm-helper nagios-conf
Requires(pre): rpm-helper apache-conf
Requires(postun): rpm-helper apache-conf
Requires:	apache-conf
Requires:	nagios-conf
Requires:	coreutils
Requires:	gawk
Requires:	grep
Requires:	nagios-plugins
Requires:	perl
Requires:	shadow-utils
BuildRequires:  autoconf2.5
BuildRequires:  automake1.7
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
# use this when embedded perl works in nagios
#Requires:	libgdbm2
#BuildRequires: 	libgdbm2-devel
#BuildRequires: 	perl-devel
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

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch0 -p1
%patch1 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0

cp %{SOURCE1} nagios.init
cp %{SOURCE4} mergecfg
cp %{SOURCE5} favicon.ico
cp %{SOURCE6} README.Mandriva

%build
export WANT_AUTOCONF_2_5=1
rm -f configure; touch missing
libtoolize --copy --force; aclocal-1.7; autoconf
#; automake --add-missing

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
    --with-gd-inc=%{_includedir}

# use this when embedded perl works in nagios
#    --enable-embedded-perl \
#    --with-perlcache \

# bug
perl -pi -e "s|/var/log/nagios/spool/checkresults|/var/spool/nagios/checkresults|g" include/locations.h

%make all

pushd contrib
    make daemonchk.cgi
    make traceroute.cgi
# use this when embedded perl works in nagios
#    make mini_epn
    make convertcfg
popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

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
    HTMLDIR=%{_datadir}/nagios \
    INIT_OPTS="" \
    INSTALL=install \
    INSTALL_OPTS="" \
    LOGDIR=/var/log/nagios \
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
	HTMLDIR=%{_datadir}/nagios \
	INIT_OPTS="" \
	INSTALL=install \
	INSTALL_OPTS="" \
	LOGDIR=/var/log/nagios \
	install
popd

# fix strange dir perms
find %{buildroot}%{_datadir}/nagios -type d | xargs chmod 755

# fix default config
perl -p -i -e "s|=/var/log/nagios/rw/|=/var/spool/nagios/|g" %{buildroot}%{_sysconfdir}/nagios/*

# install simplified init script
install -m0755 nagios.init %{buildroot}%{_initrddir}/nagios

# install the mergecfg script
install -m0755 mergecfg %{buildroot}%{_sbindir}/nagios-mergecfg

# fix web access
cat > apache-nagios.conf << EOF
# WITHOUT SSL

<IfModule !mod_ssl.c>

    ScriptAlias /%{name}/cgi-bin %{_libdir}/%{name}/cgi

    <Directory %{_libdir}/%{name}/cgi>
        Options ExecCGI
        order deny,allow
        deny from all
        allow from 127.0.0.1
	ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/12_nagios.conf"
	AuthType Basic
	AuthUserFile %{_sysconfdir}/%{name}/passwd
	AuthGroupFile %{_sysconfdir}/%{name}/group
	AuthName "Nagios Access"
	Require group nagios
	Satisfy Any
    </Directory>

    Alias /%{name} %{_datadir}/%{name}

    <Directory %{_datadir}/%{name}>
        Options None
        order deny,allow
        deny from all
        allow from 127.0.0.1
	ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/12_nagios.conf"
	AuthType Basic
	AuthUserFile %{_sysconfdir}/%{name}/passwd
	AuthGroupFile %{_sysconfdir}/%{name}/group
	AuthName "Nagios Access"
	Require group nagios
	Satisfy Any
    </Directory>

</IfModule>

# WITH SSL ENABLED

<IfModule mod_ssl.c>

    ScriptAlias /%{name}/cgi-bin %{_libdir}/%{name}/cgi

    <Directory %{_libdir}/%{name}/cgi>
	Options ExecCGI
	SSLRequireSSL
	Order Deny,Allow
	Deny from all
	AuthType Basic
	AuthUserFile %{_sysconfdir}/%{name}/passwd
	AuthGroupFile %{_sysconfdir}/%{name}/group
	AuthName "Nagios Access"
	Require group nagios
	Satisfy Any
    </Directory>

    Alias /%{name} %{_datadir}/%{name}

    <Directory %{_datadir}/%{name}>
	Options None
	SSLRequireSSL
	Order Deny,Allow
	Deny from all
	AuthType Basic
	AuthUserFile %{_sysconfdir}/%{name}/passwd
	AuthGroupFile %{_sysconfdir}/%{name}/group
	AuthName "Nagios Access"
	Require group nagios
	Satisfy Any
    </Directory>

# Uncomment the following lines to force a redirect to a working
# SSL aware apache server. This serves as an example.
#    <LocationMatch /%{name}>
#	Options FollowSymLinks
#	RewriteEngine on
#	RewriteCond %{SERVER_PORT} !^443$
#	RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
#    </LocationMatch>

</IfModule>

EOF
install -m0644 apache-nagios.conf %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/12_nagios.conf

echo "%{name}:" > %{buildroot}%{_sysconfdir}/nagios/passwd
echo "%{name}: root %{name}" > %{buildroot}%{_sysconfdir}/nagios/group

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
install -m0644 favicon.ico %{buildroot}%{_datadir}/nagios/

cat > README.urpmi << EOF
The previous minimalistic config files is not needed anymore since nagios-2.6
works out of the box now. You will have to manually merge any changes you have
made in the config files. When installing nagios-www a password for the nagios
web access user will be generated if needed. The password will be saved in
clear text in the /etc/nagios/passwd.plaintext file.
EOF

# cleanup
rm -f %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/nagios.conf

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

%post www
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null 2>&1 || :
fi
%if %mdkversion < 200900
%update_menus
%endif

if [ -z "`cat %{_sysconfdir}/%{name}/passwd|cut -d: -f2`" ]; then
    echo "Setting a unique password for the %{name} web user. As root look in the %{_sysconfdir}/%{name}/passwd.plaintext file to view it."
    PASSWORD=`perl -e 'for ($i = 0, $bit = "!", $key = ""; $i < 8; $i++) {while ($bit !~ /^[0-9A-Za-z]$/) { $bit = chr(rand(90) + 32); } $key .= $bit; $bit = "!"; } print "$key";'`
    %{_sbindir}/htpasswd -b %{_sysconfdir}/%{name}/passwd %{name} $PASSWORD
    echo "$PASSWORD" > %{_sysconfdir}/%{name}/passwd.plaintext
    chmod 600 %{_sysconfdir}/%{name}/passwd.plaintext
fi

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
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changelog INSTALLING LEGAL README* UPGRADING README.urpmi sample-config/mrtg.cfg
%attr(0755,root,root) %{_initrddir}/nagios
%attr(0755,root,root) %{_sbindir}/*
%attr(0755,root,root) %dir %{_sysconfdir}/nagios
%attr(0644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/*.cfg
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/servers
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/printers
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/switches
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/routers
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/conf.d
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/plugins.d
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/objects
%attr(0644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/objects/*.cfg
%attr(0755,%{nsusr},%{nsgrp}) %dir /var/log/nagios
%attr(0755,%{nsusr},%{nsgrp}) %dir /var/log/nagios/archives
%attr(2775,%{nsusr},%{cmdgrp}) %dir /var/spool/nagios
%attr(0755,%{nsusr},%{nsgrp}) %dir /var/spool/nagios/checkresults
%attr(0755,%{nsusr},%{nsgrp}) %dir /var/run/nagios
%attr(0755,root,root) %dir %{_libdir}/nagios/plugins/eventhandlers
%attr(0755,root,root) %{_libdir}/nagios/plugins/eventhandlers/*

%files www
%defattr(-,root,root)
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/conf/webapps.d/*_nagios.conf
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/passwd
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/group
%attr(0755,root,root) %{_libdir}/nagios/cgi/*
#%attr(-,root,root) %{_datadir}/nagios
%attr(-,root,root) %dir %{_libdir}/nagios/cgi
%attr(-,root,root) %dir %{_datadir}/nagios
%attr(-,root,root) %dir %{_datadir}/nagios/images
%attr(-,root,root) %dir %{_datadir}/nagios/stylesheets
%{_datadir}/nagios/favicon.ico
%{_datadir}/nagios/robots.txt
%{_datadir}/nagios/contexthelp
%{_datadir}/nagios/docs
%{_datadir}/nagios/media
%{_datadir}/nagios/ssi
%if %mdkversion == 200600
%{_menudir}/%{name}
%endif
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop

%files theme-default
%defattr(644,root,root,755)
%{_datadir}/nagios/*.html
%{_datadir}/nagios/images/*
%{_datadir}/nagios/stylesheets/*

%files devel
%defattr(-,root,root)
%multiarch %{multiarch_includedir}/nagios/locations.h
%{_includedir}/nagios

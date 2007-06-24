%define nsusr nagios
%define nsgrp nagios
%define cmdusr apache
%define cmdgrp apache

Summary:	Host/service/network monitoring program
Name:		nagios
Version:	2.9
Release:	%mkrel 3
License:	GPL
Group:		Networking/Other
URL:		http://www.nagios.org/
Source0:	http://prdownloads.sourceforge.net/nagios/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source4:	http://nagios.sourceforge.net/download/contrib/misc/mergecfg/mergecfg
Source5:	favicon.ico
Patch0:		nagios-optflags.diff
Patch3:		nagios-scandir.diff
Patch6:		nagios-favicon.diff
Patch7:		nagios-nonroot-no_priv_drop.diff
Patch8:		nagios-no_strip.diff
Patch9:		nagios-2.6-mdv_conf.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper apache-conf
Requires(postun): rpm-helper apache-conf
Requires:	apache-conf
Requires:	gawk
Requires:	grep
Requires:	nagios-plugins
Requires:	shadow-utils
Requires:	textutils
Requires:	perl
BuildRequires:	freetype2-devel
BuildRequires:	freetype-devel
BuildRequires: 	gd-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	xpm-devel
BuildRequires:	XFree86-devel
BuildRequires:	zlib-devel
BuildRequires:	perl-devel
BuildRequires:  autoconf2.5
BuildRequires:  automake1.7
BuildRequires:  libtool
BuildRequires:	ImageMagick
BuildRequires:	multiarch-utils >= 1.0.3
# use this when embedded perl works in nagios
#Requires:	libgdbm2
#BuildRequires: 	libgdbm2-devel
#BuildRequires: 	perl-devel
Obsoletes:	netsaint
Provides:	netsaint
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-buildroot

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
Requires(pre): rpm-helper apache-mpm
Requires(postun): rpm-helper apache-mpm
Requires(post): %{name} = %{epoch}:%{version}-%{release}
Requires(preun): %{name} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	apache-mpm
Requires:	freetype
Requires:	freetype2
Requires:	mailx
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
Obsoletes:	nagios-theme

%description theme-default
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

%setup -q -n %{name}-%{version}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done
    
%patch0 -p1 -b .optflags
%patch3 -p0
%patch6 -p1
%patch7 -p0
%patch8 -p0
%patch9 -p1

cp %{SOURCE1} nagios.init
cp %{SOURCE4} mergecfg
cp %{SOURCE5} favicon.ico

%build
export WANT_AUTOCONF_2_5=1
rm -f configure; touch missing
libtoolize --copy --force; aclocal-1.7; autoconf
#; automake --add-missing

export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
export FFLAGS="%{optflags} -fPIC"

%if %mdkversion >= 200710
export CFLAGS="$CFLAGS -fstack-protector"
export CXXFLAGS="$CXXFLAGS -fstack-protector"
export FFLAGS="$FFLAGS -fstack-protector"
%endif


./configure \
    --prefix=%{_prefix} \
    --with-init-dir=%{_initrddir} \
    --exec-prefix=%{_sbindir} \
    --bindir=%{_sbindir} \
    --sbindir=%{_libdir}/nagios/cgi \
    --libexecdir=%{_libdir}/nagios/plugins \
    --datadir=%{_datadir}/nagios \
    --sysconfdir=%{_sysconfdir}/nagios \
    --localstatedir=%{_var}/log/nagios \
    --with-lockfile=%{_var}/run/nagios/nagios.pid \
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
install -d -m0755 %{buildroot}%{_var}/spool/nagios
install -d -m0755 %{buildroot}%{_var}/run/nagios
install -d -m0755 %{buildroot}%{_includedir}/nagios
install -d -m0755 %{buildroot}%{_initrddir}

install -d -m0755 %{buildroot}%{_sysconfdir}/nagios/{servers,printers,switches,routers,plugins.d}
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
    LOGDIR=%{_var}/log/nagios \
    install \
    install-html \
    install-commandmode \
    install-config \
    fullinstall

install -m0644 sample-config/cgi.cfg %{buildroot}%{_sysconfdir}/nagios/
install -m0644 sample-config/nagios.cfg %{buildroot}%{_sysconfdir}/nagios/
install -m0644 sample-config/resource.cfg %{buildroot}%{_sysconfdir}/nagios/
install -m0644 sample-config/template-object/commands.cfg %{buildroot}%{_sysconfdir}/nagios/
install -m0644 sample-config/template-object/localhost.cfg %{buildroot}%{_sysconfdir}/nagios/

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
	LOGDIR=%{_var}/log/nagios \
	install
popd

# fix strange dir perms
find %{buildroot}%{_datadir}/nagios -type d | xargs chmod 755

# fix default config
perl -p -i -e "s|=%{_var}/log/nagios/rw/|=%{_var}/spool/nagios/|g" %{buildroot}%{_sysconfdir}/nagios/*

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
    </Directory>

    Alias /%{name} %{_datadir}/%{name}

    <Directory %{_datadir}/%{name}>
        Options None
        order deny,allow
        deny from all
        allow from 127.0.0.1
	ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/12_nagios.conf"
    </Directory>

</IfModule>

# WITH SSL ENABLED

<IfModule mod_ssl.c>

    ScriptAlias /%{name}/cgi-bin %{_libdir}/%{name}/cgi

    <Directory %{_libdir}/%{name}/cgi>
	Options ExecCGI
	SSLRequireSSL
	order deny,allow
	deny from all
	AuthType Basic
	AuthUserFile %{_sysconfdir}/%{name}/passwd
	AuthGroupFile %{_sysconfdir}/%{name}/group
	AuthName "%{name}"
	require group %{name}
	Satisfy Any
    </Directory>

    Alias /%{name} %{_datadir}/%{name}

    <Directory %{_datadir}/%{name}>
	Options None
	SSLRequireSSL
	order deny,allow
	deny from all
	AuthType Basic
	AuthUserFile %{_sysconfdir}/%{name}/passwd
	AuthGroupFile %{_sysconfdir}/%{name}/group
	AuthName "%{name}"
	require group %{name}
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

find %{buildroot}%{_libdir}/nagios/plugins/eventhandlers -type f | xargs perl -pi -e "s|/usr/local/nagios%{_var}/rw/|%{_var}/spool/nagios/|g"
find %{buildroot}%{_libdir}/nagios/plugins/eventhandlers -type f | xargs perl -pi -e "s|/usr/local/nagios/libexec/eventhandlers|%{_libdir}/nagios/plugins/eventhandlers|g"
find %{buildroot}%{_libdir}/nagios/plugins/eventhandlers -type f | xargs perl -pi -e "s|/usr/local/nagios/libexec/send_nsca|%{_libdir}/nagios/plugins/send_nsca|g"
find %{buildroot}%{_libdir}/nagios/plugins/eventhandlers -type f | xargs perl -pi -e "s|/usr/local/nagios/test%{_var}|%{_var}/log/nagios|g"
find %{buildroot}%{_libdir}/nagios/plugins/eventhandlers -type f | xargs perl -pi -e "s|/usr/local/nagios/etc/send_nsca.cfg|%{_sysconfdir}/nagios/send_nsca.cfg|g"

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

convert html/images/logofullsize.jpg -resize 16x16  %{buildroot}%{_miconsdir}/%{name}.png
convert html/images/logofullsize.jpg -resize 32x32  %{buildroot}%{_iconsdir}/%{name}.png
convert html/images/logofullsize.jpg -resize 48x48  %{buildroot}%{_liconsdir}/%{name}.png

# install menu entry.
install -d %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} << EOF
?package(%{name}): \
needs=X11 \
section=System/Monitoring \
title="Nagios" \
longtitle="%{summary}" \
command="%{_bindir}/www-browser http://localhost/%{name}/" \
icon="%{name}.png" \
xdg="true"
EOF

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Nagios
Comment=%{summary}
Exec="%{_bindir}/www-browser http://localhost/%{name}/"
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

%pre
%_pre_useradd %{nsusr} %{_var}/log/nagios /bin/sh
# this logic is taken from sympa
groups=`groups %{cmdgrp} | cut -d " " -f 4- | tr ' ' ,`
if [ -n "$groups" ]; then
    groups="$groups,%{nsgrp}"
else
    groups="%{nsgrp}";
fi
usermod -G $groups %{cmdgrp}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{nsusr}

if [ "$1" -ge "1" ]; then
    /sbin/service nagios condrestart >/dev/null 2>&1
fi

%post www
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi
%update_menus

if [ -z "`cat %{_sysconfdir}/%{name}/passwd|cut -d: -f2`" ]; then
    echo "Setting a unique password for the %{name} web user. As root look in the %{_sysconfdir}/%{name}/passwd.plaintext file to view it."
    PASSWORD=`perl -e 'for ($i = 0, $bit = "!", $key = ""; $i < 8; $i++) {while ($bit !~ /^[0-9A-Za-z]$/) { $bit = chr(rand(90) + 32); } $key .= $bit; $bit = "!"; } print "$key";'`
    %{_sbindir}/htpasswd -b %{_sysconfdir}/%{name}/passwd %{name} $PASSWORD
    echo "$PASSWORD" > %{_sysconfdir}/%{name}/passwd.plaintext
    chmod 600 %{_sysconfdir}/%{name}/passwd.plaintext
fi

%postun www
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi
%clean_menus

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changelog INSTALLING LEGAL README* UPGRADING README.urpmi sample-config/mrtg.cfg
%attr(0755,root,root) %{_initrddir}/nagios
%attr(0755,root,root) %{_sbindir}/*
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/*-sample
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/*.cfg
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/servers
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/printers
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/switches
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/routers
%attr(0755,root,root) %dir %{_sysconfdir}/nagios/plugins.d
%attr(0755,%{nsusr},%{nsgrp}) %dir %{_var}/log/nagios
%attr(0755,%{nsusr},%{nsgrp}) %dir %{_var}/log/nagios/archives
%attr(2775,%{nsusr},%{cmdgrp}) %dir %{_var}/spool/nagios
%attr(0755,%{nsusr},%{nsgrp}) %dir %{_var}/run/nagios
%attr(0755,root,root) %{_libdir}/nagios/plugins/eventhandlers/*

%files www
%defattr(-,root,root)
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/conf/webapps.d/*_nagios.conf
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/passwd
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/group
%attr(0755,root,root) %{_libdir}/nagios/cgi/*
#%attr(-,root,root) %{_datadir}/nagios
%attr(-,root,root) %dir %{_datadir}/nagios
%attr(-,root,root) %dir %{_datadir}/nagios/images
%attr(-,root,root) %dir %{_datadir}/nagios/stylesheets
%{_datadir}/nagios/favicon.ico
%{_datadir}/nagios/robots.txt
%{_datadir}/nagios/contexthelp
%{_datadir}/nagios/docs
%{_datadir}/nagios/media
%{_datadir}/nagios/ssi

%{_menudir}/%{name}
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

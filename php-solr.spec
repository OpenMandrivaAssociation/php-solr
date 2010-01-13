%define modname solr
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B07_%{modname}.ini

Summary:	Simplifies the process of interacting with Apache Solr using PHP
Name:		php-%{modname}
Version:	0.9.9
Release:	%mkrel 1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/solr/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.11
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	libxml2-devel >= 2.6.31
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Apache Solr extension is an extremely fast, light-weight, feature-rich
library that allows PHP developers to communicate easily and efficiently with
Apache Solr server instances using an object-oriented API.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

find -type f | xargs chmod 644

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-libxml-dir=%{_prefix} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS LICENSE README* TODO package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


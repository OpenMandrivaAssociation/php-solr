%define modname solr
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B07_%{modname}.ini

Summary:	Simplifies the process of interacting with Apache Solr using PHP
Name:		php-%{modname}
Version:	1.0.2
Release:	%mkrel 3
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/solr/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.11
BuildRequires:	curl-devel >= 7.15.0
BuildRequires:	libxml2-devel >= 2.6.26
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


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-3mdv2012.0
+ Revision: 795499
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2
+ Revision: 761292
- rebuild

* Wed Dec 07 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1
+ Revision: 738653
- 1.0.2

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-3
+ Revision: 696468
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2
+ Revision: 695463
- rebuilt for php-5.3.7

* Tue Jun 07 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1
+ Revision: 683040
- 1.0.1

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.11-6
+ Revision: 646683
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.11-5mdv2011.0
+ Revision: 629869
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.11-4mdv2011.0
+ Revision: 628189
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.11-3mdv2011.0
+ Revision: 600529
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.11-2mdv2011.0
+ Revision: 588867
- rebuild

* Thu Sep 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.11-1mdv2011.0
+ Revision: 578879
- 0.9.11

* Thu May 06 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.10-1mdv2010.1
+ Revision: 542992
- 0.9.10
- adjust deps

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.9-2mdv2010.1
+ Revision: 514652
- rebuilt for php-5.3.2

* Wed Jan 13 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.9-1mdv2010.1
+ Revision: 490651
- 0.9.9

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.8-2mdv2010.1
+ Revision: 485481
- rebuilt for php-5.3.2RC1

* Wed Dec 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.8-1mdv2010.1
+ Revision: 475234
- 0.9.8

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.7-2mdv2010.1
+ Revision: 468252
- rebuilt against php-5.3.1

* Thu Nov 19 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.7-1mdv2010.1
+ Revision: 467405
- 0.9.7

* Fri Nov 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-1mdv2010.1
+ Revision: 461166
- 0.9.6
- import php-solr


* Tue Oct 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-1mdv2010.0
- initial Mandriva package

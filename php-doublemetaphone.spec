%define modname doublemetaphone
%define soname %{modname}.so
%define inifile A71_%{modname}.ini

Summary:	Provide Double Metaphone functionality
Name:		php-%{modname}
Version:	1.0.0
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/doublemetaphone
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Double Metaphone algorithm by Lawrence Philips allows a word to be
broken down into its phonemes.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}/var/log/httpd

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

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
%doc package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2012.0
+ Revision: 795426
- rebuild for php-5.4.x

* Tue Mar 27 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1
+ Revision: 787456
- 1.0.0

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-21
+ Revision: 761217
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-20
+ Revision: 696410
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-19
+ Revision: 695383
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-18
+ Revision: 646626
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-17mdv2011.0
+ Revision: 629781
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-16mdv2011.0
+ Revision: 628092
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-15mdv2011.0
+ Revision: 600475
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-14mdv2011.0
+ Revision: 588757
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-13mdv2010.1
+ Revision: 514530
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-12mdv2010.1
+ Revision: 485351
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-11mdv2010.1
+ Revision: 468157
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-10mdv2010.0
+ Revision: 451262
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.2.0-9mdv2010.0
+ Revision: 397359
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-8mdv2010.0
+ Revision: 376982
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-7mdv2009.1
+ Revision: 346415
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-6mdv2009.1
+ Revision: 341720
- rebuilt against php-5.2.9RC2

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-5mdv2009.1
+ Revision: 324288
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-4mdv2009.1
+ Revision: 310260
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-3mdv2009.0
+ Revision: 238387
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-2mdv2009.0
+ Revision: 200195
- rebuilt for php-5.2.6

* Wed Apr 09 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-1mdv2009.0
+ Revision: 192502
- 0.2.0

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-3mdv2008.1
+ Revision: 162137
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-2mdv2008.1
+ Revision: 107612
- restart apache if needed

* Mon Nov 05 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2008.1
+ Revision: 106187
- import php-doublemetaphone


* Mon Nov 05 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2008.1
- initial Mandriva package

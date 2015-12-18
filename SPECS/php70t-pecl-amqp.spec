%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?pecl_phpdir: %{expand: %%global pecl_phpdir  %(%{__pecl} config-get php_dir  2> /dev/null || echo undefined)}}
%{?!pecl_xmldir: %{expand: %%global pecl_xmldir %{pecl_phpdir}/.pkgxml}}

%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

%global php_base php70t
%global pecl_name amqp
%global real_name amqp

Summary: Communicate with any AMQP compliant server
Name: %{php_base}-pecl-amqp
Version: 1.7.0alpha1
Epoch: 1
Release: 1.vortex%{?dist}
License: PHP
Group: Development/Languages
Vendor: Vortex RPM
URL: http://pecl.php.net/package/%{pecl_name}

Source: http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{php_base}-devel, %{php_base}-cli, %{php_base}-pear, librabbitmq041-devel
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires: librabbitmq041

%if %{?php_zend_api}0
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
%else
Requires: %{php_base}-api = %{php_apiver}
%endif

%description
This extension can communicate with any AMQP spec 0-9-1 compatible
server, such as RabbitMQ, OpenAMQP and Qpid, giving you the ability
to create and delete exchanges and queues, as well as publish to any
exchange and consume from any queue.


%prep
%setup -c -n %{real_name}-%{version} -q


%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

EOF

# Install XML package description
# use 'name' rather than 'pecl_name' to avoid conflict with pear extensions
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml


%clean
%{__rm} -rf %{buildroot}


%post
%{__pecl} install --nodeps --soft --force --register-only --nobuild %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]; then
%{__pecl} uninstall --nodeps --ignore-errors --register-only %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/CREDITS %{pecl_name}-%{version}/LICENSE
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{pecl_name}.xml


%changelog
* Fri Dec 18 2015 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.7.0alpha1-1.vortex
- Update to 1.7.0alpha1.

* Sat Dec 12 2015 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.6.1-1.vortex
- Update to 1.6.1.

* Fri Oct  3 2014 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.4.0-3.vortex
- Bump the epoch.

* Fri Oct  3 2014 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.4.0-2.vortex
- Update to 1.4.0.

* Fri Apr  4 2014 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.4.0beta1-1.vortex
- Rebuilt with php55t.

* Mon Feb  3 2014 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.4.0beta1-1.vortex
- Update to 1.4.0beta1.

* Wed Jan 29 2014 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.2.0-1.vortex
- Initial packaging.

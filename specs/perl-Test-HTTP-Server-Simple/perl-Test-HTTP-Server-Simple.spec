# $Id$
# Authority: shuff
# Upstream: David Glasser <glasser$bestpractical,com>

%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define real_name Test-HTTP-Server-Simple

Summary: Test::More functions for HTTP::Server::Simple
Name: perl-%{real_name}
Version: 0.11
Release: 1
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Test-HTTP-Server-Simple/

Source: http://search.cpan.org/CPAN/authors/id/A/AL/ALEXMV/Test-HTTP-Server-Simple-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(HTTP::Server::Simple)
BuildRequires: perl(NEXT)
BuildRequires: perl(Test::Builder)
#BuildRequires: perl(Test::Builder::Tester) >= 1.04
BuildRequires: perl(Test::Builder::Tester)
BuildRequires: perl(Test::More)
Requires: perl(HTTP::Server::Simple)
Requires: perl(NEXT)
Requires: perl(Test::Builder)
#Requires: perl(Test::Builder::Tester) >= 1.04
Requires: perl(Test::Builder::Tester)
Requires: perl(Test::More)

%filter_from_requires /^perl*/d
%filter_setup


%description
This mixin class provides methods to test an HTTP::Server::Simple-based web
server. Currently, it provides only one such method: started_ok.


%prep
%setup -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install

### Clean up buildroot
find %{buildroot} -name .packlist -exec %{__rm} {} \;

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc README
%doc %{_mandir}/man3/*
%dir %{perl_vendorlib}/Test/
%{perl_vendorlib}/Test/HTTP/Server/Simple.pm

%changelog
* Wed Dec  9 2009 Christoph Maser <cmr@financial.com> - 0.11-1
- Updated to version 0.11.

* Sat Oct 03 2009 Steve Huff <shuff@vecna.org> - 0.07-1
- Initial package.

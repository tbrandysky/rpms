# $Id$
# Authority: dag
# Upstream: news://comp.mail.pine/

%{?dist: %{expand %%define %dist 1}}

%define pgpver		0.18.0
#%define with_gpgpine	1

%define krb5inc %(krb5-config --cflags | sed -e 's|-I||')
%define krb5lib %(krb5-config --prefix)/%{_lib}
%{?rh62:%define krb5inc %{_usr}/kerberos/include}
%{?rh62:%define krb5lib %{_usr}/kerberos/%{_lib}}

Summary: Commonly used, MIME compliant mail and news reader
Name: pine
Version: 4.58
Release: 1
License: Freely Distributable
Group: Applications/Internet
URL: http://www.washington.edu/pine/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source0: ftp://ftp.cac.washington.edu/pine/pine%{version}.tar.bz2
Source1: http://www.megaloman.com/~hany/_data/pinepgp/pinepgp-%{pgpver}.tar.gz
Source2: pine.conf
Source3: pine-spellcheck
Source5: flock.c
Source6: pine.conf.fixed

Patch0: pine-4.58-makefile.patch
Patch2: pine-4.04-noflock.patch
Patch3: pine-4.21-passwd.patch
Patch4: pine-4.21-fixhome.patch
Patch8: imap-4.7c2-flock.patch 
Patch9: pine-4.30-ldap.patch
Patch14: pine-4.55-bogus-lock-warning.patch

Patch21: pine-4.31-segfix.patch
Patch22: pine-4.40-lockfile-perm.patch
Patch32: imap-2000-time.patch

# Do not remove this patch without checking that bugs 23679 and 38399
# _remain_ fixed.  [sic: or face the wrath of angry kernel hackers  ;o) ]
Patch33: pine-4.33-whitespace.patch

# Change PINE sendmail options to attempt to stop sendmail from logging -bs
# errors
Patch34: pine-4.33-sendmail-options.patch

# Fix bug #60818
Patch36: pine-4.44-overflow.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: perl, ncurses-devel
BuildRequires: openssl-devel, openldap-devel, krb5-devel
%{!?rh62:BuildRequires: pam-devel}
%{?rh62:BuildRequires: pam}

Requires: krb5-libs, mailcap

%description
Pine is a very popular, easy to use, full-featured email user agent
that includes a simple text editor called pico. Pine supports MIME
extensions and can also be used to read news. Pine also supports IMAP,
mail, and MH style folders.

%prep
%setup -n %{name}%{version} -a 1

#%patch0 -p1 -b .makefile
%{__perl} -pi.makefile -e 's|(BASECFLAGS)="-g (.*)"|$1="$2 %{optflags}"|g' imap/src/osdep/unix/Makefile

%{__perl} -pi.redhat-dag -e '
		s|/tmp/.\\usr\\spool\\mail\\|/tmp/.\\var\\spool\\mail\\|g;
		s|/tmp/.&#92;usr&#92;spool&#92;mail&#92;|/tmp/.&#92;var&#92;spool&#92;mail&#92;|g;
	' doc/pine.1 pine/pine.hlp

%{__perl} -pi.redhat-dag -e '
		s|/usr/spool/mail|%{_localstatedir}/spool/mail|g;
		s|/usr/spool/news|/%{_localstatedir}/spool/news|g;
		s|/usr/mail/|%{_localstatedir}/mail/|g;
		s|/usr/local/lib/pine.info|%{_libdir}/pine.info|g;
		s|/usr/local/lib/|%{_sysconfdir}/|g;
		s|/usr/local/bin/|%{_bindir}/|g;
	' doc/pine.1 doc/*.txt doc/tech-notes/*.html pine/osdep/os-*.h pine/pine-use.c pine/init.c pine/pine.hlp

#{__perl} -pi.krb5-dag -e 's|GSSDIR=/usr/local|GSSDIR=/usr/kerberos|' imap/src/osdep/unix/Makefile.gss
%patch4 -p1 -b .fixhome

# imap flock patch
%patch8 -p0 -b .flock-patch
%{__cp} %{SOURCE5} imap/src/osdep/unix

%{__perl} -pi.passwd-dag -e 's|/bin/passwd|%{_bindir}/passwd|;' pine/osdep/os-lnx.h
%patch9 -p1 -b .ldap-patch
%patch14 -p0 -b .bogus-lock-warning

%patch21 -p1 -b .segfix
%patch22 -p0 -b .lockfile-perm

%patch32 -p1 -b .time-h
%patch33 -p1 -b .whitespace-fix
# This patch does evil things
#%patch34 -p0 -b .sendmail-options
%patch36 -p1 -b .overflow

# this wants /usr/local/bin/perl
#d#chmod 644 contrib/utils/pwd2pine
%{__perl} -pi -e 's|^#!/.*bin/perl|#!%{__perl}|i' contrib/utils/pwd2pine

%{__rm} -rf krb5 ldap
mkdir krb5 ldap
%{__ln_s} -f %{krb5inc} krb5/include
%{__ln_s} -f %{krb5lib} krb5/lib
%{__ln_s} -f %{_includedir} ldap/include
%{__ln_s} -f %{_libdir} ldap/libraries
./contrib/krb5-setup lnp lnp || :
./contrib/ldap-setup lnp lnp || :

find -name "*.orig" -or -name "*~" | xargs %{__rm} -f core

%build
./build \
	OPTIMIZE="%{optflags}" \
	EXTRACFLAGS="-DIGNORE_LOCK_EACCES_ERRORS" \
	EXTRAAUTHENTICATORS="gss" \
	SPECIALAUTHENTICATORS="ssl" \
	SSLTYPE="unix" \
	SSLDIR="%{_prefix}" \
	SSLCERTS="%{_datadir}/ssl" \
	SSLINCLUDE="%{_includedir}/openssl" \
	SSLLIB="-lssl -lcrypto" \
	DEBUG="" \
	lrh

cd pinepgp-%{pgpver}
%configure \
	--with-gpg="%{_bindir}/gpg"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_libdir}

%{__make} -C pinepgp-%{pgpver} install-pinegpg \
	DESTDIR="%{buildroot}"

%{__install} -D -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pine.conf
%{__install} -D -m0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/pine.conf.fixed

%{__install} -d -m0755 %{buildroot}%{_bindir} \
			%{buildroot}%{_mandir}/man1/
%{__install} -m0755 bin/{mailutil,pine,pico,pilot,rpdump,rpload} %{buildroot}%{_bindir}
%{__install} -m0755 %{SOURCE3} %{buildroot}%{_bindir}
%{__install} -m0644 doc/*.1 imap/src/mailutil/mailutil.1 %{buildroot}%{_mandir}/man1/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc CPYRIGHT README doc/*.txt doc/pine-ports doc/tech-notes/*.html
%doc doc/mailcap.unx imap/docs/bugs.txt
%doc %{_mandir}/man?/*
%config %{_sysconfdir}/pine.conf*
%{_bindir}/*

%changelog
* Thu Apr 15 2004 Dag Wieers <dag@wieers.com> - 4.58-1
- Added mailutil. (James A Hunsaker)

* Sun Dec 21 2003 Dag Wieers <dag@wieers.com> - 4.58-0
- Initial package. (using DAR)

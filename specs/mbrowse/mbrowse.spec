# $Id$
# Authority: dag
# Upstream: Aaron Hodgen <ahodgen@munsterman.com>

# Screenshot: http://www.kill-9.org/mbrowse/screenshot/tree.png
# ScreenshotURL: http://www.kill-9.org/mbrowse/#Screenshots

%{?dist: %{expand %%define %dist 1}}

%define dfi %(which desktop-file-install &>/dev/null; echo $?)

Summary: GUI SNMP MIB browser
Name: mbrowse
Version: 0.3.1
Release: 0
License: GPL
Group: Applications/Internet
URL: http://www.kill-9.org/mbrowse/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://www.kill-9.org/mbrowse/mbrowse-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


BuildRequires: gtk+-devel >= 1.2
%{?fc1:BuildRequires: net-snmp-devel >= 4.2}
%{?el3:BuildRequires: net-snmp-devel >= 4.2}
%{?rh9:BuildRequires: net-snmp-devel >= 4.2}
%{?rh8:BuildRequires: net-snmp-devel >= 4.2}
%{?rh7:BuildRequires: ucd-snmp-devel}
%{?el2:BuildRequires: ucd-snmp-devel}
%{?rh6:BuildRequires: ucd-snmp-devel}

%description
Mbrowse is an SNMP MIB browser based on GTK and net-snmp.

%prep
%setup

%{__cat} <<EOF >%{name}.desktop
[Desktop Entry]
Name=MIB Browser
Comment=%{summary}
Icon=gnome-internet.png
Exec=mbrowse
Terminal=false
Type=Application
Categories=GNOME;Application;Internet;
EOF

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

%if %{dfi}
	%{__install} -d -m0755 %{buildroot}%{_datadir}/gnome/apps/Internet/
	%{__install} -m0644 %{name}.desktop %{buildroot}%{_datadir}/gnome/apps/Internet/
%else
	%{__install} -d -m0755 %{buildroot}%{_datadir}/applications/
	desktop-file-install --vendor gnome                \
		--add-category X-Red-Hat-Base              \
		--dir %{buildroot}%{_datadir}/applications \
		%{name}.desktop
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/*
%if %{dfi}
        %{_datadir}/gnome/apps/Internet/*.desktop
%else
        %{_datadir}/applications/*.desktop
%endif

%changelog
* Mon Mar 10 2003 Dag Wieers <dag@wieers.com> - 0.3.1-0
- Initial package. (using DAR)

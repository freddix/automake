%bcond_without	regeneration
%bcond_without	tests

%include	/usr/lib/rpm/macros.perl

%if %{without regeneration}
%unglobal	with_tests
%endif

Summary:	GNU automake - Makefile configuration tools
Name:		automake
Version:	1.14.1
Release:	1
Epoch:		1
License:	GPL v2+
Group:		Development/Building
Source0:	http://ftp.gnu.org/gnu/automake/%{name}-%{version}.tar.xz
# Source0-md5:	7fc29854c520f56b07aa232a0f880292
Patch0:		%{name}-no_versioned_dir.patch
URL:		http://sources.redhat.com/automake/
%if %{with regeneration}
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.13.0
%endif
BuildRequires:	rpm-perlprov
BuildRequires:	texinfo
Requires:	filesystem
Requires:	perl(File::Glob)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_aclocaldir	%{_datadir}/aclocal

%description
Automake is an experimental Makefile generator. Automake was inspired
by the 4.4BSD make and include files, but aims to be portable and to
conform to the GNU standards for Makefile variables and targets.

%prep
%setup -q
%patch0 -p1

%if %{with regeneration}
# prepare temporary copy of m4 dir without amversion.m4 (which causes automake version check)
mkdir m4-tmp
cd m4-tmp
ln -s ../m4/[!a]*.m4 ../m4/a[!m]*.m4 .
%endif

%build
%if %{with regeneration}
%{__aclocal} -I m4-tmp
%endif
%{__autoconf}
%if %{with regeneration}
%{__automake}
%endif
%configure \
	--host=%{_host} \
	--build=%{_host}
%{__make}

%if %{with tests}
%check
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgvdatadir=%{_datadir}/automake

rm -f $RPM_BUILD_ROOT%{_infodir}/dir*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/aclocal*
%attr(755,root,root) %{_bindir}/automake*
%{_infodir}/automake.info*
%{_infodir}/automake-history.info*
%{_mandir}/man1/aclocal*.1*
%{_mandir}/man1/automake*.1*

%{_datadir}/aclocal-*
%dir %{_datadir}/automake
%{_datadir}/automake/am
%{_datadir}/automake/Automake
%{_datadir}/automake/COPYING
%{_datadir}/automake/INSTALL
%{_datadir}/automake/texinfo.tex
%attr(755,root,root) %{_datadir}/automake/ar-lib
%attr(755,root,root) %{_datadir}/automake/compile
%attr(755,root,root) %{_datadir}/automake/config.guess
%attr(755,root,root) %{_datadir}/automake/config.sub
%attr(755,root,root) %{_datadir}/automake/depcomp
%attr(755,root,root) %{_datadir}/automake/install-sh
%attr(755,root,root) %{_datadir}/automake/mdate-sh
%attr(755,root,root) %{_datadir}/automake/missing
%attr(755,root,root) %{_datadir}/automake/mkinstalldirs
%attr(755,root,root) %{_datadir}/automake/py-compile
%attr(755,root,root) %{_datadir}/automake/tap-driver.pl
%attr(755,root,root) %{_datadir}/automake/tap-driver.sh
%attr(755,root,root) %{_datadir}/automake/test-driver
%attr(755,root,root) %{_datadir}/automake/ylwrap


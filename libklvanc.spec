#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library to parse/generate Vertical Ancillary Data
Summary(pl.UTF-8):	Biblioteka do analizy/generowania danych VANC
Name:		libklvanc
# from configure.ac /AC_INIT
Version:	1.0
%define	rel	1
%define	snap	20190806
%define	gitref	c38d31b428d0e02061f32c14562d172ec3bd9608
Release:	0.%{snap}.%{rel}
License:	LGPL v2.1
Group:		Libraries
Source0:	https://github.com/stoth68000/libklvanc/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	a870bc96decfe8951e5f5ec89e4b6a04
Patch0:		%{name}-sh.patch
URL:		https://github.com/stoth68000/libklvanc
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libtool >= 2:1.5
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libklvanc is a library which can be used for parsing/generation of
Vertical Ancillary Data (VANC) commonly found in the Serial Digital
Interface (SDI) wire protocol.

%description -l pl.UTF-8
Libklvanc to biblioteka służąca do analizy i generowania danych VANC
(Vertical Ancillary Data), używanych generalnbie w protokole Serial
Digital Interface (SDI).

%package devel
Summary:	Header files for libklvanc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libklvanc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libklvanc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libklvanc.

%package static
Summary:	Static libklvanc library
Summary(pl.UTF-8):	Statyczna biblioteka libklvanc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libklvanc library.

%description static -l pl.UTF-8
Statyczna biblioteka libklvanc.

%package apidocs
Summary:	API documentation for libklvanc library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libklvanc
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libklvanc library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libklvanc.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
# --disable-dep-curses: nothing actually uses it
%configure \
	--disable-dep-curses \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with apidocs}
cd doxygen
doxygen libklvanc.doxyconf
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libklvanc.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/klvanc_*
%attr(755,root,root) %{_libdir}/libklvanc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libklvanc.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libklvanc.so
%{_includedir}/libklvanc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libklvanc.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxygen/html/{search,*.css,*.html,*.js,*.png}
%endif

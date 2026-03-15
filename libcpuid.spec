#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	A small C library for x86 CPU detection and feature extraction
Summary(pl.UTF-8):	Mała biblioteka C do wykrywania CPU i jego możliwości dla procesorów x86
Name:		libcpuid
Version:	0.8.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/anrieff/libcpuid/releases
# TODO: prefer release tarballs
#Source0:	https://github.com/anrieff/libcpuid/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/anrieff/libcpuid/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	07547455373dcbcd707b6cf2738fb930
URL:		https://libcpuid.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libtool >= 2:2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small C library for x86 CPU detection and feature extraction.

%description -l pl.UTF-8
Mała biblioteka C do wykrywania CPU i jego możliwości dla procesorów
x86.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package tool
Summary:	Command line interface to libcpuid
Summary(pl.UTF-8):	Interfejs linii poleceń do libcpuid
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description tool
Command line interface to libcpuid.

%description tool -l pl.UTF-8
Interfejs linii poleceń do libcpuid.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -e '#"cpuid_tool" 3 #"cpuid_tool" 1 #' \
	libcpuid/docs/man/man3/cpuid_tool.3 > $RPM_BUILD_ROOT%{_mandir}/man1/cpuid_tool.1
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/cpuid_tool.3

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog Readme.md
%{_libdir}/libcpuid.so.*.*.*
%ghost %{_libdir}/libcpuid.so.17

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcpuid.so
%{_includedir}/libcpuid
%{_pkgconfigdir}/libcpuid.pc
%{_mandir}/man3/cpu_id_t.3*
%{_mandir}/man3/cpu_list_t.3*
%{_mandir}/man3/cpu_mark_t.3*
%{_mandir}/man3/cpu_raw_data_t.3*
%{_mandir}/man3/libcpuid.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcpuid.a
%endif

%files tool
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cpuid_tool
%{_mandir}/man1/cpuid_tool.1*

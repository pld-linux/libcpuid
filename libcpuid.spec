#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	A small C library for x86 CPU detection and feature extraction
#Summary(pl.UTF-8):
Name:		libcpuid
Version:	0.4.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/anrieff/libcpuid/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	42eefb90111945fe8ca71615b99195cb
URL:		http://libcpuid.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	intltool
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small C library for x86 CPU detection and feature extraction.

#%description -l pl.UTF-8

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
#Summary(pl.UTF-8):
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description tool
Command line interface to libcpuid.

#%description tool -l pl.UTF-8

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
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
%doc AUTHORS ChangeLog Readme.md
%attr(755,root,root) %{_libdir}/libcpuid.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcpuid.so.14

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcpuid.so
%{_includedir}/libcpuid
%{_pkgconfigdir}/libcpuid.pc
%{_mandir}/man3/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcpuid.a
%endif

%files tool
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cpuid_tool
%{_mandir}/man1/cpuid_tool.1*

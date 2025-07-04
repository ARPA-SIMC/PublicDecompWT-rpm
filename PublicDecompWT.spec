Name:           PublicDecompWT
Version:        2.8.1
Release:        4
Summary:        Wavelet decompression tool for xRIT files from MSG
License:        Apache 2.0
URL:            https://gitlab.eumetsat.int/open-source/PublicDecompWT
Source:         https://gitlab.eumetsat.int/open-source/PublicDecompWT/-/archive/%{version}/%{name}-%{version}.tar.gz
# Include ctime in header file DISE/UTCTime.h
# https://github.com/ARPA-SIMC/PublicDecompWT-rpm/issues/2
Patch0:         https://raw.githubusercontent.com/ARPA-SIMC/PublicDecompWT-rpm/v%{version}-%{release}/include-time-header.patch
BuildRequires:  binutils
BuildRequires:  gcc-c++

%description
Wavelet decompression tool for xRIT files from MSG
(xRITDecompress)

%package  -n %{name}-devel
Summary:  PublicDecompWT development library
Provides: %{name}-static = %{version}-%{release}

%description -n %{name}-devel
Wavelet decompression tool for xRIT files from MSG
(headers and libs)

%global debug_package %{nil}

%prep
%setup

# patching syntax changed
%if 0%{?rhel}
%patch0
%else
%patch 0
%endif

%build
cd COMP
BITS="glibc -fPIC" make
cd ../DISE
BITS="glibc -fPIC" make
cd ../xRITDecompress
make all

%install

# Headers
mkdir -p %{buildroot}/%{_includedir}/%{name}
for i in 'COMP' 'COMP/JPEG' 'COMP/T4' 'COMP/WT'; do
  install -m0644 %{_builddir}/%{name}-%{version}/${i}/Inc/*.h %{buildroot}/%{_includedir}/%{name}/
done
install -m0644 %{_builddir}/%{name}-%{version}/DISE/*.h %{buildroot}/%{_includedir}/%{name}/

# Libs
for i in JPEG T4 WT ; do
  install -D -m0644 %{_builddir}/%{name}-%{version}/COMP/${i}/Src/lib${i}.a %{buildroot}/%{_libdir}/%{name}/lib${i}.a
done
install -D -m0644 %{_builddir}/%{name}-%{version}/COMP/Src/libCOMP.a %{buildroot}/%{_libdir}/%{name}/libCOMP.a
install -D -m0644 %{_builddir}/%{name}-%{version}/DISE/libDISE.a %{buildroot}/%{_libdir}/%{name}/libDISE.a

# Bin
install -D -m0755 %{_builddir}/%{name}-%{version}/xRITDecompress/xRITDecompress %{buildroot}/%{_bindir}/xRITDecompress

mkdir %{buildroot}/%{_libdir}/pkgconfig/
cat > %{buildroot}/%{_libdir}/pkgconfig/libpublicdecompwt.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: libpublicdecompwt
Description: Wavelet decompression library for xRIT files from MeteoSat Second Generation
Version: %{version}

Cflags: -I\${includedir}/PublicDecompWT
Libs: -L\${libdir}/PublicDecompWT/ -lCOMP -lDISE -lJPEG -lT4 -lWT

EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/xRITDecompress

%files -n %{name}-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}/*.a
%{_libdir}/pkgconfig/libpublicdecompwt.pc

%changelog
* Mon Jun 16 2025 Daniele Branchini <dbranchini@arpae.it> - 2.8.1-4
- distro dependant patch syntax

* Wed May 28 2025 Daniele Branchini <dbranchini@arpae.it> - 2.8.1-3
- updated patch syntax

* Wed Jun  6 2023 Emanuele Di Giacomo <edigiacomo@arpae.it> - 2.8.1-2
- Patch for DISE/UTCTime.h (#2)

* Thu Jun  1 2023 Daniele Branchini <dbranchini@arpae.it> - 2.8.1-1
- Upstream update

* Mon Jun  8 2020 Daniele Branchini <dbranchini@arpae.it> - 2.7.2-5
- Fixed permission in xRITDecompress binary

* Fri May 29 2020 Daniele Branchini <dbranchini@arpae.it> - 2.7.2-4
- Added DISE lib compilation, fixed fPIC option

* Fri May 29 2020 Daniele Branchini <dbranchini@arpae.it> - 2.7.2-3
- Added fPIC option, fixed pkgconfig file (#1)

* Fri May 29 2020 Daniele Branchini <dbranchini@arpae.it> - 2.7.2-2
- Added pkgconfig file (#1)

* Thu Apr 30 2020 Daniele Branchini <dbranchini@arpae.it> - 2.7.2-1
- First build

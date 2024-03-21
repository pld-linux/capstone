#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Capstone engine - dissassembly framework
Summary(pl.UTF-8):	Silnik Capstone - szkielet do disasemblacji
Name:		capstone
Version:	5.0.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/aquynh/capstone/releases
Source0:	https://github.com/aquynh/capstone/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2f813b8bedd40be5fd7327d51fc101dc
URL:		http://www.capstone-engine.org/
BuildRequires:	cmake >= 3.15
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Capstone is a disassembly framework with the target of becoming the
ultimate disasm engine for binary analysis and reversing in the
security community. Capstone offers some unparalleled features:
- Support for multiple hardware architectures: ARM, ARM64 (ARMv8),
  Ethereum VM, M68K, MIPS, PPC, SPARC, SystemZ, TMS320C64X, M680X,
  XCore and X86 (including X86_64).
- Having clean/simple/lightweight/intuitive architecture-neutral API.
- Provide details on disassembled instruction ("decomposer").
- Provide semantics of the disassembled instruction, such as list of
  implicit registers read & written.
- Implemented in pure C language, with lightweight bindings for many
  languages.
- Native support for all popular platforms: Windows, MacOS X, iOS,
  Android, Linux, *BSD, Solaris, etc.
- Thread-safe by design.
- Special support for embedding into firmware or OS kernel.
- High performance & suitable for malware analysis (capable of
  handling various X86 malware tricks).
- Distributed under the open source BSD license.

%description -l pl.UTF-8
Capstone to szkielet do disasemblacji o aspiracjach do stania się
standardowym silnikiem disasemblującym do analizy binariów i
inżynierii wstecznej wśród społeczności związanej z bezpieczeństwem.
Oferuje trochę niespotykanych możliwości:
- obsługę wielu architektur sprzętowych: ARM, ARM64 (ARMv8), Ethereum
  VM, M68K, MIPS, PPC, SPARC, SystemZ, TMS320C64X, M680X, XCore oraz
  X86 (w tym X86_64)
- czyste/proste/lekkie/intuicyjne API niezależne od architektury
- podaje szczegóły disasemblowanej instrukcji ("dekompozycję")
- podaje semantykę disasemblowanej instrukcji - np. listę niejawnych
  odczytywanych i zapisywanych rejestrów
- jest zaimplementowany w czystym C z lekkimi wiązaniami do wielu
  innych języków
- natywną obsługę wielu popularnych platform: Windows, MacOS X, iOS,
  Android, Linux, *BSD, Solaris itp.
- jest bezpieczny pod kątem wątków
- specjalną obsługę osadzania w firmwarze lub jądrze systemu
- wysoką wydajność, przydatność przy analizie podejrzanego
  oprogramowania (obsługę różnych sztuczek architektury X86)
- jest udostępniony z otwartymi źródłami na licencji BSD.

%package devel
Summary:	Header files for Capstone dissassembler library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki disasemblera Capstone
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Capstone dissassembler library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki disasemblera Capstone.

%package static
Summary:	Static Capstone dissassembler library
Summary(pl.UTF-8):	Biblioteka statyczna disasemblera Capstone
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Capstone dissassembler library.

%description static -l pl.UTF-8
Biblioteka statyczna disasemblera Capstone.

%prep
%setup -q

%build
%if %{with static_libs}
%cmake -B build-static \
	-DBUILD_SHARED_LIBS=OFF \
	-DCAPSTONE_BUILD_CSTOOL=OFF

%{__make} -C build-static
%endif

%cmake -B build

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS.TXT ChangeLog LICENSE.TXT LICENSE_LLVM.TXT README.md SPONSORS.TXT
%attr(755,root,root) %{_bindir}/cstool
%attr(755,root,root) %{_libdir}/libcapstone.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libcapstone.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcapstone.so
%{_includedir}/capstone
%{_libdir}/cmake/capstone
%{_pkgconfigdir}/capstone.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcapstone.a
%endif

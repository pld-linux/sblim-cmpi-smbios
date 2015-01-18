# TODO: register .mof files?
Summary:	SBLIM CMPI SMBIOS instrumentation
Summary(pl.UTF-8):	Przyrządy pomiarowe SMBIOS dla SBLIM CMPI
Name:		sblim-cmpi-smbios
Version:	0.3.2
Release:	0.1
License:	CPL v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.gz
# Source0-md5:	9eaf50b70de769faa700229af3e2ca33
Patch0:		%{name}-update.patch
URL:		http://sblim.sourceforge.net/
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
BuildRequires:	sed >= 4.0
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
Requires:	sblim-sfcb-schema >= 2.7
ExclusiveArch:	%{ix86} %{x8664} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI SMBIOS instrumentation allows to get BIOS inventory
information about a system remotely via a CIMOM.

%description -l pl.UTF-8
Dostawcy informacji SMBIOS dla SBLIM CMPI pozwalają na uzyskiwanie
informacji o systemie z inwentarza BIOS zdalnie poprzez CIMOM.

%prep
%setup -q
%patch0 -p1

#%{__sed} -i -e 's/^PEGASUS=1/#&/' setting.cmpi

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -g -DCMPI_VERSION=90" \
	COMMONLIB=%{_libdir} \
	PEGASUS= \
	STANDALONE=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/cmpi,%{_datadir}/%{name}}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	CIMOMLIB=$RPM_BUILD_ROOT%{_libdir}/cmpi \
	CIMOMMOF=$RPM_BUILD_ROOT%{_datadir}/%{name} \
	COMMONLIB=$RPM_BUILD_ROOT%{_libdir} \
	PEGASUS= \
	STANDALONE=1

# modules
#%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README license.html
%attr(755,root,root) %{_libdir}/libdmiinfo.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiLinux_BIOSElement.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiLinux_BIOSFeature.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiLinux_BIOSFeatureBIOSElements.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiLinux_BIOSProduct.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiLinux_BIOSProductBIOSFeatures.so
%dir %{_datadir}/sblim-cmpi-smbios
%{_datadir}/sblim-cmpi-smbios/Linux_BIOS.mof
%{_datadir}/sblim-cmpi-smbios/Linux_BIOSRegistration.mof

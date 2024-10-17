%define svn		r843
%define major		0
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d
%define staticdevelname	%mklibname %{name} -d -s
%define debug_package          %{nil}

Name:		       	aften
Summary:    		An A/52 audio encoder
Version:    		0.0.8
Release:    		1
License:    		GPLv2+ and LGPLv2+ and BSD
Group:      		Sound
Source:     		http://downloads.sourceforge.net/aften/aften-%{version}.tar.bz2
URL:        		https://aften.sourceforge.net/
BuildRequires:		cmake
BuildRequires:		ninja
Requires:		%{libname} = %{version}-%{release}
BuildRoot:  		%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Aften is an audio encoder which generates compressed audio streams based on 
ATSC A/52 specification. This type of audio is also known as AC-3 or Dolby
Digital and is one of the audio codecs used in DVD-Video content. 

%package -n            %{libname}
Summary:               Library for %{name}
Group:                 System/Libraries

%description -n                %{libname}
This package provides the library for %{name}.

%package -n            %{develname}
Summary:               Development files for %{name}
Group:                 Development/Other
Requires:              %{name} = %{version}-%{release}
Provides:              %{name}-devel = %{version}-%{release}

%description -n        %{develname}
This package contains development files for %{name}.

%package -n            %{staticdevelname}
Summary:               Static development files for %{name}
Group:                 Development/Other
Requires:              %{develname} = %{version}-%{release}
Provides:              %{name}-static-devel = %{version}-%{release}

%description -n                %{staticdevelname}
This package contains static development files for %{name}.

%prep
%autosetup -p1
%if "%_lib" != "lib"
sed -i -e 's,DESTINATION lib,DESTINATION %{_lib},g' CMakeLists.txt
%endif

%cmake -G Ninja \
	-DSHARED:BOOL=ON

%build
%ninja_build -C build

%install
%ninja_install -C build

# install static devel files
cp -Pp build/*.a %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README Changelog
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*

%files -n %{staticdevelname}
%defattr(-,root,root)
%{_libdir}/*.a

#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg tqtinterface

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libtqt4 %{_lib}tqt4
%else
%define libtqt4 libtqt4
%endif

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	4.2.0
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	The Trinity Qt Interface Libraries
Group:		System/GUI/Other
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make

BuildRequires:	libtqt3-mt-devel >= 3.5.0
BuildRequires:	tqt3-dev-tools >= 3.5.0
BuildRequires:	trinity-tde-cmake >= %{tde_version}

%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig

# UUID support
BuildRequires:  pkgconfig(uuid)

# PTHREAD support
BuildRequires: npth-devel

# MESA support
BuildRequires: pkgconfig(opengl)

# X11 libraries
BuildRequires: pkgconfig(x11)

# GLU support
BuildRequires: pkgconfig(glu)

%description
The Trinity Qt Interface is a library that abstracts Qt from Trinity.
This allows the Trinity code to rapidly port from one version of Qt to another.
This is primarily accomplished by defining old functions in terms of new functions,
although some code has been added for useful functions that are no longer part of Qt.


##########

%package -n %{libtqt4}
Group:		System/GUI/Other
Summary:	The Trinity Qt Interface Libraries
Provides:	libtqt4 = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:	libtqt3-mt >= 3.5.0

Obsoletes:	trinity-tqtinterface < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-tqtinterface = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libtqt4}
The Trinity Qt Interface is a library that abstracts Qt from Trinity.
This allows the Trinity code to rapidly port from one version of Qt to another.
This is primarily accomplished by defining old functions in terms of new functions,
although some code has been added for useful functions that are no longer part of Qt.

%files -n %{libtqt4}
%defattr(-,root,root,-)
%{_libdir}/libtqt.so.4
%{_libdir}/libtqt.so.4.2.0

%post -n %{libtqt4}
/sbin/ldconfig || :

%postun -n %{libtqt4}
/sbin/ldconfig || :

##########

%package -n %{libtqt4}-devel
Group:		Development/Libraries/X11
Summary:	The Trinity Qt Interface Libraries (Development Files)
Provides:	libtqt4-devel = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:	%{libtqt4} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	libtqt3-mt-devel >= 3.5.0
Requires:	tqt3-dev-tools >= 3.5.0
Requires:	trinity-tde-cmake >= %{version}-%{release}

Obsoletes:	trinity-tqtinterface-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-tqtinterface-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libtqt4}-devel
The Trinity Qt Interface is a library that abstracts Qt from Trinity.
This allows the Trinity code to rapidly port from one version of Qt to another.
This is primarily accomplished by defining old functions in terms of new functions,
although some code has been added for useful functions that are no longer part of Qt.

%post -n %{libtqt4}-devel
/sbin/ldconfig || :

%postun -n %{libtqt4}-devel
/sbin/ldconfig || :

%files -n %{libtqt4}-devel
%defattr(-,root,root,-)
%{_bindir}/convert_qt_tqt1
%{_bindir}/convert_qt_tqt2
%{_bindir}/convert_qt_tqt3
%{_bindir}/dcopidl-tqt
%{_bindir}/dcopidl2cpp-tqt
%{_bindir}/dcopidlng-tqt
%{_bindir}/mcopidl-tqt
%{_bindir}/moc-tqt
%{_bindir}/tmoc
%{_bindir}/tqt-replace
%{_bindir}/uic-tqt
%{_includedir}/tqt/
%{_libdir}/libtqt.la
%{_libdir}/libtqt.so
%{_libdir}/pkgconfig/tqt.pc
%{_libdir}/pkgconfig/tqtqui.pc

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DQTDIR="%{_datadir}/tqt3" \
  -DQT_INCLUDE_DIR="%{_includedir}/tqt3" \
  -DQT_LIBRARY_DIR="%{_libdir}" \
  \
  -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
  -DPKGCONFIG_INSTALL_DIR="%{_libdir}/pkgconfig" \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/tqt \
  -DLIB_INSTALL_DIR=%{_libdir} \
  -DBIN_INSTALL_DIR=%{_bindir} \
  \
  -DCMAKE_LIBRARY_PATH="%{_libdir}" \
  -DCMAKE_INCLUDE_PATH="%{_includedir}" \
  \
  -DWITH_QT3="ON" \
  -DBUILD_ALL="ON" \
  -DUSE_QT3="ON" \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__make install DESTDIR="%{?buildroot}" -C build


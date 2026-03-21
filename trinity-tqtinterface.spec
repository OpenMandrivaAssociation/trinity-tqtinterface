%bcond clang 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg tqtinterface

%define libname %mklibname tqt4
%define devname %mklibname tqt4 -d

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Version:	4.2.0
Release:	%{?tde_version:%{tde_version}_}4
Summary:	The Trinity Qt Interface Libraries
Group:		System/GUI/Other
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DQTDIR="%{_datadir}/tqt3"
BuildOption:    -DQT_INCLUDE_DIR="%{_includedir}/tqt3"
BuildOption:    -DQT_LIBRARY_DIR="%{_libdir}"
BuildOption:    -DINCLUDE_INSTALL_DIR=%{_includedir}/tqt
BuildOption:    -DWITH_QT3="ON"
BuildOption:    -DBUILD_ALL="ON"
BuildOption:    -DUSE_QT3="ON"

BuildRequires:	pkgconfig(tqt-mt)
BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires:  tqt3-dev-tools

%{!?with_clang:BuildRequires:	gcc-c++}
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

%package -n %{libname}
Group:		System/GUI/Other
Summary:	The Trinity Qt Interface Libraries

%description -n %{libname}
The Trinity Qt Interface is a library that abstracts Qt from Trinity.
This allows the Trinity code to rapidly port from one version of Qt to another.
This is primarily accomplished by defining old functions in terms of new functions,
although some code has been added for useful functions that are no longer part of Qt.

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libtqt.so.4
%{_libdir}/libtqt.so.4.2.0

##########

%package -n %{devname}
Group:		Development/Libraries/X11
Summary:	The Trinity Qt Interface Libraries (Development Files)

Requires:	%{libname} = %{EVRD}

%description -n %{devname}
The Trinity Qt Interface is a library that abstracts Qt from Trinity.
This allows the Trinity code to rapidly port from one version of Qt to another.
This is primarily accomplished by defining old functions in terms of new functions,
although some code has been added for useful functions that are no longer part of Qt.

%files -n %{devname}
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


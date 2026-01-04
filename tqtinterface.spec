%bcond clang 1

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg tqtinterface
%define pkg_rel 3

%define libtqt4 %{_lib}tqt4

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	4.2.0
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	The Trinity Qt Interface Libraries
Group:		System/GUI/Other
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DQTDIR="%{_datadir}/tqt3"
BuildOption:    -DQT_INCLUDE_DIR="%{_includedir}/tqt3"
BuildOption:    -DQT_LIBRARY_DIR="%{_libdir}"
BuildOption:    -DINCLUDE_INSTALL_DIR=%{_includedir}/tqt
BuildOption:    -DWITH_QT3="ON"
BuildOption:    -DBUILD_ALL="ON"
BuildOption:    -DUSE_QT3="ON"

BuildRequires:	libtqt3-mt-devel >= 3.5.0
BuildRequires:	tqt3-dev-tools >= 3.5.0
BuildRequires:	trinity-tde-cmake >= %{tde_version}

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


%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

# Environment setup:
#
#	mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
#	echo | bzip2 -c > ~/rpmbuild/SOURCES/sugar-toolkit-gtk3.tar.bz2
#	cd ~/build/ && git clone git://git.sugarlabs.org/dextrose/sugar.git
#	ln -s ~/build/sugar/dextrose/sugar-toolkit-gtk3.spec \
#	      ~/rpmbuild/SPECS/sugar-tookit-gtk3.spec
#	rpmbuild -ba ~/rpmbuild/SPECS/sugar-toolkit-gtk3.spec
#

%define git_repo sugar-toolkit-gtk3
%define git_head devel

%define git_repodir %(echo ~/build/)
%define git_gitdir %{git_repodir}/%{git_repo}/.git

%define git_get_source pushd %{git_repodir}/%{git_repo} ;\
	/usr/bin/git pull ;\
        /usr/bin/git log > CHANGES ;\
        /usr/bin/git add CHANGES ;\
        /usr/bin/git commit -m "Updated CHANGES file" ;\
        /usr/bin/git archive --format=tar --prefix=%{name}-%{version}/ %{git_head} | \
                bzip2 -c > %{_sourcedir}/%{name}-%{version}.tar.bz2 ;\
        popd

%define git_clone_source if [ -d %{name}-%{version} ] ; then \
                cd %{name}-%{version} && git pull origin %{git_head} ; \
        else \
                git clone %{git_gitdir} %{name}-%{version} && \
                cd %{name}-%{version}/ ; \
        fi

%define git_submodule git submodule
%define git_prep_submodules %{git_submodule} init --cloned && %{git_submodule} update

%define git_version %(git --git-dir=%{git_gitdir} describe --tags 2> /dev/null || echo 0.0-`git --git-dir=%{git_gitdir} log --oneline | wc -l`-g`git --git-dir=%{git_gitdir} describe --always`)

# if the git repo has tags
%define git_get_ver %(echo %{git_version} | sed 's/^v\\?\\(.*\\)-\\([0-9]\\+\\)-g.*$/\\1/;s/-//')
%define git_get_rel %(echo %{git_version} | sed 's/^v\\?\\(.*\\)-\\([0-9]\\+-g.*\\)$/\\2/;s/-/_/')



Summary: Sugar toolkit GTK+ 3
Name: sugar-toolkit-gtk3
Epoch: 1
Version: %git_get_ver
Release: %git_get_rel
URL: http://wiki.laptop.org/go/Sugar
Source0: http://download.sugarlabs.org/sources/sucrose/glucose/%{name}/%{name}-%{version}.tar.bz2
#Source1: macros.sugar-toolkit-gtk3
License: LGPLv2+
Group: System Environment/Libraries

BuildRequires: alsa-lib-devel
BuildRequires: gettext-devel
BuildRequires: gtk3-devel
BuildRequires: gobject-introspection-devel
BuildRequires: intltool
BuildRequires: librsvg2-devel
BuildRequires: libSM-devel
BuildRequires: perl-XML-Parser
BuildRequires: pkgconfig
BuildRequires: python-devel
BuildRequires: pygtk2-codegen
BuildRequires: pygobject2-devel

Requires: dbus-python
Requires: gettext
Requires: pygobject3
Requires: python-simplejson
Requires: python-dateutil
Requires: sugar-datastore
Requires: unzip

%description
Sugar is the core of the OLPC Human Interface. The toolkit provides
a set of widgets to build HIG compliant applications and interfaces
to interact with system services like presence and the datastore.
This is the toolkit depending on GTK3.

%package devel
Summary: Invokation information for accessing SugarExt-1.0
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the invocation information for accessing
the SugarExt-1.0 library through gobject-introspection.

%prep
%git_get_source

%setup -q

%build
sh autogen.sh
autoreconf -i
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/rpm/
install -p %{_builddir}/%{name}-%{version}/dextrose/macros.sugar-toolkit-gtk3 %{buildroot}/%{_sysconfdir}/rpm/macros.sugar-toolkit-gtk3

%find_lang %name

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README CHANGES
%{python_sitelib}/*
%{_sysconfdir}/rpm/macros.sugar-toolkit-gtk3
%{_libdir}/girepository-1.0/*.typelib
%{_libdir}/lib*.so.*
%{_bindir}/sugar-activity

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_datadir}/gir-1.0/*.gir

%changelog
* Tue Oct 16 2012 Daniel Drake <dsd@laptop.org> 0.97.7-1
- 0.97.7 devel release

* Thu Oct 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.97.6-1
- 0.97.6 devel release

* Fri Oct  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.97.5-1
- 0.97.5 devel release

* Wed Sep 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.97.4-1
- 0.97.4 devel release

* Thu Sep 20 2012 Daniel Drake <dsd@laptop.org> - 0.97.3-1
- New development release

* Thu Sep 13 2012 Daniel Drake <dsd@laptop.org> - 0.97.2-1
- New development release

* Tue Aug 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.97.1-1
- 0.97.1 devel release

* Wed Aug 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.97.0-1
- 0.97.0 devel release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.4-1
- 0.96.4 stable release

* Tue Jun  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.3-1
- 0.96.3 stable release

* Sat Jun  2 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.2-1
- 0.96.2 stable release

* Sun May 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.1-2
- Add gettext to Requires

* Sat May  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.1-1
- 0.96.1 stable release

* Tue Apr 24 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.0-1
- 0.96.0 stable release

* Thu Apr 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.95.6-1
- devel release 0.95.6

* Fri Mar 23 2012 Simon Schampijer <simon@laptop.org> - 0.95.5-1
- devel release 0.95.5

* Wed Mar 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.95.4-1
- devel release 0.95.4

* Mon Feb  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.95.3-1
- devel release 0.95.3

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.95.2-2
- Fix devel dependencies

* Thu Dec 22 2011 Simon Schampijer <simon@laptop.org> - 0.95.2-1
- devel release 0.95.2
- incorporated review comments

* Sun Dec 11 2011 Simon Schampijer <simon@laptop.org> - 0.95.1-1
- devel release 0.95.1

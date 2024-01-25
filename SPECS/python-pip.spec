%bcond_with bootstrap
%bcond_with tests

%bcond_without doc

%global srcname pip
%global python3_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%if %{without bootstrap}
%global python3_wheeldir %{_datadir}/python3-wheels
%endif

%global bashcompdir %(b=$(pkg-config --variable=completionsdir bash-completion 2>/dev/null); echo ${b:-%{_sysconfdir}/bash_completion.d})

Name:                 python-%{srcname}
# When updating, update the bundled libraries versions bellow!
Version:              9.0.3
Release:              22%{?dist}.openela.0
Summary:              A tool for installing and managing Python packages

Group:                Development/Libraries

# We bundle a lot of libraries with pip, which itself is under MIT license.
# Here is the list of the libraries with corresponding licenses:

# appdirs: MIT
# CacheControl: ASL 2.0
# certifi: MPLv2.0
# chardet: LGPLv2
# colorama: BSD
# distlib: Python
# distro: ASL 2.0
# html5lib: MIT
# idna: BSD
# ipaddress: Python
# lockfile: MIT
# packaging: ASL 2.0 or BSD
# progress: ISC
# pyparsing: MIT
# requests: ASL 2.0
# retrying: ASL 2.0
# urllib3: MIT
# six: MIT
# urllib3: MIT
# webencodings: BSD

License:              MIT and Python and ASL 2.0 and BSD and ISC and LGPLv2 and MPLv2.0 and (ASL 2.0 or BSD)
URL:                  http://www.pip-installer.org
Source0:              https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:            noarch

%if %{with tests}
BuildRequires:        git
BuildRequires:        bzr
%endif

# to get tests:
# git clone https://github.com/pypa/pip && cd pip
# git checkout 9.0.1 && tar -czvf ../pip-9.0.1-tests.tar.gz tests/
%if %{with tests}
Source1:              pip-%{version}-tests.tar.gz
%endif

# Patch until the following issue gets implemented upstream:
# https://github.com/pypa/pip/issues/1351
Patch0:               allow-stripping-given-prefix-from-wheel-RECORD-files.patch

# Downstream only patch
# Emit a warning to the user if pip install is run with root privileges
# Issue upstream: https://github.com/pypa/pip/issues/4288
Patch1:               emit-a-warning-when-running-with-root-privileges.patch

# Prevent removing of the system packages installed under /usr/lib
# when pip install -U is executed.
# https://bugzilla.redhat.com/show_bug.cgi?id=1626408
# Author: Michal Cyprian
Patch2:               remove-existing-dist-only-if-path-conflicts.patch

# Do not show the "new version of pip" warning outside of venv
# Upstream issue: https://github.com/pypa/pip/issues/5346
# Fedora bug: https://bugzilla.redhat.com/show_bug.cgi?id=1573755
Patch3:               pip-nowarn-upgrade.patch

# Use the system level root certificate instead of the one bundled in certifi
# https://bugzilla.redhat.com/show_bug.cgi?id=1655255
Patch4:               dummy-certifi.patch

# Patch for CVE in the bundled urllib3
# CVE-2018-20060 Cross-host redirect does not remove Authorization header allow for credential exposure
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2018-20060
Patch5:               CVE-2018-20060.patch

# Patch for CVE in the bundled urllib3
# CVE-2019-11236 CRLF injection due to not encoding the '\r\n' sequence leading to possible attack on internal service
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2019-11236
Patch6:               CVE-2019-11236.patch

# Patch for CVE in the bundled urllib3
# CVE-2019-11324 Certification mishandle when error should be thrown
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2019-11324
Patch7:               CVE-2019-11324.patch

# Patch for CVE in the bundled requests
# CVE-2018-18074 Redirect from HTTPS to HTTP does not remove Authorization header
# This patch fixes both the CVE
# https://bugzilla.redhat.com/show_bug.cgi?id=1643829
# and the subsequent regression
# https://github.com/psf/requests/pull/4851
Patch8:               CVE-2018-18074.patch

# Patch for pip install <url> allow directory traversal, leading to arbitrary file write
# - Upstream PR: https://github.com/pypa/pip/pull/6418/files
# - Bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=1868016
# Patch9 fixes the issue
# Patch10 adds unit tests for the issue
Patch9:               pip-directory-traversal-security-issue.patch
Patch10:              pip-directory-traversal-security-issue-tests.patch

# Patch for CVE-2021-3572 - pip incorrectly handled unicode separators in git references
# The patch is adjusted for older pip where it's necessary to also switch
# the way pip gets revisions from git
# Upstream PR: https://github.com/pypa/pip/pull/9827
# Bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=1962856
Patch11:              CVE-2021-3572.patch

# Downstream-only implementation of support of yanked releases
# PEP 592 - Adding "Yank" Support to the Simple API:
#   https://www.python.org/dev/peps/pep-0592/
# Bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=2000135
Patch12:              skip_yanked_releases.patch
Patch13:              5000-add-openela.patch

%global _description \
pip is a package management system used to install and manage software packages \
written in Python. Many packages can be found in the Python Package Index \
(PyPI). pip is a recursive acronym that can stand for either "Pip Installs \
Packages" or "Pip Installs Python".

%description %_description


%package -n platform-python-%{srcname}
Summary:              A tool for installing and managing Python3 packages
Group:                Development/Libraries
Conflicts:            python%{python3_pkgversion}-pip < 9.0.3-5%{?dist}
Obsoletes:            python%{python3_pkgversion}-pip < 9.0.3-6%{?dist}

BuildRequires:        python%{python3_pkgversion}-devel
BuildRequires:        python%{python3_pkgversion}-setuptools
BuildRequires:        bash-completion
%if %{with tests}
BuildRequires:        python%{python3_pkgversion}-mock
BuildRequires:        python%{python3_pkgversion}-pytest
BuildRequires:        python%{python3_pkgversion}-pretend
BuildRequires:        python%{python3_pkgversion}-freezegun
BuildRequires:        python%{python3_pkgversion}-pytest-capturelog
BuildRequires:        python%{python3_pkgversion}-scripttest
BuildRequires:        python%{python3_pkgversion}-virtualenv
%endif
%if %{without bootstrap}
BuildRequires:        python%{python3_pkgversion}-pip
BuildRequires:        python%{python3_pkgversion}-wheel
%endif
Requires:             platform-python-setuptools

BuildRequires:        ca-certificates
Requires:             ca-certificates

# Virtual provides for the packages bundled by pip.
# See the python2 list above for instructions.
Provides:             bundled(python3dist(appdirs)) = 1.4.0
Provides:             bundled(python3dist(cachecontrol)) = 0.11.7
Provides:             bundled(python3dist(colorama)) = 0.3.7
Provides:             bundled(python3dist(distlib)) = 0.2.4
Provides:             bundled(python3dist(distro)) = 1.0.1
Provides:             bundled(python3dist(html5lib)) = 1.0b10
Provides:             bundled(python3dist(ipaddress) = 1.0.17
Provides:             bundled(python3dist(lockfile)) = 0.12.2
Provides:             bundled(python3dist(packaging)) = 16.8
Provides:             bundled(python3dist(setuptools)) = 28.8.0
Provides:             bundled(python3dist(progress)) = 1.2
Provides:             bundled(python3dist(pyparsing)) = 2.1.10
Provides:             bundled(python3dist(requests)) = 2.11.1
Provides:             bundled(python3dist(retrying)) = 1.3.3
Provides:             bundled(python3dist(six)) = 1.10.0
Provides:             bundled(python3dist(webencodings)) = 0.5

# Bundled within the requests bundle
Provides:             bundled(python3dist(chardet)) = 2.3.0
Provides:             bundled(python3dist(urllib3)) = 1.16

%description -n platform-python-%{srcname} %_description


%package -n python%{python3_pkgversion}-%{srcname}
Summary:              A tool for installing and managing Python3 packages
Group:                Development/Libraries

Requires:             platform-python-pip = %{version}-%{release}
Requires:             python36
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname} %_description


%if %{with doc}
%package doc
Summary:              A documentation for a tool for installing and managing Python packages

BuildRequires:        python%{python3_pkgversion}-sphinx

%description doc
A documentation for a tool for installing and managing Python packages

%endif

%if %{without bootstrap}
%package -n python3-%{srcname}-wheel
Summary:              The pip wheel

# Virtual provides for the packages bundled by pip.
# You can find the versions in pip/_vendor/vendor.txt file.
Provides:             bundled(python3dist(appdirs)) = 1.4.0
Provides:             bundled(python3dist(cachecontrol)) = 0.11.7
Provides:             bundled(python3dist(colorama)) = 0.3.7
Provides:             bundled(python3dist(distlib)) = 0.2.4
Provides:             bundled(python3dist(distro)) = 1.0.1
Provides:             bundled(python3dist(html5lib)) = 1.0b10
Provides:             bundled(python3dist(ipaddress) = 1.0.17
Provides:             bundled(python3dist(lockfile)) = 0.12.2
Provides:             bundled(python3dist(packaging)) = 16.8
Provides:             bundled(python3dist(setuptools)) = 28.8.0
Provides:             bundled(python3dist(progress)) = 1.2
Provides:             bundled(python3dist(pyparsing)) = 2.1.10
Provides:             bundled(python3dist(requests)) = 2.11.1
Provides:             bundled(python3dist(retrying)) = 1.3.3
Provides:             bundled(python3dist(six)) = 1.10.0
Provides:             bundled(python3dist(webencodings)) = 0.5

# Bundled within the requests bundle
Provides:             bundled(python3dist(chardet)) = 2.3.0
Provides:             bundled(python3dist(urllib3)) = 1.16

%description -n python3-%{srcname}-wheel
A Python wheel of pip to use with venv.
%endif

%prep
%setup -q -n %{srcname}-%{version}

%if %{with tests}
tar -xf %{SOURCE1}
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# Patching of bundled libraries
pushd pip/_vendor/urllib3
%patch5 -p1
%patch6 -p1
%patch7 -p1
popd
pushd pip/_vendor/requests
%patch8 -p1
popd
%patch9 -p1
%if %{with tests}
%patch10 -p1
%endif
%patch11 -p1
%patch12 -p1

# this goes together with patch4
rm pip/_vendor/certifi/*.pem
rm pip/_vendor/requests/*.pem
sed -i '/\.pem$/d' pip.egg-info/SOURCES.txt

sed -i '1d' pip/__init__.py

# Remove ordereddict as it is only required for python <= 2.6
rm pip/_vendor/ordereddict.py

# Remove windows executable binaries
rm -v pip/_vendor/distlib/*.exe
sed -i '/\.exe/d' setup.py
%patch13 -p1

%build
%if %{without bootstrap}
%py3_build_wheel
%else
%py3_build
%endif

%if %{with doc}
pushd docs
make html
make man
rm _build/html/.buildinfo
popd
%endif


%install
%if %{without bootstrap}
%py3_install_wheel %{python3_wheelname}
%else
%py3_install
%endif

rm %{buildroot}%{_bindir}/pip

%if %{with doc}
install -d %{buildroot}%{_mandir}/man1
install -pm0644 docs/_build/man/*.1 %{buildroot}%{_mandir}/man1/pip3.1
%endif # with doc

mkdir -p %{buildroot}%{bashcompdir}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    %{buildroot}%{_bindir}/pip3 completion --bash \
    > %{buildroot}%{bashcompdir}/pip3

sed -i -e "s/^\\(complete.*\\) pip\$/\\1 pip3 pip-3 pip3.6 pip-3.6/" \
    -e s/_pip_completion/_pip3_completion/ \
    %{buildroot}%{bashcompdir}/pip3

# Provide symlinks to executables to comply with Fedora guidelines for Python
mv %{buildroot}%{_bindir}/pip3 %{buildroot}%{_bindir}/pip%{python3_version}
ln -s ./pip%{python3_version} %{buildroot}%{_bindir}/pip-%{python3_version}

# Change shebang in /usr/bin/pip3.6 to /usr/bin/python3.6
pathfix.py -i /usr/bin/python%{python3_version} -np %{buildroot}%{_bindir}/pip%{python3_version}

# Make sure the INSTALLER is not pip, otherwise pip-nowarn-upgrade.patch
# (Patch3) won't work
echo rpm > %{buildroot}%{python3_sitelib}/pip-%{version}.dist-info/INSTALLER

%if %{without bootstrap}
mkdir -p %{buildroot}%{python3_wheeldir}
install -p dist/%{python3_wheelname} -t %{buildroot}%{python3_wheeldir}
%endif

%if %{with tests}
%check
py.test-%{python3_version} -m 'not network'
%endif


%files -n platform-python-%{srcname}
%license LICENSE.txt
%doc README.rst
%if %{with doc}
%{_mandir}/man1/pip3.*
%endif
%{python3_sitelib}/pip*

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE.txt
%doc README.rst
# The pip3 binary is created using alternatives
# defined in the python36 package
%{_bindir}/pip%{python3_version}
%{_bindir}/pip-%{python3_version}
%dir %{bashcompdir}
%{bashcompdir}/pip*

%if %{with doc}
%files doc
%license LICENSE.txt
%doc README.rst
%doc docs/_build/html
%endif # with doc

%if %{without bootstrap}
%files -n python3-%{srcname}-wheel
%license LICENSE.txt
# we own the dir for simplicity
%dir %{python3_wheeldir}/
%{python3_wheeldir}/%{python3_wheelname}
%endif

%changelog
* Thu Jan 25 2024 Release Engineering <releng@openela.org> - 9.0.3.openela.0
- Add openela to id list

* Wed Oct 06 2021 Charalampos Stratakis <cstratak@redhat.com> - 9.0.3-22
- Remove bundled windows executables
- Resolves: rhbz#2006788

* Tue Oct 05 2021 Lumír Balhar <lbalhar@redhat.com> - 9.0.3-21
- Support of yanked releases
Resolves:             rhbz#2000135

* Mon Jun 07 2021 Lumír Balhar <lbalhar@redhat.com> - 9.0.3-20
- Fix for CVE-2021-3572 - pip incorrectly handled unicode separators in git references
Resolves:             rhbz#1962856

* Fri Jan 08 2021 Lumír Balhar <lbalhar@redhat.com> - 9.0.3-19
- Fix bash completion files and simplify spec
Resolves:             rhbz#1904478

* Wed Aug 19 2020 Tomas Orsava <torsava@redhat.com> - 9.0.3-18
- Patch for pip install <url> allow directory traversal, leading to arbitrary file write
Resolves:             rhbz#1868016

* Wed Mar 04 2020 Charalampos Stratakis <cstratak@redhat.com> - 9.0.3-17
- Remove unused CA bundle from the bundled requests library
Resolves:             rhbz#1775200

* Mon Jan 13 2020 Lumír Balhar <lbalhar@redhat.com> - 9.0.3-16
- Add four new patches for CVEs in bundled urllib3 and requests
CVE-2018-20060, CVE-2019-11236, CVE-2019-11324, CVE-2018-18074
Resolves:             rhbz#1649153
Resolves:             rhbz#1700824
Resolves:             rhbz#1702473
Resolves:             rhbz#1643829

* Thu Jun 06 2019 Charalampos Stratakis <cstratak@redhat.com> - 9.0.3-15
- Create python-pip-wheel package with the wheel
Resolves:             rhbz#1718031

* Wed Mar 13 2019 Lumír Balhar <lbalhar@redhat.com> - 9.0.3-14
- Move bash completion files from platform-python- to python3- subpackage
- resolves: rhbz#1664749

* Mon Dec 03 2018 Miro Hrončok <mhroncok@redhat.com> - 9.0.3-13
- Use the system level root certificate instead of the one bundled in certifi
- Resolves: rhbz#1655255

* Wed Nov 28 2018 Tomas Orsava <torsava@redhat.com> - 9.0.3-12
- Do not show the "new version of pip" warning outside of venv
- Resolves: rhbz#1656171

* Mon Nov 19 2018 Victor Stinner <vstinner@redhat.com> - 9.0.3-11
- Prevent removing of the system packages installed under /usr/lib
  when pip install -U is executed. Patch by Michal Cyprian.
  Resolves: rhbz#1626408.

* Fri Nov 16 2018 Tomas Orsava <torsava@redhat.com> - 9.0.3-10
- Bump the NVR so it's higher than previous builds of python3-pip that have
  mistakenly gotten into the python27 module build when we were dealing with an
  MBS filtering problem. See BZ#1650568.
- Resolves: rhbz#1638836

* Mon Nov 12 2018 Lumír Balhar <lbalhar@redhat.com> - 9.0.3-6
- python3-pip requires python36 and obsoletes previous version
  where python3- and platform-python- were in one package
- Resolves: rhbz#1638836

* Mon Oct 22 2018 Tomas Orsava <torsava@redhat.com> - 9.0.3-5
- Split part of the python3-pip package into platform-python-pip
- python3-pip will only contain binaries in /usr/bin
- Resolves: rhbz#1638836

* Mon Aug 06 2018 Petr Viktorin <pviktori@redhat.com> - 9.0.3-4
- Remove the python2 subpackage
- Remove unversioned executables (only *-3.6 should be provided)

* Mon Aug 06 2018 Charalampos Stratakis <cstratak@redhat.com> - 9.0.3-3
- Correct license information

* Mon Jun 25 2018 Petr Viktorin <pviktori@redhat.com> - 9.0.3-2
- Don't build the python2 subpackage
  https://bugzilla.redhat.com/show_bug.cgi?id=1594335

* Thu Mar 29 2018 Charalampos Stratakis <cstratak@redhat.com> - 9.0.3-1
- Update to 9.0.3

* Wed Feb 21 2018 Lumír Balhar <lbalhar@redhat.com> - 9.0.1-16
- Include built HTML documentation (in the new -doc subpackage) and man page

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 04 2017 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-14
- Reintroduce the ipaddress module in the python3 subpackage.

* Mon Nov 20 2017 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-13
- Add virtual provides for the bundled libraries. (rhbz#1096912)

* Tue Aug 29 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-12
- Switch macros to bcond's and make Python 2 optional to facilitate building
  the Python 2 and Python 3 modules

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-10
- Modernized package descriptions
Resolves:             rhbz#1452568

* Tue Mar 21 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-9
- Fix typo in the sudo pip warning

* Fri Mar 03 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-8
- Patch 1 update: No sudo pip warning in venv or virtualenv

* Thu Feb 23 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-7
- Patch 1 update: Customize the warning with the proper version of the pip
  command

* Tue Feb 14 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-6
- Added patch 1: Emit a warning when running with root privileges

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-4
- Provide symlinks to executables to comply with Fedora guidelines for Python
Resolves:             rhbz#1406922

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-3
- Rebuild for Python 3.6 with wheel

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-2
- Rebuild for Python 3.6 without wheel

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 9.0.1-1
- Update to 9.0.1

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 8.1.2-5
- Enable EPEL Python 3 builds
- Use new python macros
- Cleanup spec

* Fri Aug 05 2016 Tomas Orsava <torsava@redhat.com> - 8.1.2-4
- Updated the test sources

* Fri Aug 05 2016 Tomas Orsava <torsava@redhat.com> - 8.1.2-3
- Moved python-pip into the python2-pip subpackage
- Added the python_provide macro

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 17 2016 Tomas Orsava <torsava@redhat.com> - 8.1.2-1
- Update to 8.1.2
- Moved to a new PyPI URL format
- Updated the prefix-stripping patch because of upstream changes in pip/wheel.py

* Mon Feb 22 2016 Slavek Kabrda <bkabrda@redhat.com> - 8.0.2-1
- Update to 8.0.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 7.1.0-3
- Rebuilt for Python3.5 rebuild
- With wheel set to 1

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 7.1.0-2
- Rebuilt for Python3.5 rebuild

* Wed Jul 01 2015 Slavek Kabrda <bkabrda@redhat.com> - 7.1.0-1
- Update to 7.1.0

* Tue Jun 30 2015 Ville Skyttä <ville.skytta@iki.fi> - 7.0.3-3
- Install bash completion
- Ship LICENSE.txt as %%license where available

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Matej Stuchlik <mstuchli@redhat.com> - 7.0.3-1
- Update to 7.0.3

* Fri Mar 06 2015 Matej Stuchlik <mstuchli@redhat.com> - 6.0.8-1
- Update to 6.0.8

* Thu Dec 18 2014 Slavek Kabrda <bkabrda@redhat.com> - 1.5.6-5
- Only enable tests on Fedora.

* Mon Dec 01 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-4
- Add tests
- Add patch skipping tests requiring Internet access

* Tue Nov 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-3
- Added patch for local dos with predictable temp dictionary names
  (http://seclists.org/oss-sec/2014/q4/655)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-3
- Disable build_wheel

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-2
- Rebuild as wheel for Python 3.4

* Mon Apr 07 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-1
- Updated to 1.5.4

* Mon Oct 14 2013 Tim Flink <tflink@fedoraproject.org> - 1.4.1-1
- Removed patch for CVE 2013-2099 as it has been included in the upstream 1.4.1 release
- Updated version to 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-4
- Fix for CVE 2013-2099

* Thu May 23 2013 Tim Flink <tflink@fedoraproject.org> - 1.3.1-3
- undo python2 executable rename to python-pip. fixes #958377
- fix summary to match upstream

* Mon May 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.1-2
- Fix main package Summary, it's for Python 2, not 3 (#877401)

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.3.1-1
- Update to 1.3.1, fix for CVE-2013-1888.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Fri Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file
* Thu Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package


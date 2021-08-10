%bcond_with html
%bcond_without check
# https://fedorahosted.org/fpc/ticket/381
%bcond_without bundled_fonts

# No qt4 for EL8/ELN/EL9
%if 0%{?rhel} >= 8
%bcond_with qt4
%else
%bcond_without qt4
%endif

# No WX for EL8/ELN/EL9
%if 0%{?rhel} >= 8
%bcond_with wx
%else
%bcond_without wx
%endif

# the default backend; one of GTK3Agg GTK3Cairo MacOSX Qt4Agg Qt5Agg TkAgg
# WXAgg Agg Cairo PS PDF SVG
%global backend                 TkAgg

%if "%{backend}" == "TkAgg"
%global backend_subpackage tk
%else
%  if "%{backend}" == "Qt4Agg"
%global backend_subpackage qt4
%  else
%    if "%{backend}" == "Qt5Agg"
%global backend_subpackage qt5
%    else
%      if "%{backend}" == "WXAgg"
%global backend_subpackage wx
%      endif
%    endif
%  endif
%endif

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

# Updated test images for new FreeType.
%global mpl_images_version 3.4.1

# The version of FreeType in this Fedora branch.
%global ftver 2.11.0

Name:           python-matplotlib
Version:        3.4.2
%global Version 3.4.2
Release:        5%{?dist}
Summary:        Python 2D plotting library
# qt4_editor backend is MIT
# ResizeObserver at end of lib/matplotlib/backends/web_backend/js/mpl.js is Public Domain
License:        Python and MIT and Public Domain
URL:            http://matplotlib.org
Source0:        https://github.com/matplotlib/matplotlib/archive/v%{Version}/matplotlib-%{Version}.tar.gz
Source1:        setup.cfg

# Fedora-specific patches; see:
# https://github.com/fedora-python/matplotlib/tree/fedora-patches
# Updated test images for new FreeType.
Source1000:     https://github.com/QuLogic/mpl-images/archive/v%{mpl_images_version}-with-freetype-%{ftver}/matplotlib-%{mpl_images_version}-with-freetype-%{ftver}.tar.gz
# Search in /etc/matplotlibrc:
Patch1001:      0001-matplotlibrc-path-search-fix.patch
# Increase tolerances for new FreeType everywhere:
Patch1002:      0002-Set-FreeType-version-to-%{ftver}-and-update-tolerances.patch
# Workarounds for problems with texlive 2021 (#1965547)
Patch1003:      0003-Slightly-increase-tolerance-on-rcupdate-test.patch
Patch1004:      0004-Use-new-style-for-test_text_urls_tex.patch
# https://github.com/matplotlib/matplotlib/pull/20488
Patch1005:      0005-Backport-PR-20488-FIX-Include-0-when-checking-lognor.patch
# Tweak tolerances a bit.
Patch1006:      0006-Increase-mathfont-test-tolerance-on-some-systems.patch
# https://github.com/matplotlib/matplotlib/pull/20817
Patch1007:      0007-Make-test_change_epoch-more-robust.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-langpack-en
BuildRequires:  freetype-devel
BuildRequires:  libpng-devel
BuildRequires:  qhull-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  zlib-devel

BuildRequires:  ghostscript
# No ImageMagick for EL8/ELN/EL9
%if ! 0%{?rhel} >= 8
BuildRequires:  ImageMagick
%endif
%ifnarch s390x
BuildRequires:  inkscape
%endif

BuildRequires:  texlive-collection-basic
BuildRequires:  texlive-collection-fontsrecommended
BuildRequires:  texlive-collection-latex
BuildRequires:  texlive-collection-latexrecommended
BuildRequires:  texlive-dvipng
BuildRequires:  texlive-latex-bin
BuildRequires:  texlive-luahbtex
BuildRequires:  texlive-tex-bin
BuildRequires:  texlive-xetex-bin
# Search for documentclass and add the classes here.
BuildRequires:  tex(article.cls)
BuildRequires:  tex(minimal.cls)
# Search for inputenc and add any encodings used with it.
BuildRequires:  tex(utf8.def)
BuildRequires:  tex(utf8x.def)
# Found with: rg -Io 'usepackage(\[.+\])?\{.+\}' lib | rg -o '\{.+\}' | sort -u
# and then removing duplicates in one line, etc.
BuildRequires:  tex(avant.sty)
BuildRequires:  tex(bm.sty)
BuildRequires:  tex(chancery.sty)
BuildRequires:  tex(charter.sty)
BuildRequires:  tex(color.sty)
BuildRequires:  tex(courier.sty)
BuildRequires:  tex(euler.sty)
BuildRequires:  tex(fancyhdr.sty)
BuildRequires:  tex(fontenc.sty)
BuildRequires:  tex(fontspec.sty)
BuildRequires:  tex(geometry.sty)
BuildRequires:  tex(graphicx.sty)
BuildRequires:  tex(helvet.sty)
BuildRequires:  tex(import.sty)
BuildRequires:  tex(inputenc.sty)
BuildRequires:  tex(mathpazo.sty)
BuildRequires:  tex(mathptmx.sty)
BuildRequires:  tex(pgf.sty)
BuildRequires:  tex(preview.sty)
BuildRequires:  tex(psfrag.sty)
BuildRequires:  tex(sfmath.sty)
BuildRequires:  tex(textcomp.sty)
BuildRequires:  tex(txfonts.sty)
BuildRequires:  tex(type1cm.sty)
BuildRequires:  tex(type1ec.sty)
BuildRequires:  tex(unicode-math.sty)
# See BakomaFonts._fontmap in lib/matplotlib/mathtext.py
BuildRequires:  tex(cmb10.tfm)
BuildRequires:  tex(cmex10.tfm)
BuildRequires:  tex(cmmi10.tfm)
BuildRequires:  tex(cmr10.tfm)
BuildRequires:  tex(cmss10.tfm)
BuildRequires:  tex(cmsy10.tfm)
BuildRequires:  tex(cmtt10.tfm)

%description
Matplotlib is a Python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms. Matplotlib can be used in Python
scripts, the Python and IPython shell, web application servers, and
various graphical user interface toolkits.

Matplotlib tries to make easy things easy and hard things possible.
You can generate plots, histograms, power spectra, bar charts,
errorcharts, scatterplots, etc, with just a few lines of code.

%package -n python3-matplotlib-data
Summary:        Data used by python-matplotlib
BuildArch:      noarch
%if %{with bundled_fonts}
Requires:       python3-matplotlib-data-fonts = %{version}-%{release}
%endif
Obsoletes:      python-matplotlib-data < 3

%description -n python3-matplotlib-data
%{summary}

%if %{with bundled_fonts}
%package -n python3-matplotlib-data-fonts
Summary:        Fonts used by python-matplotlib
# STIX and Computer Modern is OFL
# DejaVu is Bitstream Vera and Public Domain
License:        OFL and Bitstream Vera and Public Domain
BuildArch:      noarch
Requires:       python3-matplotlib-data = %{version}-%{release}
Obsoletes:      python-matplotlib-data-fonts < 3

%description -n python3-matplotlib-data-fonts
%{summary}
%endif

%package -n     python3-matplotlib
Summary:        Python 2D plotting library
BuildRequires:  python3-cairo
BuildRequires:  python3-certifi >= 2020.06.20
BuildRequires:  python3-cycler >= 0.10.0
BuildRequires:  python3-dateutil
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-gobject
BuildRequires:  python3-kiwisolver
BuildRequires:  python3-numpy
BuildRequires:  python3-pillow
BuildRequires:  python3-pyparsing
BuildRequires:  python3-pytz
BuildRequires:  python3-sphinx
Requires:       dejavu-sans-fonts
Recommends:     texlive-dvipng
Requires:       (texlive-dvipng if texlive-base)
Requires:       python3-matplotlib-data = %{version}-%{release}
Requires:       python3-cairo
Requires:       python3-cycler >= 0.10.0
Requires:       python3-dateutil
Requires:       python3-kiwisolver
Requires:       python3-matplotlib-%{?backend_subpackage}%{!?backend_subpackage:tk}%{?_isa} = %{version}-%{release}
%if %{with check}
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-rerunfailures
BuildRequires:  python3-pytest-timeout
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-pikepdf
%endif
Requires:       python3-numpy
Recommends:     python3-pillow
Requires:       python3-pyparsing
%if %{without bundled_fonts}
Requires:       stix-math-fonts
%else
Provides:       bundled(stix-math-fonts)
%endif

%description -n python3-matplotlib
Matplotlib is a Python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms. Matplotlib can be used in Python
scripts, the Python and IPython shell, web application servers, and
various graphical user interface toolkits.

Matplotlib tries to make easy things easy and hard things possible.
You can generate plots, histograms, power spectra, bar charts,
errorcharts, scatterplots, etc, with just a few lines of code.

%if %{with qt4}
%package -n     python3-matplotlib-qt4
Summary:        Qt4 backend for python3-matplotlib
BuildRequires:  python3-PyQt4-devel
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
Requires:       python3-matplotlib-qt5
Requires:       python3-PyQt4

# Upstream has deprecated this backend due to Qt4 being no longer supported.
# This backend will be removed when upstream does, likely in 3.5, or Fedora 35.
# The removal date is thus estimated to be the Fedora 35 Branch point.
Provides:       deprecated() = 20210810

%description -n python3-matplotlib-qt4
%{summary}
%endif

%package -n     python3-matplotlib-qt5
Summary:        Qt5 backend for python3-matplotlib
BuildRequires:  python3-qt5
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
Requires:       python3-qt5
%{?python_provide:%python_provide python3-matplotlib-qt5}

%description -n python3-matplotlib-qt5
%{summary}

%package -n     python3-matplotlib-gtk3
Summary:        GTK3 backend for python3-matplotlib
# This should be converted to typelib(Gtk) when supported
BuildRequires:  gtk3
BuildRequires:  python3-gobject
Requires:       gtk3%{?_isa}
Requires:       python3-gobject%{?_isa}
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}

%description -n python3-matplotlib-gtk3
%{summary}

%package -n     python3-matplotlib-tk
Summary:        Tk backend for python3-matplotlib
BuildRequires:  python3-tkinter
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
Requires:       python3-tkinter

%description -n python3-matplotlib-tk
%{summary}

%if %{with wx}
%package -n     python3-matplotlib-wx
Summary:        WX backend for python3-matplotlib
BuildRequires:  python3-wxpython4
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
Requires:       python3-wxpython4

%description -n python3-matplotlib-wx
%{summary}
%endif

%package -n python3-matplotlib-doc
Summary:        Documentation files for python-matplotlib
%if %{with html}
BuildRequires:  graphviz
BuildRequires:  python3-sphinx
BuildRequires:  tex(latex)
BuildRequires:  tex-preview
BuildRequires:  js-jquery >= 3.2.1
BuildRequires:  xstatic-jquery-ui-common
Requires:       js-jquery >= 3.2.1
Requires:       xstatic-jquery-ui-common
%endif
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-matplotlib-doc}

%description -n python3-matplotlib-doc
%{summary}

%package -n python3-matplotlib-test-data
Summary:        Test data for python3-matplotlib
Requires:       python3-matplotlib%{?_isa} = %{version}-%{release}

%description -n python3-matplotlib-test-data
%{summary}


%prep
%autosetup -n matplotlib-%{Version} -N

# Fedora-specific patches follow:
%patch1001 -p1
# Updated test images for new FreeType.
%patch1002 -p1
gzip -dc %SOURCE1000 | tar xf - --transform='s~^mpl-images-%{mpl_images_version}-with-freetype-%{ftver}/\([^/]\+\)/~lib/\1/tests/baseline_images/~'

# Copy setup.cfg to the builddir
cp -p %{SOURCE1} setup.cfg

%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1


%build
%set_build_flags
export http_proxy=http://127.0.0.1/

MPLCONFIGDIR=$PWD %py3_build
%if %{with html}
# Need to make built matplotlib libs available for the sphinx extensions:
pushd doc
    MPLCONFIGDIR=$PWD/.. \
    PYTHONPATH=`realpath ../build/lib.linux*` \
        %{python3} make.py html
popd
%endif
# Ensure all example files are non-executable so that the -doc
# package doesn't drag in dependencies
find examples -name '*.py' -exec chmod a-x '{}' \;


%install
export http_proxy=http://127.0.0.1/

MPLCONFIGDIR=$PWD %py3_install

# Delete unnecessary files.
rm %{buildroot}%{python3_sitearch}/matplotlib/backends/web_backend/.{eslintrc.js,prettierignore,prettierrc}
rm %{buildroot}%{python3_sitearch}/matplotlib/tests/tinypages/.gitignore
rm %{buildroot}%{python3_sitearch}/matplotlib/tests/tinypages/_static/.gitignore

# Move files to Fedora-specific locations.
mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_datadir}/matplotlib
mv %{buildroot}%{python3_sitearch}/matplotlib/mpl-data \
   %{buildroot}%{_datadir}/matplotlib
%if %{without bundled_fonts}
rm -rf %{buildroot}%{_datadir}/matplotlib/mpl-data/fonts
%endif


%if %{with check}
%check
# These files confuse pytest, and we want to test the installed copy.
rm -rf build*/

# We need to prime this LaTeX cache stuff, or it might fail while running tests
# in parallel.
mktexfmt latex.fmt
mktexfmt lualatex.fmt
mktexfmt pdflatex.fmt
mktexfmt xelatex.fmt

export http_proxy=http://127.0.0.1/
# Skips:
#  * test_invisible_Line_rendering: Checks for "slowness" that often fails on a
#    heavily-loaded builder.
MPLCONFIGDIR=$PWD \
PYTHONPATH=%{buildroot}%{python3_sitearch} \
PYTHONDONTWRITEBYTECODE=1 \
     xvfb-run -a -s "-screen 0 640x480x24" \
         %{python3} tests.py -ra -n $(getconf _NPROCESSORS_ONLN) \
             -m 'not network' \
             -k 'not test_invisible_Line_rendering and not Qt5Agg'
# Run Qt5Agg tests separately to not conflict with Qt4 tests.
MPLCONFIGDIR=$PWD \
PYTHONPATH=%{buildroot}%{python3_sitearch} \
PYTHONDONTWRITEBYTECODE=1 \
     xvfb-run -a -s "-screen 0 640x480x24" \
         %{python3} tests.py -ra -n $(getconf _NPROCESSORS_ONLN) \
             -m 'not network' -k 'Qt5Agg'
%endif


%files -n python3-matplotlib-data
%{_datadir}/matplotlib/mpl-data/
%if %{with bundled_fonts}
%exclude %{_datadir}/matplotlib/mpl-data/fonts/
%endif

%if %{with bundled_fonts}
%files -n python3-matplotlib-data-fonts
%{_datadir}/matplotlib/mpl-data/fonts/
%endif

%files -n python3-matplotlib-doc
%doc examples
%if %{with html}
%doc doc/build/html/*
%endif

%files -n python3-matplotlib
%license LICENSE/
%doc README.rst
%{python3_sitearch}/matplotlib-*.egg-info/
%{python3_sitearch}/matplotlib-*-nspkg.pth
%{python3_sitearch}/matplotlib/
%exclude %{python3_sitearch}/matplotlib/tests/baseline_images/*
%{python3_sitearch}/mpl_toolkits/
%exclude %{python3_sitearch}/mpl_toolkits/tests/baseline_images/*
%pycached %{python3_sitearch}/pylab.py
%pycached %exclude %{python3_sitearch}/matplotlib/backends/backend_qt4*.py
%if %{without qt4}
%pycached %exclude %{python3_sitearch}/matplotlib/backends/backend_qt5*.py
%endif
%pycached %exclude %{python3_sitearch}/matplotlib/backends/backend_gtk*.py
%pycached %exclude %{python3_sitearch}/matplotlib/backends/_backend_tk.py
%pycached %exclude %{python3_sitearch}/matplotlib/backends/backend_tk*.py
%exclude %{python3_sitearch}/matplotlib/backends/_tkagg.*
%pycached %exclude %{python3_sitearch}/matplotlib/backends/backend_wx*.py
%exclude %{_pkgdocdir}/*/

%files -n python3-matplotlib-test-data
%{python3_sitearch}/matplotlib/tests/baseline_images/
%{python3_sitearch}/mpl_toolkits/tests/baseline_images/

%if %{with qt4}
%files -n python3-matplotlib-qt4
%pycached %{python3_sitearch}/matplotlib/backends/backend_qt4.py
%pycached %{python3_sitearch}/matplotlib/backends/backend_qt4agg.py
%endif

# This subpackage is empty because the Qt4 backend imports it, so we leave
# these files in the default package, and only use this one for dependencies.
%files -n python3-matplotlib-qt5
%if %{without qt4}
%pycached %{python3_sitearch}/matplotlib/backends/backend_qt5.py
%pycached %{python3_sitearch}/matplotlib/backends/backend_qt5agg.py
%endif

%files -n python3-matplotlib-gtk3
%pycached %{python3_sitearch}/matplotlib/backends/backend_gtk*.py

%files -n python3-matplotlib-tk
%pycached %{python3_sitearch}/matplotlib/backends/backend_tk*.py
%pycached %{python3_sitearch}/matplotlib/backends/_backend_tk.py
%{python3_sitearch}/matplotlib/backends/_tkagg.*

%if %{with wx}
%files -n python3-matplotlib-wx
%pycached %{python3_sitearch}/matplotlib/backends/backend_wx*.py
%endif


%changelog
* Mon Aug 09 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.4.2-5
- Update test images for FreeType 2.11.0
- Backport patch for NumPy 1.21

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.4.2-3
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.4.2-2
- Bootstrap for Python 3.10

* Fri Jun 04 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.4.2-2
- Workaround failures with texlive 2021

* Sat May 08 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.4.2-1
- Update to latest version (#1958461)

* Wed Mar 31 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.4.1-1
- Update to latest version (#1943482)

* Thu Mar 11 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.4.0~rc3-1
- Update to latest release candidate

* Fri Feb 19 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.4.0~rc1-1
- Update to latest release candidate
- Deprecated python3-matplotlib-qt4 subpackage

* Tue Feb 16 2021 Troy Dawson <tdawson@redhat.com> - 3.3.4-3
- Add build deps that were only getting pulled in by other dependencies

* Mon Feb 01 2021 Tomas Popela <tpopela@redhat.com> - 3.3.4-2
- Conditionalize the WX backend and disable it on RHEL 8+ as WX is not
  available there.

* Thu Jan 28 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.3.4-1
- Update to latest version (#1921574)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 02 2020 Tomas Popela <tpopela@redhat.com> - 3.3.3-2
- Don't build the Qt 4 backend in ELN/RHEL 9 as Qt 4 won't be available there
  (reuse
  https://src.fedoraproject.org/rpms/python-matplotlib/c/588e490738b06d525910f05bc1ba3f3f05ec7d50?branch=epel8)

* Thu Nov 12 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.3.3-1
- Update to latest version (#1897021)

* Tue Sep 15 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.3.2-1
- Update to latest version (#1878999)

* Thu Aug 13 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.3.1-1
- Update to latest version
- Fixes RHBZ#1868838

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.3.0-1
- Update to latest version
- Fixes RHBZ#1858120

* Tue Jun 30 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.3.0-0.2.rc1
- Add more test dependencies

* Mon Jun 29 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.3.0-0.1.rc1
- Update to latest version

* Sat Jun 20 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.2.2-1
- Update to latest version

* Mon Jun 01 2020 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-2
- Only recommend texlive-dvipng (but require it if texlive is installed) (#1509657)

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-1.1
- Rebuilt for Python 3.9

* Wed Mar 18 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.2.1-1
- Update to latest version

* Tue Mar 03 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.2.0-1
- Update to latest version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 22 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.1.2-1
- Update to latest version

* Fri Sep 06 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.1.1-2
- Backport bool deprecation fix for Python 3.8

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.1-1.1
- Rebuilt for Python 3.8

* Thu Aug 08 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.1.1-1
- Update to latest version

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul  3 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.3-2
- Update Obsoletes to be later than the last python2 builds (#1726490)

* Sat Mar 02 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.0.3-1
- Update to latest version

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.0.2-1
- Update to latest version

* Wed Oct 31 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.0.1-1
- Update to latest version

* Fri Sep 21 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-2
- Obsolete old python-matplotlib-data* to prevent conflicts and provide an upgrade path

* Wed Sep 19 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.0.0-1
- Update to latest version
- Drop Python 2 subpackages
- Stop setting a default backend (allow Matplotlib to choose automatically)

* Mon Aug 13 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.2.3-1
- Update to latest version

* Fri Jul 20 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.2.2-4
- Don't use unversioned Python in build (#1605766)
- Add missing texlive-cm BR

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.2-3
- Rebuilt for Python 3.7

* Tue Apr 17 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.2.2-2
- Remove bytecode produced by pytest
- Add python?-matplotlib-test-data subpackages

* Sat Mar 31 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.2.2-1
- Update to latest release
- Run tests in parallel

* Tue Mar 13 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.1.2-3
- Cleanup spec file of old conditionals
- Use more python2- dependencies

* Mon Feb 05 2018 Karsten Hopp <karsten@redhat.com> - 2.1.2-2
- update and fix spec file conditionals

* Sun Jan 21 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.1.2-1
- Update to latest release

* Sun Dec 10 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.1.1-1
- Update to latest release

* Mon Oct 16 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.1.0-1
- Update to latest release

* Thu Sep 28 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.0.2-1
- Update to latest release

* Thu Sep 28 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.0.1-1
- Update to latest release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.0-3
- Fix NVR

* Mon Mar 06 2017 Thomas Spura <tomspur@fedoraproject.org> - 2.0.0-2.2
- Remove copyrighted file from tarball (gh-8034)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Dan Horák <dan[at]danny.cz> - 2.0.0-2
- Apply the 'aarch64' test tolerance patch on s390(x) also

* Fri Jan 20 2017 Orion Poplawski <orion@cora.nwra.com> - 2.0.0-1
- Update to 2.0.0 final

* Tue Jan 10 2017 Adam Williamson <awilliam@redhat.com> - 2.0.0-0.7.rc2
- Update to 2.0.0rc2
- Fix more big-endian integer issues
- Apply the 'aarch64' test tolerance patch on ppc64 also (it's affected by same issues)
- Tweak the 'i686' test tolerance patch a bit (some errors are gone, some new ones)
- Re-enable test suite for all arches
- Note a remaining quasi-random test issue that causes build to fail sometimes

* Mon Jan 09 2017 Adam Williamson <awilliam@redhat.com> - 2.0.0-0.6.b4
- Fix another integer type issue which caused more issues on ppc64

* Sun Jan 08 2017 Adam Williamson <awilliam@redhat.com> - 2.0.0-0.5.b4
- Fix int type conversion error that broke text rendering on ppc64 (#1411070)

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.0.0-0.4.b4
- Rebuild for Python 3.6

* Mon Oct 24 2016 Dan Horák <dan[at]danny.cz> - 2.0.0-0.3.b4
- disable tests on some alt-arches to unblock depending builds

* Mon Sep 26 2016 Dominik Mierzejewski <rpm@greysector.net> - 2.0.0-0.2.b4
- add missing runtime dependencies for python2 package

* Sat Sep 10 2016 Dominik Mierzejewski <rpm@greysector.net> - 2.0.0-0.1.b4
- Update to 2.0.0b4
- Drop upstreamed or obsolete patches
- python-cycler >= 0.10.0 is required
- move around Requires and BRs and sort more or less alphabetically
- don't ship baseline images for tests (like Debian)
- Require stix fonts only when they're not bundled
- disable HTML doc building for bootstrapping 2.0.x series
- relax image rendering tests tolerance due to freetype version differences
- disable some failing tests on aarch64 for now

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-0.2.rc2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun 03 2016 Dominik Mierzejewski <rpm@greysector.net> - 1.5.1-7
- Update to 1.5.2rc2.
- Drop wrong hunk from use-system-six patch.
- Patch new qhull paths on F25+ instead of using sed.
- Rebase failing tests patch.

* Mon May 23 2016 Dominik Mierzejewski <rpm@greysector.net> - 1.5.1-6
- Upstream no longer ships non-free images, use pristine source.

* Wed May 18 2016 Dominik Mierzejewski <rpm@greysector.net> - 1.5.1-5
- Unbundle python-six (#1336740).
- Run tests (and temporarily disable failing ones).
- Use upstream-recommended way of running tests in parallel.
- python2-cycler and -mock are required for running tests.

* Sat Apr 30 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.1-4
- Rebuild for qhull-2015.2-1.
- Reflect qhull_a.h's location having changed.

* Wed Apr 6 2016 Orion Poplawski <orion@cora.nwra.com> - 1.5.1-3
- Add requires python-cycler

* Tue Apr 05 2016 Jon Ciesla <limburgher@gmail.com> - 1.5.1-2
- Drop agg-devel BR, fix sphinx build with python*cycler BR

* Mon Apr 04 2016 Thomas Spura <tomspur@fedoraproject.org> - 1.5.1-1
- update to 1.5.1 (#1276806)
- Add missing requires of dvipng to python3-matplotlib (#1270202)
- use bundled agg (#1276806)
- Drop cxx patch (was dropped upstream)
- Regenerate search path patch2

* Mon Apr 04 2016 Thomas Spura <tomspur@fedoraproject.org> - 1.4.3-13
- Require the qt5 subpackage from the qt4 subpackage (#1219556)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Thomas Spura <tomspur@fedoraproject.org> - 1.4.3-11
- Fix another requires of the main package

* Thu Jan 07 2016 Thomas Spura <tomspur@fedoraproject.org> - 1.4.3-10
- Fix requiring the correct backend from the main package

* Thu Jan 07 2016 Thomas Spura <tomspur@fedoraproject.org> - 1.4.3-9
- regenerate tarball to exclude lena image (#1295174)

* Sun Nov 15 2015 Thomas Spura <tomspur@fedoraproject.org> - 1.4.3-8
- Pick upstream patch for fixing the gdk backend #1231748
- Add python2 subpackages and use python_provide

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.3-5
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 25 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.3-4
- Split out python-matplotlib-gtk, python-matplotlib-gtk3,
  python3-matplotlib-gtk3 subpackages (#1067373)
- Add missing requirements on gtk

* Tue Feb 24 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.3-3
- Use %%license, add skimage to build requirements

* Tue Feb 17 2015 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.4.3-2
- Disable Qt5 backend on Fedora <21 and RHEL

* Tue Feb 17 2015 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.4.3-1
- New upstream release (#1134007)
- Add Qt5 backend

* Tue Jan 13 2015 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.4.2-1
- Bump to new upstream release
- Add qhull-devel to BR
- Add six to Requires

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Feb 11 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.3.1-3
- Make TkAgg the default backend
- Remove python2 dependency from -data subpackage

* Mon Jan 27 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.3.1-2
- Correct environment for and enable %%check
- Install system wide matplotlibrc under /etc
- Do not duplicate mpl-data for python2 and python3 packages
- Conditionally bundle data fonts (https://fedorahosted.org/fpc/ticket/381)

* Sat Jan 25 2014 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-1
- update to 1.3.1
- use GTKAgg as backend (#1030396, #982793, #1049624)
- use fontconfig
- add %%check for local testing (testing requires a display)

* Wed Aug  7 2013 Thomas Spura <tomspur@fedoraproject.org> - 1.3.0-1
- update to new version
- use xz to compress sources
- drop fontconfig patch (upstream)
- drop tk patch (upstream solved build issue differently)
- redo use system agg patch
- delete bundled python-pycxx headers
- fix requires of python3-matplotlib-qt (fixes #988412)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jon Ciesla <limburgher@gmail.com> - 1.2.0-14
- agg rebuild.

* Wed Apr 10 2013 Thomas Spura <tomspur@fedoraproject.org> - 1.2.0-13
- use python3 version in python3-matplotlib-qt4 (#915727)
- include __pycache__ files in correct subpackages on python3

* Wed Apr  3 2013 Thomas Spura <tomspur@fedoraproject.org> - 1.2.0-12
- Decode output of subprocess to utf-8 or regex will fail (#928326)

* Tue Apr  2 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-11
- Make stix-fonts a requires of matplotlib (#928326)

* Thu Mar 28 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-10
- Use stix fonts avoid problems with missing cm fonts (#908717)
- Correct type mismatch in python3 font_manager (#912843, #928326)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-8
- Update fontconfig patch to apply issue found by upstream
- Update fontconfig patch to apply issue with missing afm fonts (#896182)

* Wed Jan 16 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-7
- Use fontconfig by default (#885307)

* Thu Jan  3 2013 David Malcolm <dmalcolm@redhat.com> - 1.2.0-6
- remove wx support for rhel >= 7

* Tue Dec 04 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-5
- Reinstantiate wx backend for python2.x.
- Run setup.py under xvfb-run to detect and default to gtk backend (#883502)
- Split qt4 backend subpackage and add proper requires for it.
- Correct wrong regex in tcl libdir patch.

* Tue Nov 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-4
- Obsolete python-matplotlib-wx for clean updates.

* Tue Nov 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-3
- Enable python 3 in fc18 as build requires are now available (#879731)

* Thu Nov 22 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-2
- Build python3 only on f19 or newer (#837156)
- Build requires python3-six if building python3 support (#837156)

* Thu Nov 22 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-1
- Update to version 1.2.0
- Revert to regenerate tarball with generate-tarball.sh (#837156)
- Assume update to 1.2.0 is for recent releases
- Remove %%defattr
- Remove %%clean
- Use simpler approach to build html documentation
- Do not use custom/outdated setup.cfg
- Put one BuildRequires per line
- Enable python3 support
- Cleanup spec as wx backend is no longer supported
- Use default agg backend
- Fix bogus dates in changelog by assuming only week day was wrong

* Fri Aug 17 2012 Jerry James <loganjerry@gmail.com> - 1.1.1-1
- Update to version 1.1.1.
- Remove obsolete spec file elements
- Fix sourceforge URLs
- Allow sample data to have a different version number than the sources
- Don't bother removing problematic file since we remove entire agg24 directory
- Fix building with pygtk in the absence of an X server
- Don't install license text for bundled software that we don't bundle

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 3 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.1.0-1
- Update to version 1.1.0.
- Do not regenerate upstream tarball but remove problematic file in %%prep.
- Remove non longer applicable/required patch0.
- Rediff/rename -noagg patch.
- Remove propagate-timezone-info-in-plot_date-xaxis_da patch already applied.
- Remove tkinter patch now with critical code in a try block.
- Remove png 1.5 patch as upstream is now png 1.5 aware.
- Update file list.

* Wed Apr 18 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.1-20
- remove wx support for rhel >= 7

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-19
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.1-17
- fix the build against libpng 1.5

* Tue Dec  6 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.1-16
- fix egg-info conditional for RHEL

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.0.1-15
- Rebuild for new libpng

* Mon Oct 31 2011 Dan Horák <dan[at]danny.cz> - 1.0.1-14
- fix build with new Tkinter which doesn't return an expected value in __version__

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.0.1-13
- apply upstream bugfix for timezone formatting (Bug 735677)

* Fri May 20 2011 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-12
- Add Requires dvipng (Bug 684836)
- Build against system agg (Bug 612807)
- Use system pyparsing (Bug 702160)

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-11
- Set PYTHONPATH during html doc building using find to prevent broken builds

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-10
- Spec file cleanups for readability

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-9
- Bump and rebuild

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-8
- Fix spec file typos so package builds

* Fri Feb 25 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-7
- Remove a debugging echo statement from the spec file
- Fix some line endings and permissions in -doc sub-package

* Fri Feb 25 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-6
- Spec file cleanups to silence some rpmlint warnings

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-5
- Add default attr to doc sub-package file list
- No longer designate -doc subpackage as noarch
- Add arch specific Requires for tk, wx and doc sub-packages

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-4
- Enable wxPython backend
- Make -doc sub-package noarch

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-3
- Add conditional for optionally building doc sub-package
- Add flag to build low res images for documentation
- Add matplotlib-1.0.1-plot_directive.patch to fix build of low res images
- Remove unused patches

* Sat Feb 19 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-2
- Build and package HTML documentation in -doc sub-package
- Move examples to -doc sub-package
- Make examples non-executable

* Fri Feb 18 2011 Thomas Spura <tomspur@fedoraproject.org> - 1.0.1-1
- update to new bugfix version (#678489)
- set file attributes in tk subpackage
- filter private *.so

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 8 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.0.0-1
- New upstream release
- Remove undistributable file from bundled agg library

* Thu Jul 1 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.3-1
- New upstream release

* Thu May 27 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-4
- Upstream patch to fix deprecated gtk tooltip warning.

* Mon Apr 12 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-2
- Bump to rebuild against numpy 1.3

* Thu Apr 1 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-1
- Bump to rebuild against numpy 1.4.0

* Fri Dec 11 2009 Jon Ciesla <limb@jcomserv.net> - 0.99.1.2
- Update to 0.99.1.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-4
- Fixed font dep after font guideline change

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-2
- Add dep on DejaVu Sans font for default font support

* Mon Dec 22 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-1
- Latest upstream release
- Strip out included fonts

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.98.3-2
- Rebuild for Python 2.6

* Wed Aug  6 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.3-1
- Latest upstream release

* Tue Jul  1 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.1-1
- Latest upstream release

* Fri Mar  21 2008 Jef Spaleta <jspaleta[AT]fedoraproject org> - 0.91.2-2
- gcc43 cleanups

* Fri Mar  21 2008 Jef Spaleta <jspaleta[AT]fedoraproject org> - 0.91.2-1
- New upstream version
- Adding Fedora specific setup.cfg from included template
- removed numarry and numerics build requirements

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.90.1-6
- Autorebuild for GCC 4.3

* Fri Jan  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-5
- Fixed typo in spec.

* Fri Jan  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-4
- Support for Python Eggs for F9+

* Thu Jan  3 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-3
- Rebuild for new Tcl 8.5

* Thu Aug 23 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.1-2
- Update license tag to Python
- Rebuild for BuildID

* Mon Jun 04 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.1-1
- Update to 0.90.1

* Wed Feb 14 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.0-2
- Rebuild for Tcl/Tk downgrade

* Sat Feb 10 2007 Jef Spaleta <jspaleta@gmail.com> 0.90.0-2
- Release bump for rebuild against new tk

* Fri Feb 09 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.0-1
- Update to 0.90.0

* Fri Jan  5 2007 Orion Poplawski <orion@cora.nwra.com> 0.87.7-4
- Add examples to %%docs

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 0.87.7-3
- Release bump for rebuild against python 2.5 in devel tree

* Tue Dec  5 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.7-2
- Force build of gtk/gtkagg backends in mock (bug #218153)
- Change Requires from python-numeric to numpy (bug #218154)

* Tue Nov 21 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.7-1
- Update to 0.87.7 and fix up the defaults to use numpy
- Force build of tkagg backend without X server
- Use src.rpm from Jef Spaleta, closes bug 216578

* Fri Oct  6 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.6-1
- Update to 0.87.6

* Thu Sep  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.5-1
- Update to 0.87.5

* Thu Jul 27 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.4-1
- Update to 0.87.4

* Wed Jun  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.3-1
- Update to 0.87.3

* Mon May 15 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.2-2
- Rebuild for new numpy

* Tue Mar  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.2-1
- Update to 0.87.2

* Tue Mar  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.1-1
- Update to 0.87.1
- Add pycairo >= 1.0.2 requires (FC5+ only)

* Fri Feb 24 2006 Orion Poplawski <orion@cora.nwra.com> 0.87-1
- Update to 0.87
- Add BR numpy and python-numarray
- Add patch to keep Numeric as the default numerix package
- Add BR tkinter and tk-devel for TkInter backend
- Make separate package for Tk backend

* Tue Jan 10 2006 Orion Poplawski <orion@cora.nwra.com> 0.86-1
- Update to 0.86

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 0.85-2
- Rebuild

* Sun Nov 20 2005 Orion Poplawski <orion@cora.nwra.com> 0.85-1
- New upstream version 0.85

* Mon Sep 19 2005 Orion Poplawski <orion@cora.nwra.com> 0.84-1
- New upstream version 0.84

* Tue Aug 02 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-3
- bump release

* Tue Aug 02 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-2
- Add Requires: python-numeric, pytz, python-dateutil

* Fri Jul 29 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-1
- New upstream version matplotlib 0.83.2

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.1-2
- Bump rel to fix botched tag

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.1-1
- New upstream version matplotlib 0.83.1

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-4
- BuildRequires: pytz, python-dateutil - use upstream
- Don't use INSTALLED_FILES, list dirs
- Fix execute permissions

* Fri Jul 01 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-3
- Use %%{python_sitearch}

* Thu Jun 30 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-2
- Rename to python-matplotlib
- Remove unneeded Requires: python
- Add private directories to %%files

* Tue Jun 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-1
- Initial package for Fedora Extras

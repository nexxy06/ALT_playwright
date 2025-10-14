%define _unpackaged_files_terminate_build 0
%define pypi_name playwright

%def_without check

Name: python3-module-%pypi_name
Version: 1.55.0
Release: alt1
Summary: Playwright is a Python library to automate Chromium, Firefox and WebKit browsers with a single API.
License: Apache-2.0
Group: Development/Python3
URL: https://pypi.org/project/playwright/
VCS: https://github.com/microsoft/playwright-python
BuildArch: noarch

Source: %name-%version.tar
Patch0: playwright-1.55.0-path-fix.patch
Source1: playwright-1.55.0-beta-1756314050000-linux.zip

BuildRequires(pre): rpm-build-python3
BuildRequires: python3-module-setuptools
BuildRequires: python3-module-setuptools_scm
BuildRequires: python3-module-wheel
BuildRequires: python3-module-auditwheel
BuildRequires: curl
BuildRequires: unzip

%description
%summary

%prep
%setup
%patch0 -p1

# Removing the versioning restrictions
sed -e 's|==.*"|"|' -i pyproject.toml

# Installing the correct driver version
sed -e 's|driver_version = ".*"|driver_version = "%version"|' -i setup.py

# setuptools_scm implements a file_finders entry point which returns all files
# tracked by SCM.
if [ ! -d .git ]; then
     git init
     git config user.email author@example.com
     git config user.name author
     git add .
     git commit -m 'release'
     git tag '%version'
fi

mkdir -p driver
cp %{SOURCE1} driver/playwright-1.55.0-beta-1756314050000-linux.zip

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%version
#%pyproject_build
python3 -m build --wheel --no-isolation

%install
%pyproject_install
#rm -f %buildroot%python3_sitelibdir/playwright/driver/node
#ln -s /usr/bin/node %buildroot%python3_sitelibdir/playwright/driver/node

%check
%pyproject_run_pytest -v -m 'not request'

%files
%doc *.md
%python3_sitelibdir/%pypi_name/
%python3_sitelibdir/%{pyproject_distinfo %pypi_name}

%changelog
* Sun Oct 12 2025 Nikita Panov <nikpan254@gmail.com> 1.55.0-alt1
- Initial build for Sisyphus


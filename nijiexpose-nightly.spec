%define nijiexpose_ver 0.0.0
%define nijiexpose_dist 282
%define nijiexpose_short ec1ed49

%define nijiexpose_suffix ^%{nijiexpose_dist}.git%{nijiexpose_short}

Name:           nijiexpose-nightly
Version:        %{nijiexpose_ver}%{?nijiexpose_suffix:}
Release:        %autorelease
Summary:        Tool to use nijilive puppets

# Bundled lib licenses
##   bindbc-loader licenses: BSL-1.0
##   bindbc-lua licenses: BSL-1.0
##   bindbc-sdl licenses: BSL-1.0
##   ddbus licenses: MIT
##   diet-ng licenses: MIT
##   dportals licenses: BSD-2-Clause
##   dunit licenses: MIT
##   eventcore licenses: MIT
##   facetrack-d licenses: BSD-2-Clause
##   fghj licenses: BSL-1.0
##   i18n-d licenses: BSD-2-Clause
##   i2d-imgui licenses: BSL-1.0 and MIT
##   i2d-opengl licenses: BSL-1.0
##   imagefmt licenses: BSD-2-Clause
##   inmath licenses: BSD-2-Clause
##   lumars licenses: MIT
##   mir-algorithm licenses: Apache-2.0
##   mir-core licenses: Apache-2.0
##   mir-linux-kernel licenses: BSL-1.0
##   nijilive licenses: BSD-2-Clause
##   nijiui licenses: BSD-2-Clause
##   openssl licenses: OpenSSL
##   silly licenses: ISC
##   stdx-allocator licenses: BSD-2-Clause
##   taggedalgebraic licenses: BSD-2-Clause
##   tinyfiledialogs licenses: Zlib
##   vibe-container licenses: MIT
##   vibe-core licenses: MIT
##   vibe-d licenses: MIT
##   vmc-d licenses: BSD-2-Clause
License:        BSD-2-Clause and Apache-2.0 and BSL-1.0 and ISC and MIT and OpenSSL and Zlib

URL:            https://github.com/grillo-delmal/nijiexpose-nightly

Source0:        https://github.com/grillo-delmal/nijiexpose-nightly/releases/download/nightly/nijiexpose-source.zip
Source1:        nijiexpose-nightly.desktop
Source2:        nijiexpose-nightly.appdata.xml
Source3:        dub.selections.json

# dlang
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  jq

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  git

#bindbc-lua reqs
BuildRequires:       luajit-devel

#dportals reqs
BuildRequires:       dbus-devel

#i2d-imgui reqs
BuildRequires:       cmake
BuildRequires:       gcc
BuildRequires:       gcc-c++
BuildRequires:       freetype-devel
BuildRequires:       SDL2-devel

#openssl reqs
BuildRequires:       openssl-devel

Requires:       hicolor-icon-theme

#bindbc-lua deps
Requires:       luajit

#dportals deps
Requires:       dbus

#i2d-imgui deps
Requires:       libstdc++
Requires:       freetype
Requires:       SDL2

#openssl deps
Requires:       openssl


%description
nijilive is a framework for realtime 2D puppet animation which can be used for VTubing, 
game development and digital animation. 
nijiexpose is a tool that lets you use nijilive puppets as tracked avatars.
This is a nightly build of nijiexpose!
nijiexpose may crash unexpectedly and you will likely encounter bugs.
Make sure to save and back up your work often!


%prep
%setup -c

jq "map(.path = ([\"$(pwd)\"] + (.path | split(\"/\"))[-4:] | join(\"/\")) )" <<<$(<.dub/packages/local-packages.json) > .dub/packages/local-packages.linux.json
rm .dub/packages/local-packages.json
mv .dub/packages/local-packages.linux.json .dub/packages/local-packages.json
dub add-local .flatpak-dub/semver/*/semver
dub add-local .flatpak-dub/gitver/*/gitver


%build
export DFLAGS="%{_d_optflags} -L-rpath=%{_libdir}/nijiexpose/"

# Build metadata
dub build --skip-registry=all --compiler=ldc2 --config=meta

# Build the project, with its main file included, without unittests
dub build --skip-registry=all --compiler=ldc2 --config=linux-nightly --build=debug


%install
install -d ${RPM_BUILD_ROOT}%{_libdir}/nijiexpose-nightly
install -p ./out/cimgui.so ${RPM_BUILD_ROOT}%{_libdir}/nijiexpose-nightly/cimgui.so

install -d ${RPM_BUILD_ROOT}%{_bindir}
install -p ./out/nijiexpose ${RPM_BUILD_ROOT}%{_bindir}/nijiexpose-nightly

install -d ${RPM_BUILD_ROOT}%{_datadir}/applications/
install -p -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_datadir}/applications/nijiexpose-nightly.desktop
desktop-file-validate \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/nijiexpose-nightly.desktop

install -d ${RPM_BUILD_ROOT}%{_metainfodir}/
install -p -m 644 %SOURCE2 ${RPM_BUILD_ROOT}%{_metainfodir}/nijiexpose-nightly.appdata.xml
appstream-util validate-relax --nonet \
    ${RPM_BUILD_ROOT}%{_metainfodir}/nijiexpose-nightly.appdata.xml

install -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/
install -p -m 644 ./res/icon_x256.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/nijiexpose-nightly.png

install -d ${RPM_BUILD_ROOT}%{_datadir}/nijiexpose-nightly/
install -p -m 644 %SOURCE3 ${RPM_BUILD_ROOT}%{_datadir}/nijiexpose-nightly/dub.selections.json


%files
%license LICENSE
%{_bindir}/nijiexpose-nightly
%{_libdir}/nijiexpose-nightly/*
%{_metainfodir}/nijiexpose-nightly.appdata.xml
%{_datadir}/applications/nijiexpose-nightly.desktop
%{_datadir}/icons/hicolor/256x256/apps/nijiexpose-nightly.png
%{_datadir}/nijiexpose-nightly/dub.selections.json


%changelog
%autochangelog

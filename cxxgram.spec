%global appname tdesktop

Name: cxxgram
Version: 1.1.23
Release: 1%{?dist}

License: GPLv3+
Summary: Telegram is a new era of messaging
Group: Applications/Internet
URL: https://github.com/procxx/%{appname}
ExclusiveArch: i686 x86_64

Source0: %{url}/archive/v%{version}.tar.gz#/%{appname}-%{version}.tar.gz
Patch0: 0001-Small-fixes.patch

Requires: qt5-qtimageformats%{?_isa}
Requires: hicolor-icon-theme
Requires: gtk3%{?_isa}
Recommends: libappindicator-gtk3%{?_isa}

# Compilers and tools...
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: gcc-c++
BuildRequires: chrpath
BuildRequires: cmake
BuildRequires: gcc

# Development packages for Telegram Desktop...
BuildRequires: guidelines-support-library-devel
BuildRequires: libappindicator-devel
BuildRequires: mapbox-variant-devel
BuildRequires: ffmpeg-devel >= 3.1
BuildRequires: openal-soft-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: libtgvoip-devel
BuildRequires: libstdc++-devel
BuildRequires: range-v3-devel
BuildRequires: openssl-devel
BuildRequires: minizip-devel
BuildRequires: opus-devel
BuildRequires: gtk3-devel
BuildRequires: zlib-devel
BuildRequires: dee-devel
BuildRequires: xz-devel

%description
Telegram is a messaging app with a focus on speed and security, it’s super
fast, simple and free. You can use Telegram on all your devices at the same
time — your messages sync seamlessly across any of your phones, tablets or
computers.

With Telegram, you can send messages, photos, videos and files of any type
(doc, zip, mp3, etc), as well as create groups for up to 200 people. You can
write to your phone contacts and find people by their usernames. As a result,
Telegram is like SMS and email combined — and can take care of all your
personal or business messaging needs.

%prep
# Unpacking Telegram Desktop source archive...
%autosetup -n %{appname}-%{version} -p1

%build
%cmake .
%make_build

%install
# Installing executables...
mkdir -p "%{buildroot}%{_bindir}"
chrpath -d out/Release/Telegram
install -m 0755 -p out/Release/Telegram "%{buildroot}%{_bindir}/%{name}"

# Installing desktop shortcut...
mv lib/xdg/telegramdesktop.desktop lib/xdg/%{name}.desktop
desktop-file-install --dir="%{buildroot}%{_datadir}/applications" lib/xdg/%{name}.desktop

# Installing icons...
for size in 16 32 48 64 128 256 512; do
    dir="%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps"
    install -d "$dir"
    install -m 0644 -p Telegram/Resources/art/icon${size}.png "$dir/%{name}.png"
done

# Installing tg protocol handler...
install -d "%{buildroot}%{_datadir}/kde4/services"
install -m 0644 -p lib/xdg/tg.protocol "%{buildroot}%{_datadir}/kde4/services/tg.protocol"

# Installing appdata for Gnome Software...
install -d "%{buildroot}%{_datadir}/appdata"
install -m 0644 -p lib/xdg/telegramdesktop.appdata.xml "%{buildroot}%{_datadir}/appdata/%{name}.appdata.xml"

%check
appstream-util validate-relax --nonet "%{buildroot}%{_datadir}/appdata/%{name}.appdata.xml"

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc README.md changelog.txt
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/kde4/services/tg.protocol
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Sat Dec 09 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.23-1
- Initial SPEC release.

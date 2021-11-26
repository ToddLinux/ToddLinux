# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf man-db-2.9.4.tar.xz
    cd man-db-2.9.4
    return
}

configure() {
    ./configure --prefix=/usr                        \
                --docdir=/usr/share/doc/man-db-2.9.4 \
                --sysconfdir=/etc                    \
                --disable-setuid                     \
                --enable-cache-owner=bin             \
                --with-browser=/usr/bin/lynx         \
                --with-vgrind=/usr/bin/vgrind        \
                --with-grap=/usr/bin/grap            \
                --with-systemdtmpfilesdir=           \
                --with-systemdsystemunitdir=
    return
}

make_install() {
    make
    make check
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

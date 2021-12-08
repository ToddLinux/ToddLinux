# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf kbd-2.4.0.tar.xz
    cd kbd-2.4.0
    return
}

configure() {
    sed -i '/RESIZECONS_PROGS=/s/yes/no/' configure
    sed -i 's/resizecons.8 //' docs/man/man8/Makefile.in
    ./configure --prefix=/usr --disable-vlock

    return
}

make_install() {
    make
    make -j1 DESTDIR=$TODD_FAKE_ROOT_DIR install

    mkdir -pv $TODD_FAKE_ROOT_DIR/usr/share/doc/kbd-2.4.0
    cp -R -v docs/doc/* $TODD_FAKE_ROOT_DIR/usr/share/doc/kbd-2.4.0
    return
}

unpack_src && configure && make_install

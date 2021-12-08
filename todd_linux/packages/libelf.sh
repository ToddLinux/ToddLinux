# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf elfutils-0.183.tar.bz2 && \
    cd elfutils-0.183
}

configure() {
    ./configure --prefix=/usr \
        --disable-debuginfod \
        --enable-libdebuginfod=dummy \
        --libdir=/lib

    return
}

make_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/usr/lib/pkgconfig

    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 -C libelf install

    install -vm644 config/libelf.pc $TODD_FAKE_ROOT_DIR/usr/lib/pkgconfig
    rm $TODD_FAKE_ROOT_DIR/lib/libelf.a

    return
}

unpack_src && configure && make_install

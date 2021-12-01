# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf zlib-1.2.11.tar.xz
    cd zlib-1.2.11
    return
}

configure() {
    ./configure --prefix=/usr
    return
}

make_install() {
    make
    make check
    make -j1 DESTDIR=$TODD_FAKE_ROOT_DIR install
    return
}

post_install() {
    mkdir $TODD_FAKE_ROOT_DIR/lib
    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/libz.so.* $TODD_FAKE_ROOT_DIR/lib
    ln -sfv ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/libz.so) $TODD_FAKE_ROOT_DIR/usr/lib/libz.so

    rm -fv $TODD_FAKE_ROOT_DIR/usr/lib/libz.a
}

unpack_src && configure && make_install && post_install

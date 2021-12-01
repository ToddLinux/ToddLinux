# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf zstd-1.4.8.tar.gz
    cd zstd-1.4.8
}

make_install() {
    make
    make check
    make prefix=/usr DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

post_install() {
    mkdir $TODD_FAKE_ROOT_DIR/lib
    rm -v $TODD_FAKE_ROOT_DIR/usr/lib/libzstd.a
    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/libzstd.so.* $TODD_FAKE_ROOT_DIR/lib
    ln -sfv ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/libzstd.so) $TODD_FAKE_ROOT_DIR/usr/lib/libzstd.so
}

unpack_src && make_install && post_install

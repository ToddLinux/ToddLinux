#!/bin/bash
# See LICENSE for license details.
set -euo pipefail

unpack_src() {
    tar xf expect5.45.4.tar.gz
    cd expect5.45.4
    return
}

configure() {
    ./configure --prefix=/usr \
        --with-tcl=/usr/lib \
        --enable-shared \
        --mandir=/usr/share/man \
        --with-tclinclude=/usr/include
    return
}

make_install() {
    make && \
    make test && \
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    ln -svf expect5.45.4/libexpect5.45.4.so $TODD_FAKE_ROOT_DIR/usr/lib/libexpect5.45.4.so
}

unpack_src && configure && make_install


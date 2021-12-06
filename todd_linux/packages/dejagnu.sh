#!/bin/bash
# See LICENSE for license details.
set -euo pipefail

unpack_src() {
    tar xf dejagnu-1.6.2.tar.gz
    cd dejagnu-1.6.2
    return
}

configure() {
    ./configure --prefix=/usr
    makeinfo --html --no-split -o doc/dejagnu.html doc/dejagnu.texi
    makeinfo --plaintext -o doc/dejagnu.txt doc/dejagnu.texi
    return
}

make_install() {
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    install -v -dm755 $TODD_FAKE_ROOT_DIR/usr/share/doc/dejagnu-1.6.2
    install -v -m644 doc/dejagnu.{html,txt} $TODD_FAKE_ROOT_DIR/usr/share/doc/dejagnu-1.6.2
    make check
}

unpack_src && configure && make_install


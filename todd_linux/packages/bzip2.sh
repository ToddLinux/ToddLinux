# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf bzip2-1.0.8.tar.gz
    cd bzip2-1.0.8
    return
}

configure() {
    patch -Np1 -i ../bzip2-1.0.8-install_docs-1.patch
    sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
    sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile
    return
}

make_install() {
    make -f Makefile-libbz2_so
    make clean
    make
    make PREFIX=/usr DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

post_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/{lib,bin,usr/lib}
    cp -v bzip2-shared $TODD_FAKE_ROOT_DIR/bin/bzip2
    cp -av libbz2.so* $TODD_FAKE_ROOT_DIR/lib
    ln -sv ../../lib/libbz2.so.1.0 $TODD_FAKE_ROOT_DIR/usr/lib/libbz2.so
    rm -v /usr/bin/{bunzip2,bzcat,bzip2}
    ln -sv bzip2 $TODD_FAKE_ROOT_DIR/bin/bunzip2
    ln -sv bzip2 $TODD_FAKE_ROOT_DIR/bin/bzcat

    rm -fv $TODD_FAKE_ROOT_DIR/usr/lib/libbz2.a
}

unpack_src && configure && make_install && post_install

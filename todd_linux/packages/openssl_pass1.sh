# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf openssl-1.1.1j.tar.gz
    cd openssl-1.1.1j
    return
}

configure() {
    ./config --prefix=/usr \
        --openssldir=/etc/ssl \
        --libdir=lib \
        shared \
        zlib-dynamic
}

make_install() {
    make
    
    sed -i '/INSTALL_LIBS/s/libcrypto.a libssl.a//' Makefile
    make -j1 MANSUFFIX=ssl DESTDIR=$TODD_FAKE_ROOT_DIR install

    mv -v $TODD_FAKE_ROOT_DIR/usr/share/doc/openssl $TODD_FAKE_ROOT_DIR/usr/share/doc/openssl-1.1.1j
    cp -vfr doc/* $TODD_FAKE_ROOT_DIR/usr/share/doc/openssl-1.1.1j

    return
}

unpack_src && configure && make_install

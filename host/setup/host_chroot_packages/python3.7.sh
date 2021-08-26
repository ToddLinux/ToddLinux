# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf Python-3.7.11.tar.xz
    cd Python-3.7.11
    return
}

configure() {
    sed -i 's/#zlib/zlib' Modules/Setup
    ./configure --prefix=/usr   \
                --enable-shared \
                --without-ensurepip \
                --with-zlib=/usr/include
    return
}

make_install() {
    make
    make -j1 DESTDIR=$LFS install
    return
}

unpack_src && configure && make_install

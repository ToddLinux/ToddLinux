# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf Python-3.9.2.tar.xz
    cd Python-3.9.2
    return
}

configure() {
    ./configure --prefix=/usr   \
                --enable-shared \
                --without-ensurepip
    return
}

make_install() {
    make
    make -j1 DESTDIR=$LFS install
    return
}

unpack_src && configure && make_install

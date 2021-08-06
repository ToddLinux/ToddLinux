#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf patch-2.7.6.tar.xz
    cd patch-2.7.6
    return
}

configure() {
    ./configure --prefix=/usr   \
                --host=$LFS_TGT \
                --build=$(build-aux/config.guess)
    return
}

make_install() {
    make && make DESTDIR=$LFS install
    return
}

unpack_src && configure && make_install

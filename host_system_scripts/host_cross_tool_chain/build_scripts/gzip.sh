#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gzip-1.10.tar.xz
    cd gzip-1.10
    return
}

configure() {
    ./configure --prefix=/usr \
                --host=$LFS_TGT
    return
}

make_install() {
    make && make DESTDIR=$LFS install
    return
}

post_install() {
    mv -v $LFS/usr/bin/gzip $LFS/bin
    return
}

unpack_src && configure && make_install && post_install

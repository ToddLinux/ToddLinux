#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gawk-5.1.0.tar.xz && cd gawk-5.1.0
    return
}

configure() {
    sed -i 's/extras//' Makefile.in && \
    ./configure --prefix=/usr \
        --host=$LFS_TGT \
        --build=$(./config.guess)
    return
}

make_install() {
    make && make DESTDIR=$LFS install
}

unpack_src && configure && make_install
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf bash-5.1.tar.gz
    cd bash-5.1
    return
}

configure() {
    ./configure --prefix=/usr                   \
                --build=$(support/config.guess) \
                --host=$LFS_TGT                 \
                --without-bash-malloc
    return
}

make_install() {
    make && make DESTDIR=$LFS install
    return
}

post_install() {
    mv $LFS/usr/bin/bash $LFS/bin/bash
    ln -sv bash $LFS/bin/sh
    return
}

unpack_src && configure && make_install && post_install

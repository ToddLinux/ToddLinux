# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf binutils-2.36.1.tar.xz && \
    cd binutils-2.36.1 && \
    sed -i '/@\tincremental_copy/d' gold/testsuite/Makefile.in && \
    mkdir build && \
    cd build
    return
}

configure() {
    ../configure --prefix=/usr \
        --enable-gold \
        --enable-ld=default \
        --enable-plugins \
        --enable-shared \
        --disable-werror \
        --enable-64-bit-bfd \
        --with-system-zlib
    return
}

make_install() {
    # https://sourceware.org/bugzilla/show_bug.cgi?id=27482
    make tooldir=/usr && \
    make tooldir=$TODD_FAKE_ROOT_DIR/usr -j1 install && \
    rm -fv $TODD_FAKE_ROOT_DIR/usr/lib/lib{bfd,ctf,ctf-nobfd,opcodes}.a
    return
}

unpack_src && configure && make_install

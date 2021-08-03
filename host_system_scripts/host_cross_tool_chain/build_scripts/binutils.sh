#!/bin/sh

unpack_src() {
    tar xf binutils-2.36.1.tar.xz && cd binutils-2.36.1 && mkdir build && cd build
    return
}

configure() {
    echo $PWD
    ../configure --prefix=$LFS/tools \
        --with-sysroot=$LFS \
        --target=$LFS_TGT \
        --disable-nls \
        --disable-werror
    return
}

make_install() {
    make && make install
    return
}

unpack_src && configure && make_install
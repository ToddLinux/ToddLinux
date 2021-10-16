# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf binutils-2.36.1.tar.xz && cd binutils-2.36.1 && mkdir build && cd build
    return
}

configure() {
    ../configure \
        --prefix=/usr \
        --build=$(../config.guess) \
        --host=$LFS_TGT \
        --disable-nls \
        --enable-shared \
        --disable-werror \
        --enable-64-bit-bfd
    return
}

make_install() {
    # https://sourceware.org/bugzilla/show_bug.cgi?id=27482
    make && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install && install -vm755 $TODD_BUILD_DIR/binutils-2.36.1/build/libctf/.libs/libctf.so.0.0.0 $TODD_FAKE_ROOT_DIR/usr/lib
    return
}

unpack_src && configure && make_install

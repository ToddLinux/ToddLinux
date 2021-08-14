# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    rm -r gcc-10.2.0 2>/dev/null
    tar xf gcc-10.2.0.tar.xz && cd gcc-10.2.0 && \
    mkdir build && cd build
    return
}

configure() {
    ../libstdc++-v3/configure \
        --host=$LFS_TGT \
        --build=$(../config.guess) \
        --prefix=/usr \
        --disable-multilib \
        --disable-nls \
        --disable-libstdcxx-pch \
        --with-gxx-include-dir=/tools/$LFS_TGT/include/c++/10.2.0
    return
}

make_install() {
    make && make DESTDIR=$LFS install
    return
}

unpack_src && configure && make_install
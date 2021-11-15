# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    rm -r gcc-10.2.0 2>/dev/null
    tar xf gcc-10.2.0.tar.xz && cd gcc-10.2.0
    return
}

configure() {
    ln -s gthr-posix.h libgcc/gthr-default.h && \
    mkdir build && cd build && \
    ../libstdc++-v3/configure \
        CXXFLAGS="-g -O2 -D_GNU_SOURCE" \
        --prefix=/usr \
        --disable-multilib \
        --disable-nls \
        --host=$LFS_TGT \
        --disable-libstdcxx-pch
    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

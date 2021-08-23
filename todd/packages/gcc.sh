# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    rm -r gcc-10.2.0 2>/dev/null
    tar xf gcc-10.2.0.tar.xz && cd gcc-10.2.0 && \
        tar -xf ../mpfr-4.1.0.tar.xz && mv mpfr-4.1.0 mpfr && \
        tar -xf ../gmp-6.2.1.tar.xz && mv gmp-6.2.1 gmp && \
        tar -xf ../mpc-1.2.1.tar.gz && mv mpc-1.2.1 mpc && \
        sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64 && \
        mkdir build && cd build
    return
}

configure() {
    ../configure \
        --target=$LFS_TGT \
        --prefix=$LFS/tools \
        --with-glibc-version=2.11 \
        --with-sysroot=$LFS \
        --with-newlib \
        --without-headers \
        --enable-initfini-array \
        --disable-nls \
        --disable-shared \
        --disable-multilib \
        --disable-decimal-float \
        --disable-threads \
        --disable-libatomic \
        --disable-libgomp \
        --disable-libquadmath \
        --disable-libssp \
        --disable-libvtv \
        --disable-libstdcxx \
        --enable-languages=c,c++
    return
}

make_install() {
    make && make -j1 install
    return
}

post_install() {
    cd .. && cat gcc/limitx.h gcc/glimits.h gcc/limity.h > `dirname $($LFS/tools/bin/${LFS_TGT}-gcc -print-libgcc-file-name)`/install-tools/include/limits.h
    return
}

unpack_src && configure && make_install && post_install

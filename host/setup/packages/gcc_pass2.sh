# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gcc-10.2.0.tar.xz && cd gcc-10.2.0 && \
        tar -xf ../mpfr-4.1.0.tar.xz && mv mpfr-4.1.0 mpfr && \
        tar -xf ../gmp-6.2.1.tar.xz && mv gmp-6.2.1 gmp && \
        tar -xf ../mpc-1.2.1.tar.gz && mv mpc-1.2.1 mpc && \
        sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64
    return
}

configure() {
    mkdir build && cd build && \
    mkdir -pv $LFS_TGT/libgcc && \
    ln -s ../../../libgcc/gthr-posix.h $LFS_TGT/libgcc/gthr-default.h && \
    ../configure \
        --build=$(../config.guess) \
        --host=$LFS_TGT \
        --prefix=/usr \
        CC_FOR_TARGET=$LFS_TGT-gcc \
        --with-build-sysroot=$LFS \
        --enable-initfini-array \
        --disable-nls \
        --disable-multilib \
        --disable-decimal-float \
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
    make && make -j1 install && ln -sv gcc $TODD_FAKE_ROOT_DIR/usr/bin/cc
    return
}

unpack_src && configure && make_install

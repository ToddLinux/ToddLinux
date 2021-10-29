# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    rm -rf glibc-2.33 2>/dev/null
    tar xf glibc-2.33.tar.xz && cd glibc-2.33
    return
}

create_links() {
    mkdir $TODD_FAKE_ROOT_DIR/lib64 &&\
    ln -sfv $TODD_FAKE_ROOT_DIR/lib/ld-linux-x86-64.so.2 $TODD_FAKE_ROOT_DIR/lib64 &&\
    ln -sfv $TODD_FAKE_ROOT_DIR/lib/ld-linux-x86-64.so.2 $TODD_FAKE_ROOT_DIR/lib64/ld-lsb-x86-64.so.3
    return
}

patch_src() {
    patch -Np1 -i ../glibc-2.33-fhs-1.patch
    return
}

configure() {
    mkdir build && cd build && \
    ../configure \
        --prefix=/usr \
        --host=$LFS_TGT \
        --build=$(../scripts/config.guess) \
        --enable-kernel=3.2 \
        --with-headers=$LFS/usr/include \
        libc_cv_slibdir=/lib
}

make_install() {
    make -j1 && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
}

# TODO: FIX THIS
# grep output should be "[Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]""
# test_toolchain() {
#     echo 'int main(){}' > dummy.c && $LFS/tools/bin/$LFS_TGT-gcc dummy.c && readelf -l a.out | grep '/ld-linux'
#     return
# }

# TODO: this is not tracked
finalize_headers() {
    $LFS/tools/libexec/gcc/$LFS_TGT/10.2.0/install-tools/mkheaders
    return
}

unpack_src && patch_src && configure && make_install && create_links && finalize_headers

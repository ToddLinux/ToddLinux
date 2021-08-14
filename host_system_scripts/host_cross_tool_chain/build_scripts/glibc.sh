# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    rm -rf glibc-2.33 2>/dev/null
    tar xf glibc-2.33.tar.xz && cd glibc-2.33
    return
}

create_links() {
    ln -sfv ../lib/ld-linux-x86-64.so.2 $LFS/lib64 && ln -sfv ../lib/ld-linux-x86-64.so.2 $LFS/lib64/ld-lsb-x86-64.so.3
    return
}

patch_src() {
    echo $PWD
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
    make -j1 && make DESTDIR=$LFS install
}

# TODO: FIX THIS
# grep output should be "[Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]""
test_toolchain() {
    echo 'int main(){}' > dummy.c && $LFS/tools/bin/$LFS_TGT-gcc dummy.c && readelf -l a.out | grep '/ld-linux'
    return
}

finalize_headers() {
    $LFS/tools/libexec/gcc/$LFS_TGT/10.2.0/install-tools/mkheaders
    return
}

unpack_src && patch_src && configure && make_install && create_links && test_toolchain && finalize_headers

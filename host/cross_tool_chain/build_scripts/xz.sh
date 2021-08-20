# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf xz-5.2.5.tar.xz
    cd xz-5.2.5
    return
}

configure() {
    ./configure --prefix=/usr                     \
                --host=$LFS_TGT                   \
                --build=$(build-aux/config.guess) \
                --disable-static                  \
                --docdir=/usr/share/doc/xz-5.2.5
    return
}

make_install() {
    make && make -j1 DESTDIR=$LFS install
    return
}

post_install() {
    mv -v $LFS/usr/bin/{lzma,unlzma,lzcat,xz,unxz,xzcat}  $LFS/bin
    mv -v $LFS/usr/lib/liblzma.so.*                       $LFS/lib
    ln -svf ../../lib/$(readlink $LFS/usr/lib/liblzma.so) $LFS/usr/lib/liblzma.so
    return
}

unpack_src && configure && make_install && post_install

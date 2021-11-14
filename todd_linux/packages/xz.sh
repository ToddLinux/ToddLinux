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
    make && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

post_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/{bin,lib}
    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/{lzma,unlzma,lzcat,xz,unxz,xzcat}  $TODD_FAKE_ROOT_DIR/bin
    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/liblzma.so.*                       $TODD_FAKE_ROOT_DIR/lib
    ln -svf ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/liblzma.so) $TODD_FAKE_ROOT_DIR/usr/lib/liblzma.so
    return
}

unpack_src && configure && make_install && post_install

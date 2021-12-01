# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf xz-5.2.5.tar.xz
    cd xz-5.2.5
}

configure() {
    ./configure --prefix=/usr    \
                --disable-static \
                --docdir=/usr/share/doc/xz-5.2.5
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
}

post_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/{bin,lib}
    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/{lzma,unlzma,lzcat,xz,unxz,xzcat} $TODD_FAKE_ROOT_DIR/bin
    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/liblzma.so.* $TODD_FAKE_ROOT_DIR/lib
    ln -svf ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/liblzma.so) $TODD_FAKE_ROOT_DIR/usr/lib/liblzma.so
}

unpack_src && configure && make_install && post_install

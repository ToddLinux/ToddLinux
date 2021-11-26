# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gzip-1.10.tar.xz
    cd gzip-1.10
    return
}

configure() {
    ./configure --prefix=/usr \
                --host=$LFS_TGT
    return
}

make_install() {
    make && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

post_install() {
    mkdir $TODD_FAKE_ROOT_DIR/bin
    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/gzip $TODD_FAKE_ROOT_DIR/bin/gzip
    return
}

unpack_src && configure && make_install && post_install

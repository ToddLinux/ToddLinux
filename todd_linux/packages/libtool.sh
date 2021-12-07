# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf libtool-2.4.6.tar.xz
    cd libtool-2.4.6
    return
}

configure() {
    ./configure --prefix=/usr
    return
}

make_install() {
    make 
    
    make TESTSUITEFLAGS=-j$(nproc) check

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

post_install() {
    rm -fv $TODD_FAKE_ROOT_DIR/usr/lib/libltdl.a
    return
}

unpack_src && configure && make_install && post_install

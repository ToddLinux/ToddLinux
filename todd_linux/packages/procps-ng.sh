# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf procps-ng-3.3.17.tar.xz && \
    cd procps-3.3.17
    return
}

configure() {
    ./configure --prefix=/usr \
        --exec-prefix= \
        --libdir=/usr/lib \
        --docdir=/usr/share/doc/procps-ng-3.3.17 \
        --disable-static \
        --disable-kill

    return
}

make_install() {
    mkdir $TODD_FAKE_ROOT_DIR/lib
    make

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/libprocps.so.* $TODD_FAKE_ROOT_DIR/lib
    ln -sfv ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/libprocps.so) $TODD_FAKE_ROOT_DIR/usr/lib/libprocps.so

    return
}

unpack_src && configure && make_install

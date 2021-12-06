# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf libcap-2.48.tar.xz && \
    cd libcap-2.48
    return
}

configure() {
    sed -i '/install -m.*STA/d' libcap/Makefile

    return
}

make_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/{lib,usr/lib}
    make prefix=/usr lib=lib
    make test
    make DESTDIR=$TODD_FAKE_ROOT_DIR prefix=/usr lib=lib install

    for libname in cap psx; do
        mv -v $TODD_FAKE_ROOT_DIR/usr/lib/lib${libname}.so.* $TODD_FAKE_ROOT_DIR/lib
        ln -sfv ../../lib/lib${libname}.so.2 $TODD_FAKE_ROOT_DIR/usr/lib/lib${libname}.so
        chmod -v 755 $TODD_FAKE_ROOT_DIR/lib/lib${libname}.so.2.48
    done
}

unpack_src && configure && make_install

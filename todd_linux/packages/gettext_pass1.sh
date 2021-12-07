# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gettext-0.21.tar.xz && \
    cd gettext-0.21
}

configure() {
    ./configure --prefix=/usr \
        --disable-static \
        --docdir=/usr/share/doc/gettext-0.21

    return
}

make_install() {
    make
    make check
    
    make DESTDIR=$TODD_FAKE_ROOT_DIR install
    chmod -v 0755 $TODD_FAKE_ROOT_DIR/usr/lib/preloadable_libintl.so
}

unpack_src && configure && make_install

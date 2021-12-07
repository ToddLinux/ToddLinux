# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf intltool-0.51.0.tar.gz && \
    cd intltool-0.51.0
}

configure() {
    sed -i 's:\\\${:\\\$\\{:' intltool-update.in
    ./configure --prefix=/usr

    return
}

make_install() {
    make

    make check

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    install -v -Dm644 doc/I18N-HOWTO $TODD_FAKE_ROOT_DIR/usr/share/doc/intltool-0.51.0/I18N-HOWTO

    return
}

unpack_src && configure && make_install

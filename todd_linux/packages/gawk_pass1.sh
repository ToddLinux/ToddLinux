# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gawk-5.1.0.tar.xz && cd gawk-5.1.0
    return
}

configure() {
    sed -i 's/extras//' Makefile.in && \
    ./configure --prefix=/usr

    return
}

make_install() {
    make && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    mkdir -pv $TODD_FAKE_ROOT_DIR/usr/share/doc/gawk-5.1.0
    cp -v doc/{awkforai.txt,*.{eps,pdf,jpg}} $TODD_FAKE_ROOT_DIR/usr/share/doc/gawk-5.1.0
}

unpack_src && configure && make_install

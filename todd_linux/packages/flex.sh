# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf flex-2.6.4.tar.gz
    cd flex-2.6.4
    return
}

configure() {
    ./configure --prefix=/usr \
                --docdir=/usr/share/doc/flex-2.6.4 \
                --disable-static
}

make_install() {
    make
    make check
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

post_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/usr/bin
    ln -sv flex $TODD_FAKE_ROOT_DIR/usr/bin/lex
}

unpack_src && configure && make_install && post_install

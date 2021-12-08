# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf Python-3.7.11.tar.xz
    cd Python-3.7.11
    return
}

configure() {
    ./configure --prefix=/usr \
        --enable-shared \
        --with-system-expat \
        --with-system-ffi \
        --with-ensurepip=yes

    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    install -v -dm755 $TODD_FAKE_ROOT_DIR/usr/share/doc/python-3.9.2/html

    tar --strip-components=1 \
        --no-same-owner \
        --no-same-permissions \
        -C $TODD_FAKE_ROOT_DIR/usr/share/doc/python-3.9.2/html \
        -xvf ../python-3.7.11-docs-html.tar.bz2

    return
}

unpack_src && configure && make_install

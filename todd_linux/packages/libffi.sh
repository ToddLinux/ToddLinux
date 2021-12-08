# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf libffi-3.3.tar.gz && \
    cd libffi-3.3
}

configure() {
    ./configure --prefix=/usr --disable-static --with-gcc-arch=native

    return
}

make_install() {

    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    return
}

unpack_src && configure && make_install

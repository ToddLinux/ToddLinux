# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf zlib-1.2.11.tar.xz
    cd zlib-1.2.11
    return
}

configure() {
    ./configure --prefix=/usr
    return
}

make_install() {
    make
    make -j1 DESTDIR=$TODD_FAKE_ROOT_DIR install
    return
}

unpack_src && configure && make_install

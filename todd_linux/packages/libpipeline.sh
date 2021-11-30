# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf libpipeline-1.5.3.tar.gz
    cd libpipeline-1.5.3
    return
}

configure() {
    ./configure --prefix=/usr
    return
}

make_install() {
    make
    make check
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

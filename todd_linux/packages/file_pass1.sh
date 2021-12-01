# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf file-5.39.tar.gz
    cd file-5.39
}

configure() {
    ./configure --prefix=/usr
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
}

unpack_src && configure && make_install

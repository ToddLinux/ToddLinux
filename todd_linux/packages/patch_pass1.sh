# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf patch-2.7.6.tar.xz
    cd patch-2.7.6
    return
}

configure() {
    ./configure --prefix=/usr

    return
}

make_install() {
    make && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

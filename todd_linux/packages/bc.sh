# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf bc-3.3.0.tar.xz
    cd bc-3.3.0
    return
}

configure() {
    PREFIX=/usr CC=gcc ./configure.sh -G -O3
    return
}

make_install() {
    make
    make test
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

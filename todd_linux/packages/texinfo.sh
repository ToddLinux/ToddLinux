# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf texinfo-6.7.tar.xz && \
    cd texinfo-6.7
    return
}

configure() {
    ./configure --prefix=/usr
    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

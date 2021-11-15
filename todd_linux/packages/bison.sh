# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf bison-3.7.5.tar.xz && \
    cd bison-3.7.5
    return
}

configure() {
    ./configure --prefix=/usr \
                --docdir=/usr/share/doc/bison-3.7.5
    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

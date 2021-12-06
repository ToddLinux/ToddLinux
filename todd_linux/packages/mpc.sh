# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf mpc-1.2.1.tar.gz && \
    cd mpc-1.2.1
    return
}

configure() {
    ./configure --prefix=/usr \
        --disable-static \
        --docdir=/usr/share/doc/mpc-1.2.1
    return
}

make_install() {
    make && \
    make html && \
    make check

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install && \
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install-html
}

unpack_src && configure && make_install

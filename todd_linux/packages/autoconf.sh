# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf autoconf-2.71.tar.xz && \
    cd autoconf-2.71
}

configure() {
    ./configure --prefix=/usr

    return
}

make_install() {
    make

    # make check

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    return
}

unpack_src && configure && make_install

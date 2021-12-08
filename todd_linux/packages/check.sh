# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf check-0.15.2.tar.gz
    cd check-0.15.2
    return
}

configure() {
    ./configure --prefix=/usr --disable-static

    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR docdir=/usr/share/doc/check-0.15.2 -j1 install

    return
}

unpack_src && configure && make_install

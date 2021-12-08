# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf groff-1.22.4.tar.gz && cd groff-1.22.4
    return
}

configure() {
    PAGE=A4 ./configure --prefix=/usr
    return
}

make_install() {
    make -j1 && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
}

unpack_src && configure && make_install

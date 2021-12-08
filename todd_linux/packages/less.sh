# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf less-563.tar.gz
    cd less-563
    return
}

configure() {
    ./configure --prefix=/usr --sysconfdir=/etc

    return
}

make_install() {
    make && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

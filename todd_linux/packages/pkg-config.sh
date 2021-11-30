# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf pkg-config-0.29.2.tar.gz
    cd pkg-config-0.29.2
    return
}

configure() {
    ./configure --prefix=/usr              \
                --with-internal-glib       \
                --disable-host-tool        \
                --docdir=/usr/share/doc/pkg-config-0.29.2
    return
}

make_install() {
    make
    make check
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

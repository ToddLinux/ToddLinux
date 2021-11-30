# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf openssl-1.1.1j.tar.gz
    cd openssl-1.1.1j
    return
}

configure() {
    ./config --prefix=/usr         \
             --openssldir=/etc/ssl \
             --libdir=lib          \
             shared                \
             zlib-dynamic
    ./config
}

make_install() {
    make
    # make test
    make -j1 DESTDIR=$TODD_FAKE_ROOT_DIR install
    return
}

unpack_src && configure && make_install

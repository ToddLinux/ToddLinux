# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf OpenSSL_1_1_1l.tar.gz
    cd openssl-OpenSSL_1_1_1l
    return
}

configure() {
    # ./config --prefix=/usr/lib/ssl \
    #          --openssldir=/usr/lib/ssl
    ./config
}

make_install() {
    make
    make -j1 DESTDIR=$TODD_FAKE_ROOT_DIR install
    return
}

unpack_src && configure && make_install

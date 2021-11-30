# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf Python-3.7.11.tar.xz
    cd Python-3.7.11
    return
}

configure() {
    # sed -i 's/#zlib/zlib' Modules/Setup.dist
    sed -i "338 s/^#//" Modules/Setup.dist
    sed -i "207 s/^#//" Modules/Setup.dist
    sed -i "211,214 s/^#//" Modules/Setup.dist
    # sed -i "211 s:^SSL=/usr/local/ssl:SSL=/usr/lib/openssl:" Modules/Setup.dist
    ./configure --prefix=/usr       \
                --enable-shared     \
                --without-ensurepip \
                --with-zlib=/usr/include \
                LDFLAGS="-Wl,-rpath /usr/local/lib"

    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

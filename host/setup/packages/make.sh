# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf make-4.3.tar.gz && cd make-4.3
    return
}

configure() {
    ./configure --prefix=/usr \
        --without-guile \
        --host=$LFS_TGT \
        --build=$(build-aux/config.guess)
    return
}

make_install() {
    make && make -j1 install
    return
}

unpack_src && configure && make_install

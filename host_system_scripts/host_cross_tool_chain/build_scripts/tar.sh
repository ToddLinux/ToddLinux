# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf tar-1.34.tar.xz
    cd tar-1.34
    return
}

configure() {
    ./configure --prefix=/usr                     \
                --host=$LFS_TGT                   \
                --build=$(build-aux/config.guess) \
                --bindir=/bin
    return
}

make_install() {
    make && make DESTDIR=$LFS install
    return
}

unpack_src && configure && make_install

# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf sed-4.8.tar.xz && cd sed-4.8
    return
}

configure() {
    ./configure --prefix=/usr \
        --host=$LFS_TGT \
        --bindir=/bin
    return
}

make_install() {
    make && make DESTDIR=$LFS install
    return
}

unpack_src && configure && make_install
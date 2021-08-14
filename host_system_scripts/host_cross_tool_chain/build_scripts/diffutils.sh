# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf diffutils-3.7.tar.xz
    cd diffutils-3.7
    return
}

configure() {
    ./configure --prefix=/usr \
                --host=$LFS_TGT
    return
}

make_install() {
    make && make DESTDIR=$LFS install
    return
}

unpack_src && configure && make_install

# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf findutils-4.8.0.tar.xz
    cd findutils-4.8.0
    return
}

configure() {
    ./configure --prefix=/usr   \
                --host=$LFS_TGT \
                --build=$(build-aux/config.guess)
    return
}

make_install() {
    make && make DESTDIR=$LFS install
    return
}

post_install() {
    mv -v $LFS/usr/bin/find $LFS/bin
    sed -i 's|find:=${BINDIR}|find:=/bin|' $LFS/usr/bin/updatedb
    return
}

unpack_src && configure && make_install && post_install

# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf ncurses-6.2.tar.gz && cd ncurses-6.2
    return
}

configure() {
    sed -i s/mawk// configure && \
    mkdir build && \
    pushd build && \
    ../configure && \
    make -C include && \
    make -C progs tic && \
    popd && \
    ./configure --prefix=/usr \
        --host=$LFS_TGT \
        --build=$(./config.guess) \
        --mandir=/usr/share/man \
        --with-manpage-format=normal \
        --with-shared \
        --without-debug \
        --without-ada \
        --without-normal \
        --enable-widec
    return
}

make_install() {
    make && \
    make -j1 DESTDIR=$LFS TIC_PATH=$(pwd)/build/progs/tic install && \
    echo "INPUT(-lncursesw)" > $LFS/usr/lib/libncurses.so && \
    mv -v $LFS/usr/lib/libncursesw.so.6* $LFS/lib && \
    ln -sfv ../../lib/$(readlink $LFS/usr/lib/libncursesw.so) $LFS/usr/lib/libncursesw.so
    return 
}

unpack_src && configure && make_install
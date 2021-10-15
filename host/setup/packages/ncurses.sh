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
    make -j1 TIC_PATH=$(pwd)/build/progs/tic install && \
    echo "INPUT(-lncursesw)" > $TODD_FAKE_ROOT_DIR/usr/lib/libncurses.so && \
    mkdir -p $TODD_FAKE_ROOT_DIR/lib && \
    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/libncursesw.so.6* $TODD_FAKE_ROOT_DIR/lib && \
    ln -sfv ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/libncursesw.so) $TODD_FAKE_ROOT_DIR/usr/lib/libncursesw.so
    return 
}

unpack_src && configure && make_install

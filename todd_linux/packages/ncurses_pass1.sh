# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf ncurses-6.2.tar.gz && \
    cd ncurses-6.2
    return
}

configure() {
    ./configure --prefix=/usr \
        --mandir=/usr/share/man \
        --with-shared \
        --without-debug \
        --without-normal \
        --enable-pc-files \
        --enable-widec
    return
}

make_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/{lib,usr/lib}
    make && \
    make -j1 DESTDIR=$TODD_FAKE_ROOT_DIR install

    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/libncursesw.so.6* $TODD_FAKE_ROOT_DIR/lib
    ln -sfv ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/libncursesw.so) $TODD_FAKE_ROOT_DIR/usr/lib/libncursesw.so

    for lib in ncurses form panel menu ; do
        rm -vf $TODD_FAKE_ROOT_DIR/usr/lib/lib${lib}.so
        echo "INPUT(-l${lib}w)" > $TODD_FAKE_ROOT_DIR/usr/lib/lib${lib}.so
        ln -sfv ${lib}w.pc $TODD_FAKE_ROOT_DIR/usr/lib/pkgconfig/${lib}.pc
    done

    rm -vf $TODD_FAKE_ROOT_DIR/usr/lib/libcursesw.so
    echo "INPUT(-lncursesw)" > $TODD_FAKE_ROOT_DIR/usr/lib/libcursesw.so
    ln -sfv libncurses.so $TODD_FAKE_ROOT_DIR/usr/lib/libcurses.so

    rm -fv $TODD_FAKE_ROOT_DIR/usr/lib/libncurses++w.a

    mkdir -pv $TODD_FAKE_ROOT_DIR/usr/share/doc/ncurses-6.2
    cp -v -R doc/* $TODD_FAKE_ROOT_DIR/usr/share/doc/ncurses-6.2
}

unpack_src && configure && make_install

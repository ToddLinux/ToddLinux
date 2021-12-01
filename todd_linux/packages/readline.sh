# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf readline-8.1.tar.gz
    cd readline-8.1
}

configure() {
    sed -i '/MV.*old/d' Makefile.in
    sed -i '/{OLDSUFF}/c:' support/shlib-install
    ./configure --prefix=/usr    \
                --disable-static \
                --with-curses    \
                --docdir=/usr/share/doc/readline-8.1
}

make_install() {
    make SHLIB_LIBS="-lncursesw"
    make SHLIB_LIBS="-lncursesw" DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
}

post_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/lib $TODD_FAKE_ROOT_DIR/usr/lib $TODD_FAKE_ROOT_DIR/usr/share/doc

    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/lib{readline,history}.so.* $TODD_FAKE_ROOT_DIR/lib
    ln -sfv ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/libreadline.so) $TODD_FAKE_ROOT_DIR/usr/lib/libreadline.so
    ln -sfv ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/libhistory.so) $TODD_FAKE_ROOT_DIR/usr/lib/libhistory.so

    install -v -m644 doc/*.{ps,pdf,html,dvi} $TODD_FAKE_ROOT_DIR/usr/share/doc/readline-8.1
}

unpack_src && configure && make_install && post_install

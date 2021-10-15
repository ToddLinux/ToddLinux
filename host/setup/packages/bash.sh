# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf bash-5.1.tar.gz
    cd bash-5.1
    return
}

configure() {
    ./configure --prefix=/usr                   \
                --build=$(support/config.guess) \
                --host=$LFS_TGT                 \
                --without-bash-malloc
    return
}

make_install() {
    # is DESTDIR overwritten somehow in bash Makefile?
    # BASH EXPLAIN ??????????
    make && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

post_install() {
    mkdir $TODD_FAKE_ROOT_DIR/bin
    mv $TODD_FAKE_ROOT_DIR/usr/bin/bash $TODD_FAKE_ROOT_DIR/bin/bash
    ln -sv bash $TODD_FAKE_ROOT_DIR/bin/sh
    return
}

unpack_src && configure && make_install && post_install

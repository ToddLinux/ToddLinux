# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf psmisc-23.4.tar.xz && cd psmisc-23.4
    return
}

configure() {
    ./configure --prefix=/usr
    return
}

make_install() {
    mkdir $TODD_FAKE_ROOT_DIR/bin
    make
    
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/fuser $TODD_FAKE_ROOT_DIR/bin/fuser
    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/killall $TODD_FAKE_ROOT_DIR/bin/killall
    
    return
}

unpack_src && configure && make_install
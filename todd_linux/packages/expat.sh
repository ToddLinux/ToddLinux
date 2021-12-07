# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf expat-2.4.1.tar.xz
    cd expat-2.4.1
    return
}

configure() {
    ./configure --prefix=/usr \
        --disable-static \
        --docdir=/usr/share/doc/expat-2.2.10
    return
}

make_install() {
    make 
    
    make -j1 check

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    install -v -m644 doc/*.{html,png,css} $TODD_FAKE_ROOT_DIR/usr/share/doc/expat-2.2.10
    return
}

unpack_src && configure && make_install

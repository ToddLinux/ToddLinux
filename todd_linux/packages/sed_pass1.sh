# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf sed-4.8.tar.xz && cd sed-4.8
    return
}

configure() {
    ./configure --prefix=/usr --bindir=/bin
    return
}

make_install() {
    make && make html

    chown -Rv tester .
    su tester -c "PATH=$PATH make check"
    
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    install -d -m755 $TODD_FAKE_ROOT_DIR/usr/share/doc/sed-4.8
    install -m644 doc/sed.html $TODD_FAKE_ROOT_DIR/usr/share/doc/sed-4.8

    return
}

unpack_src && configure && make_install
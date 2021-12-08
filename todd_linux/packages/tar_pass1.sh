# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf tar-1.34.tar.xz
    cd tar-1.34
    return
}

configure() {
    FORCE_UNSAFE_CONFIGURE=1 \
    ./configure --prefix=/usr \
        --bindir=/bin
    return
}

make_install() {
    make && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    make -C doc install-html DESTDIR=$TODD_FAKE_ROOT_DIR docdir=/usr/share/doc/tar-1.34
    return
}

unpack_src && configure && make_install

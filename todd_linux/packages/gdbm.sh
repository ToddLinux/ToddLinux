# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gdbm-1.19.tar.gz
    cd gdbm-1.19
    return
}

configure() {
    ./configure --prefix=/usr \
        --disable-static \
        --enable-libgdbm-compat
    return
}

make_install() {
    make 
    
    make check

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

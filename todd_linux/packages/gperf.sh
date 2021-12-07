# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gperf-3.1.tar.gz
    cd gperf-3.1
    return
}

configure() {
    ./configure --prefix=/usr --docdir=/usr/share/doc/gperf-3.1
    return
}

make_install() {
    make 
    
    make -j1 check

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

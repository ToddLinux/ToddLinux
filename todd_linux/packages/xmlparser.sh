# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf XML-Parser-2.46.tar.gz && \
    cd XML-Parser-2.46
}

configure() {
    perl Makefile.PL
    return
}

make_install() {
    make

    make test

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

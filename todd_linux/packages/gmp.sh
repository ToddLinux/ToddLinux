# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gmp-6.2.1.tar.xz && \
    cd gmp-6.2.1
    return
}

configure() {
    cp -v configfsf.guess config.guess
    cp -v configfsf.sub config.sub

    ./configure --prefix=/usr \
        --enable-cxx \
        --disable-static \
        --docdir=/usr/share/doc/gmp-6.2.1
    return
}

make_install() {
    make && \
    make html && \
    make check 2>&1 | tee gmp-check-log
    # TODO: check tests
    # awk '/# PASS:/{total+=$3} ; END{print total}' gmp-check-log

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install && \
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install-html
}

unpack_src && configure && make_install

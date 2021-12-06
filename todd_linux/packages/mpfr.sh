# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf mpfr-4.1.0.tar.xz && \
    cd mpfr-4.1.0
    return
}

configure() {
    ./configure --prefix=/usr \
        --disable-static \
        --enable-thread-safe \
        --docdir=/usr/share/doc/mpfr-4.1.0
    return
}

make_install() {
    make && \
    make html && \
    make check

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install && \
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install-html
}

unpack_src && configure && make_install

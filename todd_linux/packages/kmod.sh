# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf kmod-28.tar.xz && \
    cd kmod-28
}

configure() {
    ./configure --prefix=/usr \
        --bindir=/bin \
        --sysconfdir=/etc \
        --with-rootlibdir=/lib \
        --with-xz \
        --with-zstd \
        --with-zlib
    return
}

make_install() {
    mkdir $TODD_FAKE_ROOT_DIR/sbin


    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    for target in depmod insmod lsmod modinfo modprobe rmmod; do
        ln -sfv ../bin/kmod $TODD_FAKE_ROOT_DIR/sbin/$target
    done
    ln -sfv kmod $TODD_FAKE_ROOT_DIR/bin/lsmod

    return
}

unpack_src && configure && make_install

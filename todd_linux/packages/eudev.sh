# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf eudev-3.2.10.tar.gz && \
    cd eudev-3.2.10
    return
}

configure() {
    ./configure --prefix=/usr \
        --bindir=/sbin \
        --sbindir=/sbin \
        --libdir=/usr/lib \
        --sysconfdir=/etc \
        --libexecdir=/lib \
        --with-rootprefix= \
        --with-rootlibdir=/lib \
        --enable-manpages \
        --disable-static
    return
}

make_install() {
    mkdir -pv $TODD_FAKE_ROOT_DIR/lib/udev/rules.d
    mkdir -pv $TODD_FAKE_ROOT_DIR/etc/udev/rules.d

    make

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    tar -xvf ../udev-lfs-20171102.tar.xz
    make -f udev-lfs-20171102/Makefile.lfs install

    return
}

unpack_src && configure && make_install

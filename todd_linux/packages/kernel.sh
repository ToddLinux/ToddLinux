# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf linux-5.10.17.tar.xz
    cd linux-5.10.17
    return
}

configure() {
    make mrproper
    mv ../default.config .config
    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 modules_install
    return
}

post_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/boot
    mkdir -p $TODD_FAKE_ROOT_DIR/usr/share/doc/linux-5.10.17

    cp -v arch/x86/boot/bzImage $TODD_FAKE_ROOT_DIR/boot/vmlinuz-5.10.17-lfs-10.1
    cp -v System.map $TODD_FAKE_ROOT_DIR/boot/System.map-5.10.17
    cp -v .config $TODD_FAKE_ROOT_DIR/boot/config-5.10.17
    install -d $TODD_FAKE_ROOT_DIR/usr/share/doc/linux-5.10.17
    cp -rv Documentation/* $TODD_FAKE_ROOT_DIR/usr/share/doc/linux-5.10.17
}

unpack_src && configure && make_install && post_install

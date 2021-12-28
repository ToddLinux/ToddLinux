# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf syslinux-6.03.tar.gz
    cd syslinux-6.03
    return
}


make_install() {
    mkdir $TODD_FAKE_ROOT_DIR/boot
    cp -v bios/core/isolinux.bin $TODD_FAKE_ROOT_DIR/boot/isolinux.bin
    cp -v bios/com32/elflink/ldlinux/ldlinux.c32 $TODD_FAKE_ROOT_DIR/boot/ldlinux.c32
    return
}

unpack_src && make_install

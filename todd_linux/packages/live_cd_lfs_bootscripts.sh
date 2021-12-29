# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf lfs-bootscripts-20210201.tar.xz
    cd lfs-bootscripts-20210201
    return
}

make_install() {
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    sed -i 's/log_info_msg "Remounting root file system in read-write mode..."/# Dont remount iso in read-write mode/g' $TODD_FAKE_ROOT_DIR/etc/rc.d/rcS.d/S40mountfs
    sed -i 's/mount --options remount,rw \/ >\/dev\/null/true/g' $TODD_FAKE_ROOT_DIR/etc/rc.d/rcS.d/S40mountfs

    return
}

unpack_src && make_install

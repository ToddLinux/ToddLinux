# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf blfs-bootscripts-20210826.tar.xz
    cd blfs-bootscripts-20210826
    return
}

make_install() {
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install-service-dhcp
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install-service-dhclient
}

unpack_src && make_install

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
    return
}

unpack_src && make_install

# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf man-pages-5.10.tar.xz
    cd man-pages-5.10
    return
}

make_install() {
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && make_install

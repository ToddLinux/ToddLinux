# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf sysvinit-2.98.tar.xz && \
    cd sysvinit-2.98
    return
}

configure() {
    patch -Np1 -i ../sysvinit-2.98-consolidated-1.patch

    return
}

make_install() {
    make
    make ROOT=$TODD_FAKE_ROOT_DIR -j1 install

    return
}

unpack_src && configure && make_install

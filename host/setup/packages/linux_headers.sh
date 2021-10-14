# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    rm linux-5.10.17 2>/dev/null
    tar xf linux-5.10.17.tar.xz && cd linux-5.10.17
    return
}

prepare_headers() {
    make mrproper && make headers && \
        find usr/include -name '.*' -delete && \
        rm usr/include/Makefile && \
        mkdir $TODD_FAKE_ROOT_DIR/usr && \
        cp -rv usr/include $TODD_FAKE_ROOT_DIR/usr
    return
}

unpack_src && prepare_headers

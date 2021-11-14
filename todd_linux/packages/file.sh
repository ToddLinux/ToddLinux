# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf file-5.39.tar.gz && cd file-5.39
    return
}

configure() {
    mkdir build && \
    pushd build && \
        ../configure --disable-bzlib \
        --disable-libseccomp \
        --disable-xzlib \
        --disable-zlib && \
    make && \
    popd && \
    ./configure --prefix=/usr --host=$LFS_TGT --build=$(./config.guess)
    return
}

make_install() {
    make FILE_COMPILE=$(pwd)/build/src/file && \
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    rm -r binutils-2.36.1 2>/dev/null
    tar xf binutils-2.36.1.tar.xz && cd binutils-2.36.1 && mkdir build && cd build
    return
}

configure() {
    ../configure --prefix=$LFS/tools \
        --with-sysroot=$LFS \
        --target=$LFS_TGT \
        --disable-nls \
        --disable-werror
    return
}

make_install() {
    make && make -j1 install
    return
}

unpack_src && configure && make_install

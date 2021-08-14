# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf m4-1.4.18.tar.xz
    cd m4-1.4.18
    return
}

configure() {
    sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
    echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h

    ./configure --prefix=/usr   \
                --host=$LFS_TGT \
                --build=$(build-aux/config.guess)
    return
}

make_install() {
    make
    make DESTDIR=$LFS install
    return
}

unpack_src && configure && make_install

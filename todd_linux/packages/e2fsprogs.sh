# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf e2fsprogs-1.46.1.tar.gz && \
    cd e2fsprogs-1.46.1
    return
}

configure() {
    mkdir -v build
    cd build

    ../configure --prefix=/usr \
        --bindir=/bin \
        --with-root-prefix="" \
        --enable-elf-shlibs \
        --disable-libblkid \
        --disable-libuuid \
        --disable-uuidd \
        --disable-fsck


    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    rm -fv $TODD_FAKE_ROOT_DIR/usr/lib/{libcom_err,libe2p,libext2fs,libss}.a

    gunzip -v $TODD_FAKE_ROOT_DIR/usr/share/info/libext2fs.info.gz
    install-info --dir-file=/usr/share/info/dir $TODD_FAKE_ROOT_DIR/usr/share/info/libext2fs.info

    makeinfo -o doc/com_err.info ../lib/et/com_err.texinfo
    install -v -m644 doc/com_err.info $TODD_FAKE_ROOT_DIR/usr/share/info
    install-info --dir-file=/usr/share/info/dir $TODD_FAKE_ROOT_DIR/usr/share/info/com_err.info

    return
}

unpack_src && configure && make_install

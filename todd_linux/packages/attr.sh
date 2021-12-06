# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf attr-2.4.48.tar.gz && \
    cd attr-2.4.48
    return
}

configure() {
    ./configure --prefix=/usr \
        --bindir=/bin \
        --disable-static \
        --sysconfdir=/etc \
        --docdir=/usr/share/doc/attr-2.4.48

    return
}

make_install() {
    make && \
    make check

    mkdir -p $TODD_FAKE_ROOT_DIR/{lib,usr/lib}
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/libattr.so.* $TODD_FAKE_ROOT_DIR/lib/
    ln -sfv ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/libattr.so) $TODD_FAKE_ROOT_DIR/usr/lib/libattr.so
}

unpack_src && configure && make_install
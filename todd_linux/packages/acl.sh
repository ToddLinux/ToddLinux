# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf acl-2.2.53.tar.gz && \
    cd acl-2.2.53
    return
}

configure() {
    ./configure --prefix=/usr \
        --bindir=/bin \
        --disable-static \
        --libexecdir=/usr/lib \
        --docdir=/usr/share/doc/acl-2.2.53

    return
}

make_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/{lib,usr/lib}
    make && \
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    mv -v $TODD_FAKE_ROOT_DIR/usr/lib/libacl.so.* $TODD_FAKE_ROOT_DIR/lib
    ln -sfv ../../lib/$(readlink $TODD_FAKE_ROOT_DIR/usr/lib/libacl.so) $TODD_FAKE_ROOT_DIR/usr/lib/libacl.so

}

unpack_src && configure && make_install
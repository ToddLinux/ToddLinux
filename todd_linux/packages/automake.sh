# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf automake-1.16.3.tar.xz && \
    cd automake-1.16.3
}

configure() {
    sed -i "s/''/etags/" t/tags-lisp-space.sh

    ./configure --prefix=/usr --docdir=/usr/share/doc/automake-1.16.3

    return
}

make_install() {
    make

    # Using the -j4 make option speeds up the tests, even on systems with only one processor, due to internal delays in
    # individual tests. To test the results, issue:
    # make -j4 check

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    return
}

unpack_src && configure && make_install

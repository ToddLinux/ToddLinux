# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf bash-5.1.tar.gz
    cd bash-5.1
    return
}

configure() {
    sed -i '/^bashline.o:.*shmbchar.h/a bashline.o: ${DEFDIR}/builtext.h' Makefile.in
    ./configure --prefix=/usr \
        --docdir=/usr/share/doc/bash-5.1 \
        --without-bash-malloc \
        --with-installed-readline
    return
}

make_install() {
    make 
    
    chown -Rv tester .
    su tester -c "PATH=$PATH make tests < $(tty)"

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

post_install() {
    mkdir $TODD_FAKE_ROOT_DIR/bin
    mv $TODD_FAKE_ROOT_DIR/usr/bin/bash $TODD_FAKE_ROOT_DIR/bin/bash
    ln -sv bash $TODD_FAKE_ROOT_DIR/bin/sh
    return
}

unpack_src && configure && make_install && post_install

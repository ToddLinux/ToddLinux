# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf tcl8.6.11-src.tar.gz
    cd tcl8.6.11
    tar xf ../tcl8.6.11-html.tar.gz --strip-components=1
    return
}

configure() {
    SRCDIR=$(pwd)
    cd unix
    ./configure --prefix=/usr           \
                --mandir=/usr/share/man \
                $([ "$(uname -m)" = x86_64 ] && echo --enable-64bit)
}

make_install() {
    make
    sed -e "s|$SRCDIR/unix|/usr/lib|" \
        -e "s|$SRCDIR|/usr/include|"  \
        -i tclConfig.sh
    sed -e "s|$SRCDIR/unix/pkgs/tdbc1.1.2|/usr/lib/tdbc1.1.2|" \
        -e "s|$SRCDIR/pkgs/tdbc1.1.2/generic|/usr/include|"    \
        -e "s|$SRCDIR/pkgs/tdbc1.1.2/library|/usr/lib/tcl8.6|" \
        -e "s|$SRCDIR/pkgs/tdbc1.1.2|/usr/include|"            \
        -i pkgs/tdbc1.1.2/tdbcConfig.sh
    sed -e "s|$SRCDIR/unix/pkgs/itcl4.2.1|/usr/lib/itcl4.2.1|" \
        -e "s|$SRCDIR/pkgs/itcl4.2.1/generic|/usr/include|"    \
        -e "s|$SRCDIR/pkgs/itcl4.2.1|/usr/include|"            \
        -i pkgs/itcl4.2.1/itclConfig.sh
    unset SRCDIR

    make test
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    chmod -v u+w $TODD_FAKE_ROOT_DIR/usr/lib/libtcl8.6.so
    make install-private-headers
}

post_install() {
    ln -sfv tclsh8.6 $TODD_FAKE_ROOT_DIR/usr/bin/tclsh
    mv $TODD_FAKE_ROOT_DIR/usr/share/man/man3/{Thread,Tcl_Thread}.3
}

unpack_src && configure && make_install && post_install

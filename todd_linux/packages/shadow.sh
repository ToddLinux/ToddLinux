# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf shadow-4.8.1.tar.xz && \
    cd shadow-4.8.1
    return
}

configure() {
    sed -i 's/groups$(EXEEXT) //' src/Makefile.in
    find man -name Makefile.in -exec sed -i 's/groups\.1 / /' {} \;
    find man -name Makefile.in -exec sed -i 's/getspnam\.3 / /' {} \;
    find man -name Makefile.in -exec sed -i 's/passwd\.5 / /' {} \;

    sed -e 's:#ENCRYPT_METHOD DES:ENCRYPT_METHOD SHA512:' \
        -e 's:/var/spool/mail:/var/mail:' \
        -i etc/login.defs

    sed -i 's/1000/999/' etc/useradd
    touch $TODD_FAKE_ROOT_DIR/usr/bin/passwd
    ./configure --sysconfdir=/etc \
        --with-group-name-max-length=32
    return
}

make_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/{lib,usr/lib}
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR install

    # TODO: interactive mode
    # pwconv
    # grpconv
    # passwd root
}

unpack_src && configure && make_install

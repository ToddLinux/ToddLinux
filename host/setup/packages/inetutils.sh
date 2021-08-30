# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf inetutils-2.0.tar.xz
    cd inetutils-2.0
    return
}

configure() {
    ./configure --prefix=/usr        \
                --localstatedir=/var \
                --disable-logger     \
                --disable-whois      \
                --disable-rcp        \
                --disable-rexec      \
                --disable-rlogin     \
                --disable-rsh        \
                --disable-servers
    return
}

make_install() {
    make
    make -j1 DESTDIR=$LFS install
    return
}

unpack_src && configure && make_install

# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf iproute2-5.10.0.tar.xz
    cd iproute2-5.10.0
    return
}

configure() {
    sed -i /ARPD/d Makefile
    rm -fv man/man8/arpd.8
    sed -i 's/.m_ipt.o//' tc/Makefile
    # ./configure
    return
}

make_install() {
    make
    make -j1 DOCDIR=/usr/share/doc/iproute2-5.10.0 install
    return
}

unpack_src && configure && make_install

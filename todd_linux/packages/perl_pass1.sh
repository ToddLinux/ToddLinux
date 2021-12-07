# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

export BUILD_ZLIB=False
export BUILD_BZIP2=0

unpack_src() {
    tar xf perl-5.32.1.tar.xz && \
    cd perl-5.32.1
}

configure() {
    sh Configure -des \
        -Dprefix=/usr \
        -Dvendorprefix=/usr \
        -Dprivlib=/usr/lib/perl5/5.32/core_perl \
        -Darchlib=/usr/lib/perl5/5.32/core_perl \
        -Dsitelib=/usr/lib/perl5/5.32/site_perl \
        -Dsitearch=/usr/lib/perl5/5.32/site_perl \
        -Dvendorlib=/usr/lib/perl5/5.32/vendor_perl \
        -Dvendorarch=/usr/lib/perl5/5.32/vendor_perl \
        -Dman1dir=/usr/share/man/man1 \
        -Dman3dir=/usr/share/man/man3 \
        -Dpager="/usr/bin/less -isR" \
        -Duseshrplib \
        -Dusethreads
    return
}

make_install() {
    make

    # make test

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

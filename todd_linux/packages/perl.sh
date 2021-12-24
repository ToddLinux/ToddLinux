# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

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
                 -Dman1dir=/tmp/perl_garbage \
                 -Dman3dir=/tmp/perl_garbage
                 # perl is overly excited about writing man pages
                 # and for some reason if you give it 'none' as manpage directory it will still try to write
                 # hacky fix but whatever
                 # +rep
    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf util-linux-2.36.2.tar.xz && \
    cd util-linux-2.36.2
    return
}

configure() {
    mkdir -p /var/lib/hwclock && \
    ./configure ADJTIME_PATH=/var/lib/hwclock/adjtime \
                    --docdir=/usr/share/doc/util-linux-2.36.2 \
                    --disable-chfn-chsh \
                    --disable-login \
                    --disable-nologin \
                    --disable-su \
                    --disable-setpriv \
                    --disable-runuser \
                    --disable-pylibmount \
                    --disable-static \
                    --without-python \
                    runstatedir=/run
    return
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

unpack_src && configure && make_install

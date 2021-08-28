# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gettext-0.21.tar.xz && \
    cd gettext-0.21
}

configure() {
    ./configure --disable-shared
    return
}

make_install() {
    make && \
    cp -v gettext-tools/src/{msgfmt,msgmerge,xgettext} /usr/bin
}

unpack_src && configure && make_install
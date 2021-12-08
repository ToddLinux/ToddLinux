# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf grub-2.04.tar.xz && cd grub-2.04
    return
}

configure() {
    sed "s/gold-version/& -R .note.gnu.property/" -i Makefile.in grub-core/Makefile.in

    ./configure --prefix=/usr \
        --sbindir=/sbin \
        --sysconfdir=/etc \
        --disable-efiemu \
        --disable-werror

    return
}

make_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/usr/share/bash-completion/completions
    make -j1 && make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    mv -v $TODD_FAKE_ROOT_DIR/etc/bash_completion.d/grub $TODD_FAKE_ROOT_DIR/usr/share/bash-completion/completions
}

unpack_src && configure && make_install

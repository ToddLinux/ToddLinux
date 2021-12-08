# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf vim-8.2.2433.tar.gz && \
    cd vim-8.2.2433
    return
}

configure() {
    echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h

    ./configure --prefix=/usr
    return
}

make_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/usr/share/doc
    mkdir -p $TODD_FAKE_ROOT_DIR/etc

    make

    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install

    ln -sv vim $TODD_FAKE_ROOT_DIR/usr/bin/vi
    for L in $TODD_FAKE_ROOT_DIR/usr/share/man/{,*/}man1/vim.1; do
        ln -sv vim.1 $(dirname $L)/vi.1
    done

    ln -sv ../vim/vim82/doc $TODD_FAKE_ROOT_DIR/usr/share/doc/vim-8.2.2433
    
    echo "\" Begin /etc/vimrc
\" Ensure defaults are set before customizing settings, not after
source \$VIMRUNTIME/defaults.vim
let skip_defaults_vim=1
set nocompatible
set backspace=2
set mouse=
syntax on
\" if (&term == "xterm") || (&term == "putty")
\"  set background=dark
\" endif
\" End /etc/vimrc" > $TODD_FAKE_ROOT_DIR/etc/vimrc

    return
}

unpack_src && configure && make_install

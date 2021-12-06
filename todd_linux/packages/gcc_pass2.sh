# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf gcc-10.2.0.tar.xz && \
    cd gcc-10.2.0
    return
}

configure() {
    case $(uname -m) in
        x86_64)
        sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
        ;;
    esac

    mkdir -v build
    cd build

    ../configure --prefix=/usr \
        LD=ld \
        --enable-languages=c,c++ \
        --disable-multilib \
        --disable-bootstrap \
        --with-system-zlib

    return
}

make_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/{lib,usr/lib/bfd-plugins/}
    make
    
    ulimit -s 32768

    # chown -Rv tester .
    # su tester -c "PATH=$PATH make -k check"
    # ../contrib/test_summary
    
    make DESTDIR=$TODD_FAKE_ROOT_DIR install

    rm -rf $TODD_FAKE_ROOT_DIR/usr/lib/gcc/x86_64-pc-linux-gnu/10.2.0/include-fixed/bits/
    chown -v -R root:root $TODD_FAKE_ROOT_DIR/usr/lib/gcc/*linux-gnu/10.2.0/include{,-fixed}
    ln -sv ../usr/bin/cpp $TODD_FAKE_ROOT_DIR/lib/cpp
    ln -sfv ../../libexec/gcc/x86_64-pc-linux-gnu/10.2.0/liblto_plugin.so $TODD_FAKE_ROOT_DIR/usr/lib/bfd-plugins/

}

# TODO: test this toolchain

unpack_src && configure && make_install

# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf coreutils-8.32.tar.xz
    cd coreutils-8.32
    return
}

configure() {
    ./configure --prefix=/usr                     \
                --host=$LFS_TGT                   \
                --build=$(build-aux/config.guess) \
                --enable-install-program=hostname \
                --enable-no-install-program=kill,uptime
    return
}

make_install() {
    make && make -j1 install
    return
}

post_install() {
    mkdir -p $TODD_FAKE_ROOT_DIR/{bin,usr/sbin}
    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/{cat,chgrp,chmod,chown,cp,date,dd,df,echo} $TODD_FAKE_ROOT_DIR/bin
    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/{false,ln,ls,mkdir,mknod,mv,pwd,rm}        $TODD_FAKE_ROOT_DIR/bin
    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/{rmdir,stty,sync,true,uname}               $TODD_FAKE_ROOT_DIR/bin
    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/{head,nice,sleep,touch}                    $TODD_FAKE_ROOT_DIR/bin
    mv -v $TODD_FAKE_ROOT_DIR/usr/bin/chroot                                     $TODD_FAKE_ROOT_DIR/usr/sbin
    mkdir -pv $TODD_FAKE_ROOT_DIR/usr/share/man/man8
    mv -v $TODD_FAKE_ROOT_DIR/usr/share/man/man1/chroot.1                        $TODD_FAKE_ROOT_DIR/usr/share/man/man8/chroot.8
    sed -i 's/"1"/"8"/'                                           $TODD_FAKE_ROOT_DIR/usr/share/man/man8/chroot.8
    return
}

unpack_src && configure && make_install && post_install

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
    make && make -j1 DESTDIR=$LFS install
    return
}

post_install() {
    mv -v $LFS/usr/bin/{cat,chgrp,chmod,chown,cp,date,dd,df,echo} $LFS/bin
    mv -v $LFS/usr/bin/{false,ln,ls,mkdir,mknod,mv,pwd,rm}        $LFS/bin
    mv -v $LFS/usr/bin/{rmdir,stty,sync,true,uname}               $LFS/bin
    mv -v $LFS/usr/bin/{head,nice,sleep,touch}                    $LFS/bin
    mv -v $LFS/usr/bin/chroot                                     $LFS/usr/sbin
    mkdir -pv $LFS/usr/share/man/man8
    mv -v $LFS/usr/share/man/man1/chroot.1                        $LFS/usr/share/man/man8/chroot.8
    sed -i 's/"1"/"8"/'                                           $LFS/usr/share/man/man8/chroot.8
    return
}

unpack_src && configure && make_install && post_install

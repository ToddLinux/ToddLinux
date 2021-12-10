# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf glibc-2.33.tar.xz && cd glibc-2.33
    return
}

patch_src() {
    patch -Np1 -i ../glibc-2.33-fhs-1.patch
    return
}

configure() {
    sed -e '402a\      *result = local->data.services[database_index];' -i nss/nss_database.c
    mkdir -v build
    cd build
    touch $TODD_FAKE_ROOT_DIR/etc/ld.so.conf
    ../configure --prefix=/usr                            \
                 --disable-werror                         \
                 --enable-kernel=3.2                      \
                 --enable-stack-protector=strong          \
                 --with-headers=/usr/include              \
                 libc_cv_slibdir=/lib
    sed '/test-installation/s@$(PERL)@echo not running@' -i ../Makefile
    return
}

make_install() {
    make -j1
    make check
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    cp -v ../nscd/nscd.conf $TODD_FAKE_ROOT_DIR/etc/nscd.conf
    mkdir -pv $TODD_FAKE_ROOT_DIR/var/cache/nscd
}

install_locals() {
    mkdir -pv $TODD_FAKE_ROOT_DIR/usr/lib/locale
    localedef --prefix $TODD_FAKE_ROOT_DIR -i POSIX      -f UTF-8       C.UTF-8 2> /dev/null || true
    localedef --prefix $TODD_FAKE_ROOT_DIR -i cs_CZ      -f UTF-8       cs_CZ.UTF-8
    localedef --prefix $TODD_FAKE_ROOT_DIR -i de_DE      -f ISO-8859-1  de_DE
    localedef --prefix $TODD_FAKE_ROOT_DIR -i de_DE@euro -f ISO-8859-15 de_DE@euro
    localedef --prefix $TODD_FAKE_ROOT_DIR -i de_DE      -f UTF-8       de_DE.UTF-8
    localedef --prefix $TODD_FAKE_ROOT_DIR -i el_GR      -f ISO-8859-7  el_GR
    localedef --prefix $TODD_FAKE_ROOT_DIR -i en_GB      -f UTF-8       en_GB.UTF-8
    localedef --prefix $TODD_FAKE_ROOT_DIR -i en_HK      -f ISO-8859-1  en_HK
    localedef --prefix $TODD_FAKE_ROOT_DIR -i en_PH      -f ISO-8859-1  en_PH
    localedef --prefix $TODD_FAKE_ROOT_DIR -i en_US      -f ISO-8859-1  en_US
    localedef --prefix $TODD_FAKE_ROOT_DIR -i en_US      -f UTF-8       en_US.UTF-8
    localedef --prefix $TODD_FAKE_ROOT_DIR -i es_MX      -f ISO-8859-1  es_MX
    localedef --prefix $TODD_FAKE_ROOT_DIR -i fa_IR      -f UTF-8       fa_IR
    localedef --prefix $TODD_FAKE_ROOT_DIR -i fr_FR      -f ISO-8859-1  fr_FR
    localedef --prefix $TODD_FAKE_ROOT_DIR -i fr_FR@euro -f ISO-8859-15 fr_FR@euro
    localedef --prefix $TODD_FAKE_ROOT_DIR -i fr_FR      -f UTF-8       fr_FR.UTF-8
    localedef --prefix $TODD_FAKE_ROOT_DIR -i it_IT      -f ISO-8859-1  it_IT
    localedef --prefix $TODD_FAKE_ROOT_DIR -i it_IT      -f UTF-8       it_IT.UTF-8
    localedef --prefix $TODD_FAKE_ROOT_DIR -i ja_JP      -f EUC-JP      ja_JP
    localedef --prefix $TODD_FAKE_ROOT_DIR -i ja_JP      -f SHIFT_JIS   ja_JP.SIJS 2> /dev/null || true
    localedef --prefix $TODD_FAKE_ROOT_DIR -i ja_JP      -f UTF-8       ja_JP.UTF-8
    localedef --prefix $TODD_FAKE_ROOT_DIR -i ru_RU      -f KOI8-R      ru_RU.KOI8-R
    localedef --prefix $TODD_FAKE_ROOT_DIR -i ru_RU      -f UTF-8       ru_RU.UTF-8
    localedef --prefix $TODD_FAKE_ROOT_DIR -i tr_TR      -f UTF-8       tr_TR.UTF-8
    localedef --prefix $TODD_FAKE_ROOT_DIR -i zh_CN      -f GB18030     zh_CN.GB18030
    localedef --prefix $TODD_FAKE_ROOT_DIR -i zh_HK      -f BIG5-HKSCS  zh_HK.BIG5-HKSCS
}

# TODO: FIX THIS LATER
# grep output should be "[Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]""
# test_toolchain() {
#     echo 'int main(){}' > dummy.c && $LFS/tools/bin/$LFS_TGT-gcc dummy.c && readelf -l a.out | grep '/ld-linux'
#     return
# }

create_links() {
    mkdir $TODD_FAKE_ROOT_DIR/lib64 &&\
    ln -sfv $TODD_FAKE_ROOT_DIR/lib/ld-linux-x86-64.so.2 $TODD_FAKE_ROOT_DIR/lib64 &&\
    ln -sfv $TODD_FAKE_ROOT_DIR/lib/ld-linux-x86-64.so.2 $TODD_FAKE_ROOT_DIR/lib64/ld-lsb-x86-64.so.3
    return
}

post_configure() {
    cat > $TODD_FAKE_ROOT_DIR/etc/nsswitch.conf << "EOF"
# Begin /etc/nsswitch.conf
passwd: files
group: files
shadow: files
hosts: files dns
networks: files
protocols: files
services: files
ethers: files
rpc: files
# End /etc/nsswitch.conf
EOF

    cat > $TODD_FAKE_ROOT_DIR/etc/ld.so.conf << "EOF"
# Begin /etc/ld.so.conf
/usr/local/lib
/opt/lib
EOF
}

timezone_setup() {
    tar -xf ../../tzdata2021a.tar.gz

    ZONEINFO=$TODD_FAKE_ROOT_DIR/usr/share/zoneinfo
    mkdir -pv $ZONEINFO/{posix,right}
    for tz in etcetera southamerica northamerica europe africa antarctica asia australasia backward; do
        zic -L /dev/null   -d $ZONEINFO       ${tz}
        zic -L /dev/null   -d $ZONEINFO/posix ${tz}
        zic -L leapseconds -d $ZONEINFO/right ${tz}
    done
    cp -v zone.tab zone1970.tab iso3166.tab $ZONEINFO
    zic -d $ZONEINFO -p America/New_York
    unset ZONEINFO

    ln -sfv /usr/share/zoneinfo/Europe/Berlin /etc/localtime
}

unpack_src && patch_src && configure && make_install && install_locals && create_links && post_configure && timezone_setup

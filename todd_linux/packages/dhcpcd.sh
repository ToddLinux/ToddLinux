# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf dhcpcd-9.4.0.tar.xz
    cd dhcpcd-9.4.0
    return
}

setup_users() {
    # TODO: can't cleanly be uninstalled
    install  -v -m700 -d /var/lib/dhcpcd &&

    groupadd -g 52 dhcpcd        &&
    useradd  -c 'dhcpcd PrivSep' \
             -d /var/lib/dhcpcd  \
             -g dhcpcd           \
             -s /bin/false     \
             -u 52 dhcpcd &&
    chown    -v dhcpcd:dhcpcd /var/lib/dhcpcd 
}

configure() {
    ./configure --prefix=/usr                \
                --sysconfdir=/etc            \
                --libexecdir=/usr/lib/dhcpcd \
                --dbdir=/var/lib/dhcpcd      \
                --privsepuser=dhcpcd
}

make_install() {
    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    return
}

post_install() {
ONBOOT="yes"
cat > /etc/sysconfig/ifconfig.enp0s3 << "EOF"
IFACE="enp0s3"
SERVICE="dhcpcd"
DHCP_START="-b -q <insert appropriate start options here>"
DHCP_STOP="-k <insert additional stop options here>"
EOF
}

unpack_src && setup_users && configure && make_install && post_install

# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

export CFLAGS="${CFLAGS:--g -O2} -Wall -fno-strict-aliasing         \
        -D_PATH_DHCLIENT_SCRIPT='\"/usr/sbin/dhclient-script\"'     \
        -D_PATH_DHCPD_CONF='\"/etc/dhcp/dhcpd.conf\"'               \
        -D_PATH_DHCLIENT_CONF='\"/etc/dhcp/dhclient.conf\"'"

unpack_src() {
    tar xf dhcp-4.4.2-P1.tar.gz
    cd dhcp-4.4.2-P1
    return
}

configure() {
    sed -i '/o.*dhcp_type/d' server/mdb.c
    sed -r '/u.*(local|remote)_port/d'    \
        -i client/dhclient.c              \
           relay/dhcrelay.c

    ./configure --prefix=/usr                                           \
                --sysconfdir=/etc/dhcp                                  \
                --localstatedir=/var                                    \
                --with-srv-lease-file=/var/lib/dhcpd/dhcpd.leases       \
                --with-srv6-lease-file=/var/lib/dhcpd/dhcpd6.leases     \
                --with-cli-lease-file=/var/lib/dhclient/dhclient.leases \
                --with-cli6-lease-file=/var/lib/dhclient/dhclient6.leases
}

make_install() {
    make -j1
    make DESTDIR=$TODD_FAKE_ROOT_DIR -j1 install
    # now it should work :>
    # TODO: install dhcp server here aswell
    install -v -m755 client/scripts/linux $TODD_FAKE_ROOT_DIR/usr/sbin/dhclient-script
    return
}

configure_dhcp() {
    install -vdm755 /etc/dhcp &&
    echo "# Begin /etc/dhcp/dhclient.conf
#
# Basic dhclient.conf(5)

#prepend domain-name-servers 127.0.0.1;
request subnet-mask, broadcast-address, time-offset, routers,
        domain-name, domain-name-servers, domain-search, host-name,
        netbios-name-servers, netbios-scope, interface-mtu,
        ntp-servers;
require subnet-mask, domain-name-servers;
#timeout 60;
#retry 60;
#reboot 10;
#select-timeout 5;
#initial-interval 2;

# End /etc/dhcp/dhclient.conf
" > $TODD_FAKE_ROOT_DIR/etc/dhcp/dhclient.conf

    install -v -dm 755 $TODD_FAKE_ROOT_DIR/var/lib/dhclient
    # TODO: stuff left
}

unpack_src && configure && make_install

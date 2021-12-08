# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf sysklogd-1.5.1.tar.gz && \
    cd sysklogd-1.5.1
    return
}

configure() {
    sed -i '/Error loading kernel symbols/{n;n;d}' ksym_mod.c
    sed -i 's/union wait/int/' syslogd.c

    return
}

make_install() {
    mkdir $TODD_FAKE_ROOT_DIR/etc

    make
    make DESTDIR=$TODD_FAKE_ROOT_DIR BINDIR=/sbin -j1 install

    echo "# Begin /etc/syslog.conf
auth,authpriv.* -/var/log/auth.log
*.*;auth,authpriv.none -/var/log/sys.log
daemon.* -/var/log/daemon.log
kern.* -/var/log/kern.log
mail.* -/var/log/mail.log
user.* -/var/log/user.log
*.emerg *
# End /etc/syslog.conf
" >  $TODD_FAKE_ROOT_DIR/etc/syslog.conf

    return
}

unpack_src && configure && make_install

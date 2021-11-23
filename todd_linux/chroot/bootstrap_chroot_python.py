#!/usr/bin/env python3
# THIS SCRIPT HAS TO BE EXECUTED FROM WITHIN CHROOT ENVIRONMENT!
# it isn't being executed from the main system because requests hasn't been installed yet
import os
import sys

SIGN_FILE = "lfs_sign.lock"
DIRECTORY_LAYOUT = [
    "/boot",
    "/home",
    "/var",
    "/mnt",
    "/opt",
    "/srv",
    "/etc",
    "/lib",
    "/usr",
    "/media",
    "/etc/opt",
    "/etc/sysconfig",
    "/lib/firmware",
    "/media/floppy",
    "/media/cdrom",
    "/usr/bin",
    "/usr/include",
    "/usr/lib",
    "/usr/sbin",
    "/usr/src",
    "/usr/local",
    "/usr/share",
    "/usr/local/bin",
    "/usr/local/include",
    "/usr/local/lib",
    "/usr/local/sbin",
    "/usr/local/src",
    "/usr/local/share",
    "/usr/share/color",
    "/usr/share/dict",
    "/usr/share/doc",
    "/usr/share/info",
    "/usr/share/locale",
    "/usr/share/man",
    "/usr/local/share/color",
    "/usr/local/share/dict",
    "/usr/local/share/doc",
    "/usr/local/share/info",
    "/usr/local/share/locale",
    "/usr/local/share/man",
    "/usr/share/misc",
    "/usr/share/terminfo",
    "/usr/share/zoneinfo",
    "/usr/local/share/misc",
    "/usr/local/share/terminfo",
    "/usr/local/share/zoneinfo",
    "/usr/share/man/man1",
    "/usr/share/man/man2",
    "/usr/share/man/man3",
    "/usr/share/man/man4",
    "/usr/share/man/man5",
    "/usr/share/man/man6",
    "/usr/share/man/man7",
    "/usr/share/man/man8",
    "/usr/local/share/man/man1",
    "/usr/local/share/man/man2",
    "/usr/local/share/man/man3",
    "/usr/local/share/man/man4",
    "/usr/local/share/man/man5",
    "/usr/local/share/man/man6",
    "/usr/local/share/man/man7",
    "/usr/local/share/man/man8",
    "/var/cache",
    "/var/local",
    "/var/log",
    "/var/mail",
    "/var/opt",
    "/var/spool",
    "/var/lib",
    "/var/lib/color",
    "/var/lib/misc",
    "/var/lib/locate",
]


# TODO: this file shouldn't be encoded here
# TODO: better domain?
RESOLV_FILE = """# Begin /etc/resolv.conf
domain todd.org
nameserver 1.1.1.1
nameserver 8.8.8.8
# End /etc/resolv.conf
"""

# TODO: this file shouldn't be encoded here
GROUP_FILE = """root:x:0:
bin:x:1:daemon
sys:x:2:
kmem:x:3:
tape:x:4:
tty:x:5:
daemon:x:6:
floppy:x:7:
disk:x:8:
lp:x:9:
dialout:x:10:
audio:x:11:
video:x:12:
utmp:x:13:
usb:x:14:
cdrom:x:15:
adm:x:16:
messagebus:x:18:
input:x:24:
mail:x:34:
kvm:x:61:
uuidd:x:80:
wheel:x:97:
nogroup:x:99:
users:x:999:
"""

# TODO: this file shouldn't be encoded here
PASSWD_FILE = """root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/dev/null:/bin/false
daemon:x:6:6:Daemon User:/dev/null:/bin/false
messagebus:x:18:18:D-Bus Message Daemon User:/run/dbus:/bin/false
uuidd:x:80:80:UUID Generation Daemon User:/dev/null:/bin/false
nobody:x:99:99:Unprivileged User:/dev/null:/bin/false"""

# TODO: this file shouldn't be encoded here
HOSTS_FILE = "127.0.0.1 localhost"


def main() -> bool:
    print("entering chroot to bootstrap python: ok")
    os.chdir("/")
    print("preparing chroot from within chroot environment: ...")

    # set correct linker paths for python with openssl
    os.system("ldconfig /usr/local/lib")

    for folder in DIRECTORY_LAYOUT:
        if not os.path.isdir(folder):
            os.mkdir(folder)

    if os.system("""ln -sfv /run /var/run &&
                    ln -sfv /run/lock /var/lock &&
                    ln -sfv /proc/self/mounts /etc/mtab""") != 0:
        return False

    if os.system("""
    install -dv -m 0750 /root &&
    install -dv -m 1777 /tmp /var/tmp
    """) != 0:
        return False

    with open("/etc/hosts", "w") as file:
        file.write(HOSTS_FILE)

    with open("/etc/passwd", "w") as file:
        file.write(PASSWD_FILE)

    with open("/etc/group", "w") as file:
        file.write(GROUP_FILE)

    # this adds new user
    if os.system("""
    echo "\ntester:x:$(ls -n $(tty) | cut -d" " -f3):101::/home/tester:/bin/bash" >> /etc/passwd &&
    echo "\ntester:x:101:" >> /etc/group &&
    install -o tester -d /home/tester
    """) != 0:
        return False

    # some stub log files
    if os.system("""
    touch /var/log/{btmp,lastlog,faillog,wtmp} &&
    chgrp -v utmp /var/log/lastlog &&
    chmod -v 664  /var/log/lastlog &&
    chmod -v 600  /var/log/btmp
    """) != 0:
        return False

    with open("/etc/resolv.conf", "w") as file:
        file.write(RESOLV_FILE)

    print("installing requests with pip: ...")
    if os.system(f"python3 -m pip install requests") != 0:
        return False
    print("installing requests with pip: ok")

    print("preparing chroot from within chroot environment: ok")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

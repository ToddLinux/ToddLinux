# THIS SCRIPT HAS TO BE EXECUTED FROM WITHIN CHROOT ENVIRONMENT!
import sys
import os

SIGN_FILE = "lfs_sign.lock"
DIRECTORY_LAYOUT = ["boot", "home", "mnt", "opt", "srv"]


def main() -> bool:
    os.chdir("/")
    print("preparing chroot from within chroot environment: ...")
    # "don't fuck up my system"-protection
    if not os.path.exists(SIGN_FILE):
        print(f"Error: chroot root path doesn't contain the sign file; Are you sure you're using this script from within the chroot environment; use sign_lfs.py to create one")
        return False

    for folder in DIRECTORY_LAYOUT:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    if os.system("""
    mkdir -pv /etc/{opt,sysconfig} &&
    mkdir -pv /lib/firmware &&
    mkdir -pv /media/{floppy,cdrom} &&
    mkdir -pv /usr/{,local/}{bin,include,lib,sbin,src} &&
    mkdir -pv /usr/{,local/}share/{color,dict,doc,info,locale,man} &&
    mkdir -pv /usr/{,local/}share/{misc,terminfo,zoneinfo} &&
    mkdir -pv /usr/{,local/}share/man/man{1..8} &&
    mkdir -pv /var/{cache,local,log,mail,opt,spool} &&
    mkdir -pv /var/lib/{color,misc,locate} &&
    ln -sfv /run /var/run &&
    ln -sfv /run/lock /var/lock &&
    install -dv -m 0750 /root &&
    install -dv -m 1777 /tmp /var/tmp &&
    ln -sfv /proc/self/mounts /etc/mtab
    """) != 0:
        return False

    with open("/etc/hosts", "w") as file:
        file.write("127.0.0.1 localhost $(hostname)")

    with open("/etc/passwd", "w") as file:
        file.write("""root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/dev/null:/bin/false
daemon:x:6:6:Daemon User:/dev/null:/bin/false
messagebus:x:18:18:D-Bus Message Daemon User:/run/dbus:/bin/false
uuidd:x:80:80:UUID Generation Daemon User:/dev/null:/bin/false
nobody:x:99:99:Unprivileged User:/dev/null:/bin/false""")

    with open("/etc/group", "w") as file:
        file.write("""root:x:0:
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
users:x:999:""")

    if os.system("""
    echo "\ntester:x:$(ls -n $(tty) | cut -d" " -f3):101::/home/tester:/bin/bash" >> /etc/passwd &&
    echo "\ntester:x:101:" >> /etc/group &&
    install -o tester -d /home/tester
    """) != 0:
        return False

    if os.system("""
    touch /var/log/{btmp,lastlog,faillog,wtmp} &&
    chgrp -v utmp /var/log/lastlog &&
    chmod -v 664  /var/log/lastlog &&
    chmod -v 600  /var/log/btmp
    """) != 0:
        return False

    print("preparing chroot from within chroot environment: ok")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

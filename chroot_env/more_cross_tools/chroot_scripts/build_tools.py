# to be executed from within chroot environment
import sys
import os

DIRECTORY_LAYOUT = ["boot", "home", "mnt", "opt", "srv"]


def main() -> int:
    os.chdir("/")
    if not os.path.exists("lfs_sign.loc"):
        print("Error: executing chroot cript in dir that doesn't have sign file; use sign_lfs.py to create one")
        return 1
    for folder in DIRECTORY_LAYOUT:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    # todo: not catching failures
    os.system("""
    mkdir -pv /etc/{opt,sysconfig};
    mkdir -pv /lib/firmware;
    mkdir -pv /media/{floppy,cdrom};
    mkdir -pv /usr/{,local/}{bin,include,lib,sbin,src};
    mkdir -pv /usr/{,local/}share/{color,dict,doc,info,locale,man};
    mkdir -pv /usr/{,local/}share/{misc,terminfo,zoneinfo};
    mkdir -pv /usr/{,local/}share/man/man{1..8};
    mkdir -pv /var/{cache,local,log,mail,opt,spool};
    mkdir -pv /var/lib/{color,misc,locate};
    ln -sfv /run /var/run;
    ln -sfv /run/lock /var/lock;
    install -dv -m 0750 /root;
    install -dv -m 1777 /tmp /var/tmp;
    ln -sv /proc/self/mounts /etc/mtab;
    """)

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

    os.system("""
    echo "tester:x:$(ls -n $(tty) | cut -d" " -f3):101::/home/tester:/bin/bash" >> /etc/passwd;
    echo "tester:x:101:" >> /etc/group;
    install -o tester -d /home/tester;
    """)

    os.system("""
    touch /var/log/{btmp,lastlog,faillog,wtmp};
    chgrp -v utmp /var/log/lastlog;
    chmod -v 664  /var/log/lastlog;
    chmod -v 600  /var/log/btmp;
    """)

    return 0


if __name__ == "__main__":
    sys.exit(main())

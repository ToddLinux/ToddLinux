import os
import shutil


from ..host import assert_signed
from ..todd.todd import install_packages

REQUIRED_TARGET_PACKAGES = [
    ("kernel", 0)
]

SCRIPTS_FOLDER = "/scripts"

# TODO: this file shouldn't be encoded here
ETC_FSTAB = """# Begin /etc/fstab
# file system mount-point type options dump fsck
# order
/dev/sda / iso9660 ro 1 1
tmpfs /tmp tmpfs mode=1777,nosuid,nodev 0 0
tmpfs /var/log/ tmpfs mode=1777,nosuid,nodev 0 0
proc /proc proc nosuid,noexec,nodev 0 0
sysfs /sys sysfs nosuid,noexec,nodev 0 0
devpts /dev/pts devpts gid=5,mode=620 0 0
tmpfs /run tmpfs defaults 0 0
devtmpfs /dev devtmpfs mode=0755,nosuid 0 0
# End /etc/fstab
"""

# TODO: this file shouldn't be encoded here
ETC_PROFILE = """# Begin /etc/profile
export LANG=en_US.UTF-8
# End /etc/profile
"""

# TODO: this file shouldn't be encoded here
ETC_INPUTRC = r"""# Begin /etc/inputrc
# Modified by Chris Lynn <roryo@roryo.dynup.net>
# Allow the command prompt to wrap to the next line
set horizontal-scroll-mode Off
# Enable 8bit input
set meta-flag On
set input-meta On
# Turns off 8th bit stripping
set convert-meta Off
# Keep the 8th bit for display
set output-meta On
# none, visible or audible
set bell-style none
# All of the following map the escape sequence of the value
# contained in the 1st argument to the readline specific functions
"\eOd": backward-word
"\eOc": forward-word
# for linux console
"\e[1~": beginning-of-line
"\e[4~": end-of-line
"\e[5~": beginning-of-history
"\e[6~": end-of-history
"\e[3~": delete-char
"\e[2~": quoted-insert
# for xterm
"\eOH": beginning-of-line
"\eOF": end-of-line
# for Konsole
"\e[H": beginning-of-line
"\e[F": end-of-line
# End /etc/inputrc"""

# TODO: this file shouldn't be encoded here
ETC_SHELLS = """# Begin /etc/shells
/bin/sh
/bin/bash
# End /etc/shells"""

# TODO: this file shouldn't be encoded here
ETC_USB = """# Begin /etc/modprobe.d/usb.conf
install ohci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i ohci_hcd ; true
install uhci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i uhci_hcd ; true
# End /etc/modprobe.d/usb.conf"""

# TODO: this file shouldn't be encoded here
# GRUB_CFG = """# Begin /boot/grub/grub.cfg
# set default=0
# set timeout=5
# insmod ext2
# set root=(hd0,1)

# menuentry "ToddLinux, Linux 5.10.17-lfs-10.1" {
# linux /boot/vmlinuz-5.10.17-lfs-10.1 root=/dev/sda1 ro
# }
# """

# TODO: this file shouldn't be encoded here
ISO_LINUX_CFG = """
default bootcd
prompt 1
timeout 40

label bootcd
  kernel vmlinuz-5.10.17-lfs-10.1
  append root=/dev/sr0
"""

# TODO: this file shouldn't be encoded here
INITTAB = """
# Begin /etc/inittab

id:3:initdefault:

si::sysinit:/etc/rc.d/init.d/rc S

l0:0:wait:/etc/rc.d/init.d/rc 0
l1:S1:wait:/etc/rc.d/init.d/rc 1
l2:2:wait:/etc/rc.d/init.d/rc 2
l3:3:wait:/etc/rc.d/init.d/rc 3
l4:4:wait:/etc/rc.d/init.d/rc 4
l5:5:wait:/etc/rc.d/init.d/rc 5
l6:6:wait:/etc/rc.d/init.d/rc 6

ca:12345:ctrlaltdel:/sbin/shutdown -t1 -a -r now

su:S016:once:/sbin/sulogin

1:2345:respawn:/sbin/agetty --noclear tty1 9600
2:2345:respawn:/sbin/agetty tty2 9600
3:2345:respawn:/sbin/agetty tty3 9600
4:2345:respawn:/sbin/agetty tty4 9600
5:2345:respawn:/sbin/agetty tty5 9600
6:2345:respawn:/sbin/agetty tty6 9600

# End /etc/inittab
"""

ETC_RCD_INITD_CREATE_RAMDISK = """#!/bin/sh


case "$1" in
        start)
                mknod /dev/ram0 b 1 0
                echo -n "Mounting etc ramdisk ...              "
                mount -t tmpfs -o size=64m tmpfs /etc
                
                sleep 1
                echo -n "Copying files to ramdisk ...                 "
                cp -pR /etc_files/* /etc
                sleep 1
                ;;
        *)
                echo "Usage: $0 {start}"
                exit 1
                ;;
esac
"""


def post_install_chroot(verbose: bool, jobs: int) -> bool:
    os.chdir("/")
    assert_signed()
    print("performing post-install: ...")
    with open("/etc/inittab", "w") as file:
        file.write(INITTAB)

    with open("/etc/fstab", "w") as file:
        file.write(ETC_FSTAB)

    with open("/etc/profile", "w") as file:
        file.write(ETC_PROFILE)

    with open("/etc/inputrc", "w") as file:
        file.write(ETC_INPUTRC)

    with open("/etc/shells", "w") as file:
        file.write(ETC_SHELLS)

    with open("/etc/rc.d/init.d/create_ramdisk", "w") as file:
        file.write(ETC_RCD_INITD_CREATE_RAMDISK)


    shutil.rmtree("etc_files")
    shutil.copytree("etc", "etc_files")

    if os.system("chmod 0755 /etc/rc.d/init.d/create_ramdisk"):
        return False
    
    if os.system("cp /etc/rc.d/init.d/create_ramdisk /etc/rc.d/rcS.d/S99create_ramdisk"):
        return False

    
    print("performing post-install: ok")


    print("installing kernel: ...")
    if not install_packages(
        REQUIRED_TARGET_PACKAGES,
        f"{SCRIPTS_FOLDER}/todd_linux/packages",
        "target",
        "/",
        verbose,
        jobs,
    ):
        return False
    print("installing kernel: ok")

    print("performing final setup: ...")
    # setup shadowed passwords and enable root account
    # TODO: maybe move this to shadow.sh?
    if os.system("pwconv"):
        return False

    if os.system("grpconv"):
        return False

    if os.system("echo root:root | chpasswd"):
        return False

    if os.system("install -v -m755 -d /etc/modprobe.d"):
        return False
    with open("/etc/modprobe.d/usb.conf", "w") as file:
        file.write(ETC_USB)

    with open("/boot/isolinux.cfg", "w") as file:
        file.write(ISO_LINUX_CFG)
    print("performing final setup: ok")

    print("cleanup: ...")

    shutil.rmtree("/tmp", ignore_errors=True)
    os.mkdir("/tmp")

    shutil.rmtree("/tools", ignore_errors=True)

    shutil.rmtree("/var/cache/todd", ignore_errors=True)
    os.mkdir("/var/cache/todd")

    print("cleanup: ok")

    return True

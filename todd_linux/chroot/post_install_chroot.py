import os

from ..host import assert_signed
from ..todd.todd import install_packages

REQUIRED_TARGET_PACKAGES = [
    ("kernel", 0)
]

SCRIPTS_FOLDER = "/scripts"

ETC_FSTAB = """# Begin /etc/fstab
# file system mount-point type options dump fsck
# order
/dev/sda / ext4 defaults 1 1
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

ETC_SHELLS = """# Begin /etc/shells
/bin/sh
/bin/bash
# End /etc/shells"""

ETC_USB = """# Begin /etc/modprobe.d/usb.conf
install ohci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i ohci_hcd ; true
install uhci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i uhci_hcd ; true
# End /etc/modprobe.d/usb.conf"""

GRUB_CFG = """# Begin /boot/grub/grub.cfg
set default=0
set timeout=5
insmod ext2
set root=(hd0,1)

menuentry "ToddLinux, Linux 5.10.17-lfs-10.1" {
linux /boot/vmlinuz-5.10.17-lfs-10.1 root=/dev/sda1 ro
}
"""

ISO_LINUX_CFG = """
default bootcd
prompt 1
timeout 40

label bootcd
  kernel vmlinuz-5.10.17-lfs-10.1
  append root=/dev/sr0
"""


def post_install_chroot(verbose: bool, jobs: int) -> bool:
    os.chdir("/")
    assert_signed()
    print("performing post-install: ...")

    with open("/etc/fstab", "w") as file:
        file.write(ETC_FSTAB)

    with open("/etc/profile", "w") as file:
        file.write(ETC_PROFILE)

    with open("/etc/inputrc", "w") as file:
        file.write(ETC_INPUTRC)

    with open("/etc/shells", "w") as file:
        file.write(ETC_SHELLS)
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
    if os.system("install -v -m755 -d /etc/modprobe.d"):
        return False
    with open("/etc/modprobe.d/usb.conf", "w") as file:
        file.write(ETC_USB)

    with open("/boot/isolinux.cfg", "w") as file:
        file.write(ISO_LINUX_CFG)
    print("performing final setup: ok")

    return True

    # if os.system("mkdir -p /boot/grub"):
    #     return False
    # with open("/boot/grub/grub.cfg", "w") as file:
    #     file.write(GRUB_CFG)
    # print("performing final setup: ok")

    # return True

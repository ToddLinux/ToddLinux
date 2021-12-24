import os

from ..host import assert_signed
from ..todd.todd import install_packages

REQUIRED_TARGET_PACKAGES = [
    ("kernel", 0)
]

SCRIPTS_FOLDER = "/scripts"

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


def post_install_chroot(verbose: bool, jobs: int) -> bool:
    os.chdir("/")
    assert_signed()
    print("performing post-install: ...")

    # TODO: missing fstab

    with open("/etc/profile", "w") as file:
        file.write(ETC_PROFILE)

    with open("/etc/inputrc", "w") as file:
        file.write(ETC_INPUTRC)

    with open("/etc/shells", "w") as file:
        file.write(ETC_SHELLS)
    print("performing post-install: ok")

    if not install_packages(
        REQUIRED_TARGET_PACKAGES,
        f"{SCRIPTS_FOLDER}/todd_linux/packages",
        "target",
        "/",
        verbose,
        jobs,
    ):
        return False

    os.system("install -v -m755 -d /etc/modprobe.d")
    with open("/etc/modprobe.d/usb.conf", "w") as file:
        file.write(ETC_USB)

    return True

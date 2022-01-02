import os
from typing import Optional

from ..host import assert_signed
from ..todd.todd import install_packages, update_repo
from .post_install_chroot import post_install_chroot

__all__ = ["install_from_chroot"]

SCRIPTS_FOLDER = "/scripts"


SIGN_FILE = "lfs_sign.lock"
REQUIRED_INTERMEDIATE_PACKAGES = [
    ("libstdcpp", 1),
    ("gettext", 0),
    ("bison", 0),
    ("perl", 0),
    ("python3.7", 1),
    ("texinfo", 0),
    ("util-linux", 0),
]
REQUIRED_TARGET_PACKAGES = [
    ("man-pages", -1),
    ("glibc", -1),
    ("pkg-config", -1),
    ("libpipeline", -1),
    ("zlib", -1),
    ("bzip2", -1),
    ("xz", -1),
    ("zstd", -1),
    ("file", -1),
    ("readline", -1),
    ("m4", -1),
    ("bc", -1),
    ("flex", -1),
    ("tcl", -1),
    ("expect", -1),
    ("dejagnu", -1),
    ("binutils", -1),
    ("gmp", -1),
    ("mpfr", -1),
    ("mpc", -1),
    ("attr", -1),
    ("acl", -1),
    ("libcap", -1),
    ("shadow", -1),
    ("gcc", -1),
    ("ncurses", -1),
    ("sed", -1),
    ("psmisc", -1),
    ("gettext", -1),
    ("bison", -1),
    ("grep", -1),
    ("bash", -1),
    ("libtool", -1),
    ("gdbm", -1),
    ("gperf", -1),
    ("expat", -1),
    ("inetutils", -1),
    ("perl", -1),
    ("xmlparser", -1),
    ("intltool", -1),
    ("autoconf", -1),
    ("automake", -1),
    ("kmod", -1),
    ("libelf", -1),
    ("libffi", -1),
    ("openssl", -1),
    ("python3.7", -1),
    ("coreutils", -1),
    ("check", -1),
    ("diffutils", -1),
    ("gawk", -1),
    ("findutils", -1),
    ("groff", -1),
    ("grub", -1),
    ("less", -1),
    ("gzip", -1),
    ("iproute2", -1),
    ("kbd", -1),
    ("make", -1),
    ("patch", -1),
    ("man-db", -1),
    ("tar", -1),
    ("texinfo", -1),
    ("vim", -1),
    ("eudev", -1),
    ("procps-ng", -1),
    ("util-linux", -1),
    ("e2fsprogs", -1),
    ("sysklogd", -1),
    ("sysvinit", -1),
    ("live_cd_lfs_bootscripts", -1),
    ("blfs_bootscripts", -1),
    ("dhcpcd", -1),
    ("isolinux", -1),
    ("wget", -1),
    # ("dhcp", -1),  # we don't two different DHCP clients right now
]


def install_from_chroot(verbose: bool, jobs: Optional[int]) -> bool:
    print("entering chroot to install from chroot: ok")
    if jobs is None:
        jobs = 2

    os.chdir("/")
    assert_signed()
    print("installing intermediate tools from within chroot environment: ...")

    if not install_packages(
        REQUIRED_INTERMEDIATE_PACKAGES,
        "chroot",
        "/",
        verbose,
        jobs,
        f"{SCRIPTS_FOLDER}/todd_linux/packages",
    ):
        return False
    print("installing intermediate tools from within chroot environment: ok")
    if not update_repo():
        return False
    print("installing target packages from within chroot environment: ...")
    if not install_packages(
        REQUIRED_TARGET_PACKAGES,
        "target",
        "/",
        verbose,
        jobs,
    ):
        return False
    print("installing target packages from within chroot environment: ok")

    return post_install_chroot(verbose, jobs)

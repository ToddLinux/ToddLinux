import os
from typing import Optional

from ..host import assert_signed
from ..todd.todd import install_packages

__all__ = ["install_from_chroot"]

SCRIPTS_FOLDER = f"/scripts"


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
    ("man-pages", 0),
    ("glibc", 1),
    ("pkg-config", 0),
    ("libpipeline", 0),
    # TODO: add back when other packages installed
    # ("man-db", 0),
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
        f"{SCRIPTS_FOLDER}/todd_linux/packages",
        "chroot",
        "/",
        verbose,
        jobs,
    ):
        return False
    print("installing intermediate tools from within chroot environment: ok")
    print("installing target packages from within chroot environment: ...")
    if not install_packages(
        REQUIRED_TARGET_PACKAGES,
        f"{SCRIPTS_FOLDER}/todd_linux/packages",
        "target",
        "/",
        verbose,
        jobs,
    ):
        return False
    print("installing target packages from within chroot environment: ok")
    return True

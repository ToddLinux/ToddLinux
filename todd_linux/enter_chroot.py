import os
import pathlib

from .sign_lfs import assert_signed

BASE_DIR = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{BASE_DIR}/.."
SCRIPTS_FOLDER = "scripts"


def enter_chroot(lfs_dir) -> bool:
    os.chdir(lfs_dir)

    assert_signed()

    if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /bin/bash") != 0:
        return False
    return True


def enter_bootstrap_chroot_python(lfs_dir: str, verbose: bool, jobs: int) -> bool:
    print("entering chroot to bootstrap python: ...")
    if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /usr/bin/python3 /{SCRIPTS_FOLDER}/todd_linux/chroot_scripts/bootstrap_chroot_python.py") != 0:
        return False
    return True


def enter_install_from_chroot(lfs_dir: str, verbose: bool, jobs: int) -> bool:
    print("entering chroot to install from chroot: ...")
    if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /usr/bin/python3 /{SCRIPTS_FOLDER}/main.py / --chroot {'-v' if verbose else ''} -j {jobs}") != 0:
        return False
    return True

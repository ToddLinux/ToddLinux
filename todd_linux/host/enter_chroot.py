import os
import pathlib

__all__ = ["enter_chroot", "enter_install_from_chroot", "enter_install_from_chroot"]

BASE_DIR = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{BASE_DIR}/../.."
SCRIPTS_FOLDER = "scripts"

PATH = "/bin:/usr/bin:/sbin:/usr/sbin"


def enter_chroot(lfs_dir) -> bool:
    os.chdir(lfs_dir)

    if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH={PATH} /bin/bash") != 0:
        return False
    return True


def enter_bootstrap_chroot_python(lfs_dir: str) -> bool:
    print("entering chroot to bootstrap python: ...")
    if (
        os.system(
            f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH={PATH} /usr/bin/python3 /{SCRIPTS_FOLDER}/todd_linux/chroot/bootstrap_chroot_python.py"
        )
        != 0
    ):
        return False
    return True


def enter_install_from_chroot(lfs_dir: str, verbose: bool, jobs: int) -> bool:
    print("entering chroot to install from chroot: ...")
    if (
        os.system(
            f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH={PATH} /usr/bin/python3 /{SCRIPTS_FOLDER}/main.py / --chroot {'-v' if verbose else ''} -j {jobs}"
        )
        != 0
    ):
        return False
    return True

import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{BASE_DIR}/../.."
SCRIPTS_FOLDER = "scripts"


def install_required_packages_from_chroot(lfs_dir: str, verbose: bool, jobs: int) -> bool:
    if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /usr/bin/python3 /{SCRIPTS_FOLDER}/host/setup/chroot_scripts/install_from_chroot.py {'-v' if verbose else ''} -j {jobs}") != 0:
        return False
    return True

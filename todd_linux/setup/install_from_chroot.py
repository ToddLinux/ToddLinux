import os
import pathlib

FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{FILE_DIR_PATH}/../.."
SCRIPTS_FOLDER = "scripts"


def install_required_packages_from_chroot(lfs_dir: str, verbose: bool, jobs: int, measure_time: bool) -> bool:
    if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /usr/bin/python3 /{SCRIPTS_FOLDER}/host/setup/chroot_scripts/install_from_chroot.py {'-t' if measure_time else ''} {'-v' if verbose else ''} -j {jobs}") != 0:
        return False
    return True

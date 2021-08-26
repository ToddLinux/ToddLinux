import os
import subprocess
import pathlib
from argparse import ArgumentParser
from typing import Optional

from .install_from_host import install_required_packages_from_host
from .install_from_chroot import install_required_packages_from_chroot
from .check_req import check_all_reqs
from .create_directory_layout import create_directory_layout
from .prepare_chroot import prepare_chroot


FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
SIGN_FILE = "lfs_sign.lock"


def setup() -> bool:
    parser = ArgumentParser(description="Run Todd Linux build system")
    parser.add_argument('path', help='path to chroot environment', type=str)
    parser.add_argument('-t', '--time', help='measure build time', action='store_true')
    parser.add_argument('-v', '--verbose', help='print messages from underlaying build processes', action='store_true')
    parser.add_argument('-j', '--jobs', help='number of concurrent jobs (if not specified `nproc` output is used)')
    args = parser.parse_args()
    verbose: bool = args.verbose
    measure_time: bool = args.time
    jobs: Optional[int] = args.jobs
    lfs_dir = os.path.abspath(args.path)
    os.chdir(lfs_dir)

    # use nproc to determin amount of threads to use
    if jobs is None:
        output = subprocess.check_output("nproc", stderr=subprocess.STDOUT).decode()
        jobs = int(output)

    # "don't fuck up my system"-protection
    if not os.path.exists(SIGN_FILE):
        print(f"Error: provided lfs path '{os.getcwd()}' doesn't have sign file; use sign_lfs.py to create one")
        return False

    if os.geteuid() != 0:
        print("Warning: executing script without root privileges; the script will perform all possible actions and fail when root rights are required")

    if not check_all_reqs():
        return False

    create_directory_layout()

    if not install_required_packages_from_host(lfs_dir, verbose, jobs, measure_time):
        return False

    if not prepare_chroot(lfs_dir):
        return False

    if not install_required_packages_from_chroot(lfs_dir, verbose, jobs, measure_time):
        return False

    return True

import argparse
import os
import subprocess
import pathlib
import pwd
import grp
import sys


from argparse import ArgumentParser
from typing import Callable, Optional, Tuple, Callable, List

from .install_from_host import install_required_packages_from_host
from .install_from_chroot import install_required_packages_from_chroot
from .check_req import check_all_reqs
from .prepare_chroot import prepare_chroot


FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
SIGN_FILE = "lfs_sign.lock"


def install_unelevated(lfs_dir: str, verbose: bool, jobs: int, measure_time: bool) -> bool:
    demote(*get_ids())

    if not install_required_packages_from_host(lfs_dir, verbose, jobs, measure_time):
        return False

    return True


def install_elevated(lfs_dir: str, verbose: bool, jobs: int, measure_time: bool) -> bool:
    if not install_required_packages_from_host(lfs_dir, verbose, jobs, measure_time):
        return False

    if not prepare_chroot(lfs_dir):
        return False

    if not install_required_packages_from_chroot(lfs_dir, verbose, jobs, measure_time):
        return False

    return True


def get_ids() -> Tuple[int, int]:
    uid = os.environ.get("SUDO_UID") if "SUDO_UID" in os.environ else os.getuid()
    gid = os.environ.get("SUDO_GID") if "SUDO_GID" in os.environ else os.getgid()
    return int(uid), int(gid)


def get_user_and_group() -> Tuple[str, str]:
    uid, gid = get_ids()
    username = pwd.getpwuid(uid)[0]
    group = grp.getgrgid(gid).gr_name
    return username, group


def change_lfs_owner(lfs_dir: str) -> None:
    user, group = get_user_and_group()
    os.system(f"chown -R {user}:{group} {lfs_dir}")
    pass


def demote(user_uid: int, user_gid: int) -> None:
    os.setgid(user_gid)
    os.setuid(user_uid)


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

    change_lfs_owner(lfs_dir)

    # use nproc to determine amount of threads to use
    if jobs is None:
        output = subprocess.check_output("nproc", stderr=subprocess.STDOUT).decode()
        jobs = int(output)

    # "don't fuck up my system"-protection
    if not os.path.exists(SIGN_FILE):
        print(f"Error: provided lfs path '{os.getcwd()}' doesn't have sign file; use sign_lfs.py to create one")
        return False

    # TODO: terminate on insufficient privileges
    if os.geteuid() != 0:
        print("Warning: executing script without root privileges; the script will perform all possible actions and fail when root rights are required")

    if not check_all_reqs():
        return False

    # fork and install software as unelevated user
    newpid = os.fork()
    if newpid == 0:
        success = install_unelevated(lfs_dir, verbose, jobs, measure_time)
        return success
    else:
        _, exit_code = os.waitpid(newpid, 0)
        if exit_code != 0:
            return False

        success = install_elevated(lfs_dir, verbose, jobs, measure_time)
        return success

import os
import subprocess
import pathlib
import pwd

from argparse import ArgumentParser
from typing import Optional, Tuple, Union
from pwd import struct_passwd

from .install_from_host import install_required_packages_from_host
from .install_from_chroot import install_required_packages_from_chroot
from .check_req import check_all_reqs
from .prepare_chroot import prepare_chroot


FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()

# system protection
SIGN_FILE = "lfs_sign.lock"


def install_unelevated(build_user: struct_passwd, lfs_dir: str, verbose: bool, jobs: int, measure_time: bool) -> bool:
    """
    Installs software as unelevated user

    :param build_user: the user by which the software is being build and installed
    :param lfs_dir: installation directory
    :param verbose: if true print build messages
    :param jobs: number of build jobs
    :param measure_time: measure installation time
    :return: true if successfully installed false otherwise
    """
    uid = build_user.pw_uid
    gid = build_user.pw_gid
    demote(uid, gid)

    if not install_required_packages_from_host(lfs_dir, verbose, jobs, measure_time):
        return False

    return True


def install_elevated(lfs_dir: str, verbose: bool, jobs: int, measure_time: bool) -> bool:
    """
    Installs software as elevated user

    :param lfs_dir: installation directory
    :param verbose: if true print build messages
    :param jobs: number of build jobs
    :param measure_time: measure installation time
    :return: true if successfully installed false otherwise
    """
    if not prepare_chroot(lfs_dir):
        return False

    if not install_required_packages_from_chroot(lfs_dir, verbose, jobs, measure_time):
        return False

    return True


def get_build_user() -> Union[None, struct_passwd]:
    """
    Fetches the information about build user

    :return: user information if can be obtained, None otherwise
    """
    try:
        lfs_user = pwd.getpwnam("lfs_build")
        return lfs_user
    except:
        return None


def change_lfs_owner(user: struct_passwd, lfs_dir: str) -> None:
    """
    Changes the owner of directory

    :param user: user information
    :param lfs_dir: directory path
    """
    uid = user.pw_uid
    gid = user.pw_gid
    os.system(f"chown -R {uid}:{gid} {lfs_dir}")


def demote(user_uid: int, user_gid: int) -> None:
    """
    Change process UID and GID to non-privileged user

    :param user_uid: UID of user the process is being demoted to
    :param user_gid: GID of user the process is being demoted to
    """
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
    build_user = get_build_user()

    os.chdir(lfs_dir)

    if os.geteuid() != 0:
        print("Insufficient privlieges")
        return False

    # if user doesn't exist exit with error
    if not build_user:
        print("No such user: lfs_build")
        print("Refer to Wiki on how to add build user")
        return False

    # lfs directory must be owned by build user
    change_lfs_owner(build_user, lfs_dir)

    # use nproc to determine amount of threads to use
    if jobs is None:
        output = subprocess.check_output("nproc", stderr=subprocess.STDOUT).decode()
        jobs = int(output)

    # "don't fuck up my system"-protection
    if not os.path.exists(SIGN_FILE):
        print(f"Error: provided lfs path '{os.getcwd()}' doesn't have sign file; use sign_lfs.py to create one")
        return False

    if not check_all_reqs():
        return False

    newpid = os.fork()
    if newpid == 0:
        # install software as unelevated user
        success = install_unelevated(build_user, lfs_dir, verbose, jobs, measure_time)
        return success
    else:
        _, exit_code = os.waitpid(newpid, 0)
        if exit_code != 0:
            return False

        success = install_elevated(lfs_dir, verbose, jobs, measure_time)
        return success

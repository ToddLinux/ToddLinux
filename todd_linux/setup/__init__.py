import os
import subprocess
import pathlib
import pwd

from typing import Optional, Union
from pwd import struct_passwd

from .enter_chroot import enter_chroot
from .sign_lfs import create_sign_file
from .install_from_host import install_required_packages_from_host
from .install_from_chroot import install_required_packages_from_chroot
from .check_req import check_all_reqs
from .prepare_chroot import prepare_chroot
from todd.todd import load_packages, PKG_CACHE_DIRECTORY, fetch_package_sources


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


# TODO: still downloading sources multiple times
def prefetch_packages(lfs_dir: str) -> bool:
    """
    Download all source packages

    :param lfs_dir: package management system root directory
    :return: true if successfully downloaded all package sources false otherwise
    """
    packages = load_packages(f"{FILE_DIR_PATH}/packages")
    cache_dir = f"{lfs_dir}/{PKG_CACHE_DIRECTORY}"

    if not os.path.isdir(f"{lfs_dir}/{PKG_CACHE_DIRECTORY}"):
        os.makedirs(cache_dir)

    for (_, package) in packages.items():
        package_dest_dir = f"{cache_dir}/{package.name}/{package.version}"
        if not fetch_package_sources(package, package_dest_dir):
            return False

    return True


def setup(
    lfs_dir: str,
    verbose: bool,
    measure_time: bool,
    prefetch: bool,
    jobs: Optional[int]
) -> bool:
    os.chdir(lfs_dir)
    build_user = get_build_user()

    if os.geteuid() != 0:
        print("Insufficient privlieges")
        return False

    # if user doesn't exist exit with error
    if not build_user:
        print("No such user: lfs_build")
        print("Refer to Wiki on how to add build user")
        return False

    if prefetch:
        prefetch_packages(lfs_dir)

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

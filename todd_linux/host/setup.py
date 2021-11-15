import os
import subprocess
import pathlib
import pwd
from typing import Optional, Union
from pwd import struct_passwd

from .install_from_host import install_required_packages_from_host
from .check_req import check_all_reqs
from .sign_lfs import assert_signed
from .prepare_chroot import prepare_chroot
from .enter_chroot import enter_bootstrap_chroot_python, enter_install_from_chroot
from ..todd.todd import fetch_package_sources, load_packages

__all__ = ["setup_host"]

BASE_DIR = pathlib.Path(__file__).parent.resolve()


def install_unelevated(build_user: struct_passwd, lfs_dir: str, verbose: bool, jobs: int) -> bool:
    """
    Installs software as unelevated user

    :param build_user: the user by which the software is being build and installed
    :param lfs_dir: installation directory
    :param verbose: if true print build messages
    :param jobs: number of build jobs
    :return: True if successfully installed False otherwise
    """
    uid = build_user.pw_uid
    gid = build_user.pw_gid
    demote(uid, gid)

    if not install_required_packages_from_host(lfs_dir, verbose, jobs):
        return False

    return True


def install_elevated(lfs_dir: str, verbose: bool, jobs: int) -> bool:
    """
    Installs software as elevated user

    :param lfs_dir: installation directory
    :param verbose: if true print build messages
    :param jobs: number of build jobs
    :return: True if successfully installed False otherwise
    """
    if not prepare_chroot(lfs_dir):
        return False

    if not enter_bootstrap_chroot_python(lfs_dir, verbose, jobs):
        return False

    if not enter_install_from_chroot(lfs_dir, verbose, jobs):
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


# TODO: still downloading sources multiple times -> kinda pointless atm
def prefetch_packages(lfs_dir: str) -> bool:
    """
    Download all source packages

    :param lfs_dir: package management system root directory
    :return: True if successfully downloaded all package sources False otherwise
    """
    packages = load_packages(f"{BASE_DIR}/packages")

    for package in packages.values():
        if not fetch_package_sources(lfs_dir, package):
            return False

    return True


def setup_host(
    lfs_dir: str,
    verbose: bool,
    prefetch: bool,
    jobs: Optional[int]
) -> bool:
    os.chdir(lfs_dir)
    build_user = get_build_user()

    if os.geteuid() != 0:
        print("Insufficient privileges")
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

    assert_signed(".")

    if not check_all_reqs():
        return False

    newpid = os.fork()
    if newpid == 0:
        # install software as unelevated user
        success = install_unelevated(build_user, lfs_dir, verbose, jobs)
        return success
    else:
        _, exit_code = os.waitpid(newpid, 0)
        if exit_code != 0:
            return False

        success = install_elevated(lfs_dir, verbose, jobs)
        return success

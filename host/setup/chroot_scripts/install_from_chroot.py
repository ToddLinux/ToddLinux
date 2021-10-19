# THIS SCRIPT HAS TO BE EXECUTED FROM WITHIN CHROOT ENVIRONMENT!
import sys
import os
from argparse import ArgumentParser

SCRIPTS_FOLDER = f"/scripts"
sys.path.append(SCRIPTS_FOLDER)
from pkg_manager import install_packages  # nopep8


SIGN_FILE = "lfs_sign.lock"
REQUIRED_PACKAGES = [
    "libstdcpp_pass2",
    "gettext",
    "bison",
    "perl",
    "python3_pass2",
    "texinfo",
    "util-linux"
]


def main() -> bool:
    parser = ArgumentParser(description="Install host tools from within chroot environemnt")
    parser.add_argument('-t', '--time', help='measure build time', action='store_true')
    parser.add_argument('-v', '--verbose', help='print messages from underlaying build processes', action='store_true')
    parser.add_argument('-j', '--jobs', help='number of concurrent jobs (if not specified `nproc` output is used)')
    args = parser.parse_args()
    verbose: bool = args.verbose
    measure_time: bool = args.time
    jobs: int = args.jobs

    os.chdir("/")
    print("installing tools from within chroot environment: ...")
    # "don't fuck up my system"-protection
    if not os.path.exists(SIGN_FILE):
        print(f"Error: chroot root path doesn't contain the sign file; Are you sure you're using this script from within the chroot environment; use sign_lfs.py to create one")
        return False

    if not install_packages(REQUIRED_PACKAGES, f"{SCRIPTS_FOLDER}/host/setup/packages", "chroot", "/", verbose, jobs, measure_time):
        return False
    print("installing tools from within chroot environment: ok")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

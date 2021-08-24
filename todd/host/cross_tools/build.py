# See LICENSE for license details.
import sys
import os
import shutil
import csv
import pathlib
import subprocess
import time
from typing import Optional, List

from datetime import timedelta
from time import time
from argparse import ArgumentParser


FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
LOCK_FILE = "builds/builds.lock"
DIRECTORY_LAYOUT = ["bin", "etc", "lib", "lib64", "sbin", "usr", "var", "tools", "builds"]


# load all required builds
def get_builds() -> List[Build]:
    with open(f"{FILE_DIR_PATH}/builds.csv", "r", newline="") as file:
        raw_builds = csv.DictReader(file, delimiter=";")
        builds = [Build(build["package"], build["src_packages"],
                        build["build_script"]) for build in raw_builds]
    return builds


# create folders in root
def create_directory_layout():
    print("creating minimal directory layout")
    for folder in DIRECTORY_LAYOUT:
        if not os.path.isdir(folder):
            os.mkdir(folder)


def build_all_required_packages(lfs_dir: str, quiet_mode: bool) -> bool:
    output_redirect = "/dev/null" if quiet_mode else None

    create_directory_layout()
    builds = get_builds()
    finished_builds = get_finished_builds()
    with open(LOCK_FILE, "a", newline="") as file:
        for build in builds:
            if build.package in finished_builds:
                print(f"building {build.package}:\talready built")
                continue

            if not build_package(build, lfs_dir, output_redirect):
                return False

            # package has been successfully built
            file.write(f"{build.package}\n")
            file.flush()

    return True


def main() -> int:
    # handle command line arguments
    parser = ArgumentParser(description='Build cross toolchain and required tools')
    parser.add_argument('path', help='path to chroot environment', type=str)
    parser.add_argument('-time', help='measure build time', action='store_true')
    parser.add_argument('-quiet', help='don\'t print messages from underlaying processes', action='store_true')
    parser.add_argument('-jobs', help='number of concurrent jobs (if not specified `nproc` output is used)')

    args = parser.parse_args()
    quiet_mode = args.quiet
    measure_time = args.time
    jobs = args.jobs
    lfs_dir = os.path.abspath(args.path)
    os.chdir(lfs_dir)
    if not os.path.exists("lfs_sign.loc"):
        print("Error: provided lfs path doesn't have sign file; use sign_lfs.py to create one")
        return 1

    # use nproc to determin amount of threads to use
    if jobs is None:
        output = subprocess.check_output("nproc", stderr=subprocess.STDOUT).decode()
        jobs = int(output)
    os.environ["LFS"] = lfs_dir
    os.environ["LFS_TGT"] = "x86_64-lfs-linux-gnu"
    os.environ["MAKEFLAGS"] = f"-j{jobs}"
    os.environ["PATH"] = lfs_dir + "/tools/bin:" + os.environ["PATH"]

    start = time()
    ok = build_all_required_packages(lfs_dir, quiet_mode)
    end = time()

    if measure_time:
        print("host_cross_tool_chain time:", timedelta(seconds=(end - start)))

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

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


# represents build of <package> as found in builds.csv
# executing <build_script> after providing all <src_packages>
class Build:
    def __init__(self, package: str, src_packages: str, build_script: str):
        self.package = package
        self.src_packages = src_packages.split(":")
        self.build_script = build_script

    def __repr__(self):
        return f"<Build package: '{self.package}' src_packages: {self.src_packages} build_script: '{self.build_script}'>"


# read already completed builds
def get_finished_builds() -> List[str]:
    finished_builds = []
    if os.path.isfile(LOCK_FILE):
        with open(LOCK_FILE, "r", newline="") as file:
            finished_builds = [line.strip() for line in file.readlines()]
    return finished_builds


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


# copy all sources for one build
def copy_sources(build: Build):
    for source in build.src_packages:
        print(f"building {build.package}:\tcopying source '{source}'...                \r", end="")
        # find archive
        dirs = os.listdir(f"src/{source}")
        if len(dirs) != 1:
            print(f"building {build.package}:\tcopying failed; not only one archive found             ", end="")
            return False
        shutil.copy(f"src/{source}/{dirs[0]}", f"builds/{build.package}")


# perform all required step for build a single package
# redirect all output (stdout and stderr) from the build script to <output_redirect> if provided
def build_package(build: Build, lfs_dir: str, output_redirect: Optional[str]) -> bool:
    print(f"building {build.package}:\tcreating package folder...\r", end="")
    if os.path.isdir(f"builds/{build.package}"):
        shutil.rmtree(f"builds/{build.package}")
    os.mkdir(f"builds/{build.package}")

    copy_sources(build)

    print(f"building {build.package}:\texecute build script...                      \r", end="")
    os.chdir(f"builds/{build.package}")

    cmd_suffix = ""
    if output_redirect is not None:
        cmd_suffix = f" >{output_redirect} 2>&1"
    if os.system(f"{FILE_DIR_PATH}/build_scripts/{build.build_script}" + cmd_suffix) != 0:
        print(f"building {build.package}:\tbuild script failed...                 ", end="")
        return False

    print(f"building {build.package}:\tok                      ")
    # post build cleanup
    os.chdir(lfs_dir)
    shutil.rmtree(f"builds/{build.package}")
    return True


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

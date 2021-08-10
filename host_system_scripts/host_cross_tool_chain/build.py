# See LICENSE for license details.
import sys
import os
import shutil
import csv
import pathlib
import subprocess
import time

from datetime import timedelta
from time import time


file_dir_path = pathlib.Path(__file__).parent.resolve()

LOCK_FILE = "builds/builds.lock"
OPTIONS = ["-time", "-quiet"]
DIRECTORY_LAYOUT = ["bin", "etc", "lib", "lib64",
                    "sbin", "usr", "var", "tools", "builds"]


class Build:
    def __init__(self, package: str, src_packages: str, build_script: str):
        self.package = package
        self.src_packages = src_packages.split(":")
        self.build_script = build_script

    def __repr__(self):
        return f"<Build package: '{self.package}' src_packages: {self.src_packages} build_script: '{self.build_script}'>"


def get_finished_builds():
    finished_builds = []
    # read already completed builds
    if os.path.isfile(LOCK_FILE):
        with open(LOCK_FILE, "r", newline="") as file:
            finished_builds = [line.strip() for line in file.readlines()]
    return finished_builds


def get_builds():
    with open(f"{file_dir_path}/builds.csv", "r", newline="") as file:
        raw_builds = csv.DictReader(file, delimiter=";")
        builds = [Build(build["package"], build["src_packages"],
                        build["build_script"]) for build in raw_builds]
    return builds


def create_directory_layout():
    print("creating minimal directory layout")
    for folder in DIRECTORY_LAYOUT:
        if not os.path.isdir(folder):
            os.mkdir(folder)


def copy_sources(build: Build):
    for source in build.src_packages:
        print(
            f"building {build.package}:\tcopying source '{source}'...                \r", end="")
        # find archive
        dirs = os.listdir(f"src/{source}")
        if len(dirs) != 1:
            print(
                f"building {build.package}:\tcopying failed; not only one archive found             ", end="")
            return False
        shutil.copy(f"src/{source}/{dirs[0]}", f"builds/{build.package}")

def build_package(build: Build, lfs_dir: str, output_redirect: str) -> bool:
    print(f"building {build.package}:\tcreating package folder...\r", end="")
    if os.path.isdir(f"builds/{build.package}"):
        shutil.rmtree(f"builds/{build.package}")
    os.mkdir(f"builds/{build.package}")

    copy_sources(build)

    print(
        f"building {build.package}:\texecute build script...                      \r", end="")
    os.chdir(f"builds/{build.package}")

    if os.system(f"{file_dir_path}/build_scripts/{build.build_script}" + output_redirect) != 0:
        print(
            f"building {build.package}:\tbuild script failed...                 ", end="")
        return False

    print(f"building {build.package}:\tok                      ")
    os.chdir(lfs_dir)
    shutil.rmtree(f"builds/{build.package}")

    return True


def build_targets(lfs_dir: str, quiet_mode: bool) -> bool:
    output_redirect = " >/dev/null 2>&1" if quiet_mode else ""
    os.chdir(lfs_dir)

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

            # package built
            file.write(f"{build.package}\n")
            file.flush()

    return True


def set_environ_variables(lfs_dir: str):
    output = subprocess.check_output(
        "nproc", stderr=subprocess.STDOUT).decode()
    n_proc = 1 if output == "1" else int(output) - 1

    os.environ["LFS"] = lfs_dir
    os.environ["LFS_TGT"] = "x86_64-lfs-linux-gnu"
    os.environ["MAKEFLAGS"] = f"-j{n_proc}"
    os.environ["PATH"] = lfs_dir + "/tools/bin:" + os.environ["PATH"]


def print_usage(script_name: str):
    print(f"Usage: {script_name} [options]... [path]")
    print(f"Options")
    print(f"  -time   measure time")
    print(f"  -quiet  don't print building messages from child processes")


def main() -> int:
    args = [a for a in sys.argv if a not in OPTIONS]
    quiet_mode = "-quiet" in sys.argv
    measure_time = "-time" in sys.argv

    if len(args) < 2:
        print("Missing path")
        print_usage(args[0])
        sys.exit(1)

    lfs_dir = os.path.abspath(args[1])
    set_environ_variables(lfs_dir)
    start = time()
    ok = build_targets(lfs_dir, quiet_mode)
    end = time()
    if measure_time:
        print("host_cross_tool_chain time:", timedelta(seconds=(end - start)))

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

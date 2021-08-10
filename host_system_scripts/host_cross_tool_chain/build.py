# See LICENSE for license details.
import sys
import os
import shutil
import csv
import pathlib
import subprocess
import time

from datetime import timedelta


file_dir_path = pathlib.Path(__file__).parent.resolve()

OPTIONS = ["-time", "-quiet"]


class Build:
    def __init__(self, package: str, src_packages: str, build_script: str):
        self.package = package
        self.src_packages = src_packages.split(":")
        self.build_script = build_script

    def __repr__(self):
        return f"<Build package: '{self.package}' src_packages: {self.src_packages} build_script: '{self.build_script}'>"


# fails when one fails
def build_targets(lfs_dir: str, quiet_mode: bool) -> bool:
    output_redirect = " >/dev/null 2>&1" if quiet_mode else ""
    os.chdir(lfs_dir)

    print("creating minimal directory layout")
    folders = ["bin", "etc", "lib", "lib64",
               "sbin", "usr", "var", "tools", "builds"]
    for folder in folders:
        if not os.path.isdir(folder):
            os.mkdir(folder)

    # start build
    with open(f"{file_dir_path}/builds.csv", "r", newline="") as file:
        raw_builds = csv.DictReader(file, delimiter=";")
        builds = [Build(build["package"], build["src_packages"],
                        build["build_script"]) for build in raw_builds]

    finished_builds = []
    if os.path.isfile("builds/builds.lock"):
        with open("builds/builds.lock", "r", newline="") as file:
            # read already completed builds
            finished_builds = [line.strip() for line in file.readlines()]

    with open("builds/builds.lock", "a", newline="") as file:
        for build in builds:
            if build.package in finished_builds:
                print(f"building {build.package}:\talready built")
                continue
            print(
                f"building {build.package}:\tcreating package folder...\r", end="")
            if os.path.isdir(f"builds/{build.package}"):
                shutil.rmtree(f"builds/{build.package}")
            os.mkdir(f"builds/{build.package}")

            # copy all sources
            for source in build.src_packages:
                print(
                    f"building {build.package}:\tcopying source '{source}'...                \r", end="")
                # find archive
                dirs = os.listdir(f"src/{source}")
                if len(dirs) != 1:
                    print(
                        f"building {build.package}:\tcopying failed; not only one archive found             ", end="")
                    return False
                shutil.copy(
                    f"src/{source}/{dirs[0]}", f"builds/{build.package}")

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

            # package built
            file.write(f"{build.package}\n")
            file.flush()
    return True


def set_environ_variables(lfs_dir):
    os.environ["LFS"] = lfs_dir
    os.environ["LFS_TGT"] = "x86_64-lfs-linux-gnu"
    output = subprocess.check_output(
        "nproc", stderr=subprocess.STDOUT).decode()
    n_proc = 1 if output == "1" else int(output) - 1
    os.environ["MAKEFLAGS"] = f"-j{n_proc}"
    os.environ["PATH"] = lfs_dir + "/tools/bin:" + os.environ["PATH"]


def main() -> int:
    if len(sys.argv) < 2:
        raise ValueError("Add path to LFS mount point as first argument")

    args = [a for a in sys.argv if a not in OPTIONS]
    lfs_dir = os.path.abspath(args[1])
    quiet_mode = "-quiet" in sys.argv
    measure_time = "-time" in sys.argv

    set_environ_variables(lfs_dir)
    start = time.time()
    ok = build_targets(lfs_dir, quiet_mode)
    end = time.time()
    if measure_time:
        print("host_cross_tool_chain time:", timedelta(seconds=(end - start)))

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

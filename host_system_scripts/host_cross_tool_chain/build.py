# See LICENSE for license details.
import sys
import os
import shutil
import csv
import pathlib
import subprocess

file_dir_path = pathlib.Path(__file__).parent.resolve()


class Build:
    def __init__(self, package: str, src_packages: str, build_script: str):
        self.package = package
        self.src_packages = src_packages.split(":")
        self.build_script = build_script

    def __repr__(self):
        return f"<Build package: '{self.package}' src_packages: {self.src_packages} build_script: '{self.build_script}'>"


def build_targets(lfs_dir: str, quiet_mode: bool) -> bool:
    all_ok = True
    output_redirect = " >/dev/null 2>&1" if quiet_mode else ""
    os.chdir(lfs_dir)

    print("creating minimal directory layout")
    folders = ["bin", "etc", "lib", "lib64",
               "sbin", "usr", "var", "tools", "builds"]
    # folders = ["builds", "tools"]
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
                print(f"building {build.package}: already built")
                continue
            try:
                print(
                    f"building {build.package}: creating package folder...\r", end="")
                if os.path.isdir(f"builds/{build.package}"):
                    shutil.rmtree(f"builds/{build.package}")
                os.mkdir(f"builds/{build.package}")

                # copy all sources
                for source in build.src_packages:
                    print(
                        f"building {build.package}: copying source '{source}'...                \r", end="")
                    # find archive
                    dirs = os.listdir(f"src/{source}")
                    if len(dirs) != 1:
                        print(
                            f"building {build.package}: copying failed; not only one archive found             ", end="")
                        raise ValueError
                    shutil.copy(
                        f"src/{source}/{dirs[0]}", f"builds/{build.package}")
            except ValueError:
                all_ok = False
                continue

            print(
                f"building {build.package}: execute build script...                      \r", end="")
            os.chdir(f"builds/{build.package}")
            if os.system(f"{file_dir_path}/build_scripts/{build.build_script}" + output_redirect) != 0:
                print(
                    f"building {build.package}: build script failed...                 ", end="")
                all_ok = False
                continue
            print(f"building {build.package}: ok                      ")
            os.chdir(lfs_dir)

            # package built
            file.write(f"{build.package}\n")
            file.flush()
    return all_ok


def set_environ_variables(lfs_dir):
    os.environ["LFS"] = lfs_dir
    os.environ["LFS_TGT"] = "x86_64-lfs-linux-gnu"
    output = subprocess.check_output(
        "nproc", stderr=subprocess.STDOUT).decode()
    os.environ["MAKEFLAGS"] = f"-j{output}"
    os.environ["PATH"] = lfs_dir + "/tools/bin:" + os.environ["PATH"]


def main() -> int:
    if len(sys.argv) < 2:
        raise ValueError("Add path to LFS mount point as first argument")

    args = [a for a in sys.argv if a != "-quiet"]
    lfs_dir = os.path.abspath(args[1])
    quiet_mode = "-quiet" in sys.argv

    set_environ_variables(lfs_dir)
    return 0 if build_targets(lfs_dir, quiet_mode) else 1


if __name__ == "__main__":
    sys.exit(main())

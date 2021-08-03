# See LICENSE for license details.
import sys
import os
import shutil
import csv
import pathlib

file_dir_path = pathlib.Path(__file__).parent.resolve()


class Build:
    def __init__(self, target: str, src_packages: str, build_script: str):
        self.target = target
        self.src_packages = src_packages.split(":")
        self.build_script = build_script

    def __repr__(self):
        return f"<Build target: '{self.target}' src_packages: {self.src_packages} build_script: '{self.build_script}'>"


def main():
    if len(sys.argv) < 2:
        raise ValueError("Add path to LFS mount point as first argument")
    lfs_dir = sys.argv[1]
    os.chdir(lfs_dir)

    print("creating minimal directory layout")
    folders = ["bin", "etc", "lib", "lib64",
               "sbin", "usr", "var", "tools", "builds"]
    for folder in folders:
        os.mkdir(folder)

    # start build
    with open(f"{file_dir_path}/builds.csv", "r", newline="") as file:
        raw_builds = csv.DictReader(file, delimiter=";")
        builds = [Build(build["target"], build["src_packages"],
                        build["build_script"]) for build in raw_builds]

    for build in builds:
        try:
            print(f"building {build.target}: creating target folder...\r")
            os.mkdir(f"builds/{build.target}")

            for source in build.src_packages:
                print(
                    f"building {build.target}: copying source '{source}'...                \r")
                # find archive
                dirs = os.listdir(f"src/{source}")
                if len(dirs) != 1:
                    print(
                        f"building {build.target}: copying failed; not only one archive found             ")
                    raise ValueError
                shutil.copy(
                    f"src/{source}/{dirs[0]}", f"builds/{build.target}")
        except ValueError:
            continue

        print(
            f"building {build.target}: execute build script...                      \r")
        if os.system(f"{file_dir_path}/build_scripts/{build.target}.sh") != 0:
            print(
                f"building {build.target}: build script failed...                 \r")
        print(f"building {build.target}: ok                      ")


if __name__ == "__main__":
    main()

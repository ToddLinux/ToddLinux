# See LICENSE for license details.
import sys
import os
import yaml
import pathlib

file_dir_path = pathlib.Path(__file__).parent.resolve()


def main():
    if len(sys.argv) < 2:
        raise ValueError("Add path to LFS mount point as first argument")
    lfs_dir = sys.argv[1]

    print("creating minimal directory layout")
    os.chdir(lfs_dir)
    folders = ["bin", "etc", "lib", "lib64", "sbin", "usr", "var", "tools"]
    for folder in folders:
        os.mkdir(folder)

    # start build
    with open(f"{file_dir_path}/build.yaml", "r") as file:
        build = yaml.safe_load(file)

    print(build)


if __name__ == "__main__":
    main()

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
    os.chdir(lfs_dir)

    # print("creating minimal directory layout")
    # folders = ["bin", "etc", "lib", "lib64", "sbin", "usr", "var", "tools"]
    # for folder in folders:
    #     os.mkdir(folder)

    # start build
    with open(f"{file_dir_path}/build.yaml", "r") as file:
        builds = yaml.safe_load(file)

    os.chdir("src")
    for build in builds:
        print(f"building {build['package']}: extracting...\r")
        os.chdir(build["package"])
        # find archive
        dirs = os.listdir(".")
        if len(dirs) != 1:
            print(
                f"building {build['package']}: extracting failed; not only one archive found")
            continue

        if os.system(f"tar xf {dirs[0]}"):
            print(f"building {build['package']}: extracting failed")
            continue
        os.remove(dirs[0])

        dirs = os.listdir(".")
        while(len(dirs) == 1):
            print(dirs[0])
            os.chdir(dirs[0])
            dirs = os.listdir(".")
        print(os.getcwd())
        break
        os.chdir(lfs_dir)


if __name__ == "__main__":
    main()

# See LICENSE for license details.
import sys
import os


def main():
    if len(sys.argv) < 2:
        raise ValueError("Add path to LFS mount point as first argument")
    lfs_dir = sys.argv[1]

    os.chdir(lfs_dir)
    folders = ["bin", "etc", "lib", "lib64", "sbin", "usr", "var"]
    for folder in folders:
        os.mkdir(folder)


if __name__ == "__main__":
    main()

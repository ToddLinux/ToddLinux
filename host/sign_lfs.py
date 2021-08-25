#!/usr/bin/env python3
import os
from datetime import datetime
import sys
from argparse import ArgumentParser

SIGN_FILE = "lfs_sign.lock"


def main() -> int:
    parser = ArgumentParser(description="Sign LFS Chroot Environment")
    parser.add_argument('path', help='path to lfs chroot environment', type=str)
    parser.add_argument("-f", "--force", help="Add sign file even when folder is not empty", action="store_true")

    args = parser.parse_args()
    force = args.force
    lfs_dir = os.path.abspath(args.path)
    os.chdir(lfs_dir)

    if len(os.listdir(".")) != 0:
        if force:
            print("Warning: adding sign file to non-empty directory")
        else:
            print("lfs path is not empty, use `--force` to overwrite")
            return 1

    with open(SIGN_FILE, "w") as file:
        file.write(f"ToddLinux Chroot Environment created on {datetime.now()}")
    os.chmod(SIGN_FILE, 0o444)
    print(f"added sign file to '{lfs_dir}'")

    return 0


if __name__ == "__main__":
    sys.exit(main())

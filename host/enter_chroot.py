#!/usr/bin/env python3
import os
import sys
from argparse import ArgumentParser

SIGN_FILE = "lfs_sign.lock"


def enter_chroot() -> bool:
    parser = ArgumentParser(description="Enter Todd Linux Chroot Environment")
    parser.add_argument('path', help='path to chroot environment', type=str)

    args = parser.parse_args()
    lfs_dir = os.path.abspath(args.path)
    os.chdir(lfs_dir)

    if not os.path.exists(SIGN_FILE):
        print(f"Error: provided lfs path '{os.getcwd()}' doesn't have sign file; use sign_lfs.py to create one")
        return False

    if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /bin/bash") != 0:
        return False
    return True


if __name__ == "__main__":
    sys.exit(0 if enter_chroot() else 1)

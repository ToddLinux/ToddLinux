#!/usr/bin/env python3
import os
import sys
from argparse import ArgumentParser
from datetime import datetime

# A sign file signifies the root directory of the target system,
# this is where all of the compiled software is going to be installed to,
# it's meant to prevent accidental changes to host system
SIGN_FILE = "lfs_sign.lock"


def create_sign_file(force: bool, lfs_dir: str) -> bool:
    """
    Write sign file to directory.
    If directory is not empty fail, setting force to true overrides this behavior.
    Force option will overwrite a sign file if such exists.

    :param force: force write sign file to directory
    :param lfs_dir: directory to which sign file will be written to
    :return: true if completed successfully false otherwise
    """
    os.chdir(lfs_dir)

    if not os.access('.', os.W_OK):
        print("You don't have sufficient privlieges to write sign file to this directory")
        return False

    # if directory is not empty don't do anything unless asked to
    if os.listdir("."):
        if force:
            print("Warning: adding sign file to non-empty directory")
        else:
            print("lfs path is not empty, use `--force` to overwrite")
            return False

    # you will get exception if you try to write to read-only file
    if os.path.isfile(SIGN_FILE):
        os.remove(SIGN_FILE)

    with open(SIGN_FILE, "w") as file:
        file.write(f"ToddLinux Chroot Environment created on {datetime.now()}\n")

    os.chmod(SIGN_FILE, 0o444)  # read for all
    print(f"added sign file to '{lfs_dir}'")

    return True


def main() -> bool:
    parser = ArgumentParser(description="Sign LFS Chroot Environment")
    parser.add_argument('path', help='path to lfs chroot environment', type=str)
    parser.add_argument("-f", "--force", help="Add sign file even when folder is not empty", action="store_true")

    args = parser.parse_args()
    force = args.force
    lfs_dir = os.path.abspath(args.path)

    return create_sign_file(force, lfs_dir)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

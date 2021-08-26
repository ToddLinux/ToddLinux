#!/usr/bin/env python
import os
import sys

SIGN_FILE = "lfs_sign.lock"


def clean_chroot():
    os.system(r"find /usr/{lib,libexec} -name \*.la -delete")
    os.system("rm -rf /usr/share/{info,man,doc}/*")
    pass


if __name__ == '__main__':
    os.chdir("/")
    if not os.path.exists(SIGN_FILE):
        print("Error: chroot root path doesn't contain the sign file; Are you sure you're using this script from within the chroot environment; use sign_lfs.py to create one")
        sys.exit(1)

    clean_chroot()

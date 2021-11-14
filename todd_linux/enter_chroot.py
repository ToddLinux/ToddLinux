import os

from .sign_lfs import assert_signed

SIGN_FILE = "lfs_sign.lock"


def enter_chroot(lfs_dir) -> bool:
    os.chdir(lfs_dir)

    assert_signed()

    if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /bin/bash") != 0:
        return False
    return True

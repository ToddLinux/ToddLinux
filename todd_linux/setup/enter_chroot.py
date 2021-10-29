import os

SIGN_FILE = "lfs_sign.lock"


def enter_chroot(lfs_dir) -> bool:
    os.chdir(lfs_dir)

    if not os.path.exists(SIGN_FILE):
        print(f"Error: provided lfs path '{os.getcwd()}' doesn't have sign file; use sign_lfs.py to create one")
        return False

    if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /bin/bash") != 0:
        return False
    return True

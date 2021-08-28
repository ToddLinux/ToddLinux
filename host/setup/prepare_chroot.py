# See LICENSE for license details.
import os
from datetime import datetime
import pathlib
import shutil

FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{FILE_DIR_PATH}/../.."

VIRTUAL_KERNEL_FILESYSTEMS = ["dev", "proc", "sys", "run"]
SCRIPTS_FOLDER = "scripts"
LOCK_FILE = "chroot_prepared.lock"


# execute command and raise error at failure
def throw_me(cmd: str) -> None:
    if os.system(cmd) != 0:
        raise ValueError(f"'{cmd}' failed")


def prepare_chroot(lfs_dir: str) -> bool:
    print("preparing chroot environment: ...")
    try:
        if os.geteuid() != 0:
            print("prepare chroot must be executed as root; restart the script with root privileges and it will pick up where it left of")
            return False
        os.chdir(lfs_dir)

        # create additional directories
        for folder in VIRTUAL_KERNEL_FILESYSTEMS:
            if os.path.isdir(folder):
                print(f"'{folder}' is already existent; unmounting and deleting...")
                os.system(f"umount -R -q {folder}")
                shutil.rmtree(folder)
            os.mkdir(folder)

        # set owner to root
        throw_me(f"chown -R root:root {lfs_dir}")

        # create device nodes
        throw_me(f"mknod -m 600 {lfs_dir}/dev/console c 5 1")
        throw_me(f"mknod -m 666 {lfs_dir}/dev/null c 1 3")

        # mount virtual kernel filesystems
        throw_me(f"mount -v --bind /dev {lfs_dir}/dev")
        throw_me(f"mount -v --bind /dev/pts {lfs_dir}/dev/pts")
        throw_me(f"mount -v -t proc proc {lfs_dir}/proc")
        throw_me(f"mount -v -t sysfs sysfs {lfs_dir}/sys")
        throw_me(f"mount -v -t tmpfs tmpfs {lfs_dir}/run")

        # create symbolic link to /run/shm
        throw_me(f"if [ -h {lfs_dir}/dev/shm ]; then mkdir -pv {lfs_dir}/$(readlink {lfs_dir}/dev/shm); fi")

    except ValueError as e:
        print(str(e))
        return False

    print("copying scripts: ...")
    # delete old scripts folder
    if os.path.isdir(SCRIPTS_FOLDER):
        shutil.rmtree(SCRIPTS_FOLDER)
    shutil.copytree(ROOT_PATH, SCRIPTS_FOLDER)
    print("copying scripts: ok")

    # perform further actions from within chroot environment itself
    if not os.path.exists(LOCK_FILE):
        if os.system(f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /usr/bin/python3 /{SCRIPTS_FOLDER}/host/setup/chroot_scripts/prepare_chroot.py") != 0:
            return False
        with open(LOCK_FILE, "w") as file:
            file.write(f"ToddLinux Chroot Environment successfully prepared on {datetime.now()}")
    else:
        print("internal chroot environment preparation has already been performed")

    print("preparing chroot environment: ok")
    return True

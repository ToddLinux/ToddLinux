import os
import pathlib
import shutil

__all__ = ["prepare_chroot"]

BASE_DIR = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{BASE_DIR}/../.."

VIRTUAL_KERNEL_FILESYSTEMS = ["dev", "proc", "sys", "run"]
SCRIPTS_FOLDER = "scripts"


# execute command and raise error at failure
def throw_me(cmd: str) -> None:
    if os.system(cmd) != 0:
        raise ValueError(f"'{cmd}' failed")


def prepare_chroot(lfs_dir: str) -> bool:
    print("preparing chroot environment: ...")
    try:
        if os.geteuid() != 0:
            print(
                "prepare chroot must be executed as root; restart the script with root privileges and it will pick up where it left of"
            )
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

    print("preparing chroot environment: ok")
    return True

import os
import sys
import shutil
import pathlib

FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()

CHROOT_TOOL_SCRIPTS = "chroot_tool_scripts"


def throw_me(cmd: str) -> None:
    if os.system(cmd) != 0:
        raise ValueError(f"'{cmd}' failed")


def main() -> int:
    try:
        if os.geteuid() != 0:
            print("Script must be executed as root")
            return 1
        if len(sys.argv) < 2:
            print("Set path to LFS as first argument")
            return 1
        # Relative Paths Matter
        lfs_dir = os.path.abspath(sys.argv[1])
        os.chdir(lfs_dir)

        # copy script
        shutil.copytree(
            f"{FILE_DIR_PATH}/{CHROOT_TOOL_SCRIPTS}", f"{lfs_dir}/{CHROOT_TOOL_SCRIPTS}")

        # enter chroot
        throw_me(
            f"chroot {lfs_dir} /usr/bin/env -i HOME=/root PATH=/bin:/usr/bin:/sbin:/usr/sbin /usr/bin/python3 /{CHROOT_TOOL_SCRIPTS}/build_tools.py")

        shutil.rmtree(f"{lfs_dir}/{CHROOT_TOOL_SCRIPTS}")

    except ValueError as e:
        print(str(e))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

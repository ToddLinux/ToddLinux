import os
from datetime import datetime
import sys


def main() -> int:
    if len(sys.argv) < 2:
        raise ValueError("Add path to LFS mount point as first argument")
    lfs_dir = os.path.abspath(sys.argv[1])

    os.chdir(lfs_dir)
    with open("tlh_sign.loc", "w") as file:
        file.write(f"ToddLinux Chroot Environment created on {datetime.now()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

import os
from datetime import datetime

__all__ = ["create_sign_file", "assert_signed"]

# A sign file signifies the root directory of the target system,
# this is where all of the compiled software is going to be installed to,
# it's meant to prevent accidental changes to host system
SIGN_FILE = "lfs_sign.lock"


def create_sign_file(lfs_dir: str, force: bool) -> bool:
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


def assert_signed(lfs_dir: str = "/") -> None:
    assert os.path.exists(f"{lfs_dir}/{SIGN_FILE}"), f"Error: provided lfs path '{os.path.abspath(lfs_dir)}' doesn't have sign file"

import os
import pathlib

from ..todd.todd import install_packages

__all__ = ["install_required_packages_from_host"]

BASE_DIR = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{BASE_DIR}/../.."
PACKAGES_PATH = f"{ROOT_PATH}/todd_linux/packages"


REQUIRED_PACKAGES = [
    "binutils",
    "gcc",
    "linux_headers",
    "glibc",
    "libstdcpp",
    "m4",
    "ncurses",
    "bash",
    "coreutils",
    "diffutils",
    "file",
    "findutils",
    "gawk",
    "grep",
    "gzip",
    "make",
    "patch",
    "sed",
    "tar",
    "xz",
    "binutils_pass2",
    "gcc_pass2",
    "iproute2",
    "iana-etc",
    "inetutils",
    "zlib",
    "openssl",
    "python3.7",
    "python3-setuptools",
    "python3-pip",
]

DIRECTORY_LAYOUT = ["bin", "etc", "lib", "lib64", "sbin", "usr", "var", "tools", "builds"]


# create folders in root
def create_directory_layout():
    print("creating minimal directory layout: ...")
    for folder in DIRECTORY_LAYOUT:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    print("creating minimal directory layout: ok")


def install_required_packages_from_host(lfs_dir: str, verbose: bool, jobs: int) -> bool:
    os.chdir(lfs_dir)
    create_directory_layout()

    os.environ["LFS"] = lfs_dir
    os.environ["LFS_TGT"] = "x86_64-lfs-linux-gnu"
    os.environ["PATH"] = lfs_dir + "/tools/bin:" + os.environ["PATH"]

    return install_packages(REQUIRED_PACKAGES, PACKAGES_PATH, "host", lfs_dir, verbose, jobs)

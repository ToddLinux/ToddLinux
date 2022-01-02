import os
import pathlib

from ..todd.todd import install_packages

__all__ = ["install_required_packages_from_host"]

BASE_DIR = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{BASE_DIR}/../.."
PACKAGES_PATH = f"{ROOT_PATH}/todd_linux/packages"


REQUIRED_PACKAGES = [
    ("binutils", 0),
    ("gcc", 0),
    ("linux_headers", 0),
    ("glibc", 0),
    ("libstdcpp", 0),
    ("m4", 0),
    ("ncurses", 0),
    ("bash", 0),
    ("coreutils", 0),
    ("diffutils", 0),
    ("file", 0),
    ("findutils", 0),
    ("gawk", 0),
    ("grep", 0),
    ("gzip", 0),
    ("make", 0),
    ("patch", 0),
    ("sed", 0),
    ("tar", 0),
    ("xz", 0),
    ("binutils", 1),
    ("gcc", 1),
    ("iproute2", 0),
    ("iana-etc", 0),
    ("inetutils", 0),
    ("zlib", 0),
    ("openssl", 0),
    ("python3.7", 0),
    ("python3-setuptools", 0),
    ("python3-pip", 0),
]

DIRECTORY_LAYOUT = [
    "bin",
    "etc",
    "lib",
    "lib64",
    "sbin",
    "usr",
    "var",
    "tools",
    "builds",
]


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
    os.environ["PATH"] = lfs_dir + "/tools/bin:" + os.environ["PATH"]

    return install_packages(REQUIRED_PACKAGES, "host", lfs_dir, verbose, jobs, PACKAGES_PATH)

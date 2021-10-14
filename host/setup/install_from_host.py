from argparse import ArgumentParser
from typing import Optional
import os
import pathlib
import sys

FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{FILE_DIR_PATH}/../.."
sys.path.append(ROOT_PATH)

from pkg_manager import install_packages, FAKE_ROOT, BUILD_FOLDER  # nopep8


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
    # "python3-setuptools",
    "python3-requests",
    "python3-urllib3",
    "python3-certifi",
    "python3-idna"]

DIRECTORY_LAYOUT = ["bin", "etc", "lib", "lib64", "sbin", "usr", "var", "tools", "builds"]


# create folders in root
def create_directory_layout():
    print("creating minimal directory layout: ...")
    for folder in DIRECTORY_LAYOUT:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    print("creating minimal directory layout: ok")


def install_required_packages_from_host(lfs_dir: str, verbose: bool, jobs: int, measure_time: bool) -> bool:
    os.chdir(lfs_dir)
    create_directory_layout()

    os.environ["LFS"] = lfs_dir
    os.environ["LFS_TGT"] = "x86_64-lfs-linux-gnu"
    os.environ["PATH"] = lfs_dir + "/tools/bin:" + os.environ["PATH"]
    os.environ["TODD_BUILD_DIR"] = BUILD_FOLDER
    os.environ["TODD_FAKE_ROOT_DIR"] = FAKE_ROOT

    return install_packages(REQUIRED_PACKAGES, f"{FILE_DIR_PATH}/packages", "host", lfs_dir, verbose, jobs, measure_time)

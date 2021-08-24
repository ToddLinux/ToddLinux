import os
import pathlib
from typing import List

from pkg_manager import install_packages

file_dir_path = pathlib.Path(__file__).parent.resolve()
LOCK_FILE = "host_installed.lock"

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
    "python3"]


def install_required_packages(lfs_dir: str, verbose: bool, jobs: int, measure_time: bool) -> bool:
    os.environ["LFS"] = lfs_dir
    os.environ["LFS_TGT"] = "x86_64-lfs-linux-gnu"
    os.environ["PATH"] = lfs_dir + "/tools/bin:" + os.environ["PATH"]

    return install_packages(REQUIRED_PACKAGES, f"{file_dir_path}/host_chroot_packages", "host", f"{lfs_dir}/{LOCK_FILE}", verbose, jobs, measure_time)

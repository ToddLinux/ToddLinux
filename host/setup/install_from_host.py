import os
import pathlib
import sys

FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{FILE_DIR_PATH}/../.."
sys.path.append(ROOT_PATH)
from pkg_manager import install_packages  # nopep8


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
    "zlib",
    "python3.7",
    "python3-requests",
    "python3-urllib3",
    "python3-certifi",
    "python3-idna"]


def install_required_packages_from_host(lfs_dir: str, verbose: bool, jobs: int, measure_time: bool) -> bool:
    os.environ["LFS"] = lfs_dir
    os.environ["LFS_TGT"] = "x86_64-lfs-linux-gnu"
    os.environ["PATH"] = lfs_dir + "/tools/bin:" + os.environ["PATH"]

    return install_packages(REQUIRED_PACKAGES, f"{FILE_DIR_PATH}/host_chroot_packages", "host", f"{lfs_dir}/{LOCK_FILE}", verbose, jobs, measure_time)

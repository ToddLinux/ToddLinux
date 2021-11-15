from argparse import ArgumentParser
import os
from typing import Optional

from .host import create_sign_file, enter_chroot, setup_host, assert_signed
from .chroot import install_from_chroot

__all__ = ["main"]


def main() -> bool:
    parser = ArgumentParser(description="ToddLinux Builder.")
    # different sub-scripts
    parser.add_argument("--sign", help="Sign LFS Directory.", action="store_true")
    parser.add_argument("--enter", help="Enter Chroot Environment.", action="store_true")
    parser.add_argument("--chroot", help="Perform installation from within chroot environment. Not to be used by the user. (path has to be '/')", action="store_true")

    # sign lfs
    parser.add_argument("-f", "--force", help="Add sign file even when folder is not empty", action="store_true")
    parser.add_argument("path", help="path to lfs chroot environment", type=str)

    # installation
    parser.add_argument("-v", "--verbose", help="print messages from underlaying build processes", action="store_true")
    parser.add_argument("-j", "--jobs", help="number of concurrent jobs (if not specified 'nproc' output is used)")
    parser.add_argument("-p", "--prefetch", help="download package sources before building", action="store_true")

    args = parser.parse_args()
    # different sub-scripts
    sign: bool = args.sign
    enter: bool = args.enter
    chroot: bool = args.chroot

    # sign lfs
    force: bool = args.force
    lfs_dir: str = os.path.abspath(args.path)

    # installation
    verbose: bool = args.verbose
    prefetch: bool = args.prefetch
    jobs: Optional[int] = args.jobs

    if sign:
        return create_sign_file(lfs_dir, force)
    assert_signed(lfs_dir)
    if enter:
        return enter_chroot(lfs_dir)
    if chroot:
        assert not lfs_dir == "/", "Chroot scripts must be launched from root path."
        return install_from_chroot(verbose, jobs)

    return setup_host(lfs_dir, verbose, prefetch, jobs)

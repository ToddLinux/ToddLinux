import os
import sys

from typing import Optional
from argparse import ArgumentParser
from create_directory_layout import create_directory_layout
from install_from_host import install_required_packages_from_host
from create_directory_layout import create_directory_layout


# TODO: find a better way to pass these arguments
def main() -> bool:
    parser = ArgumentParser(description="Run Todd Linux build system")
    parser.add_argument('path', help='path to chroot environment', type=str)
    parser.add_argument('-t', '--time', help='measure build time', action='store_true')
    parser.add_argument('-v', '--verbose', help='print messages from underlaying build processes', action='store_true')
    parser.add_argument('-j', '--jobs', help='number of concurrent jobs (if not specified `nproc` output is used)')
    args = parser.parse_args()
    verbose: bool = args.verbose
    measure_time: bool = args.time
    jobs: Optional[int] = args.jobs
    lfs_dir = os.path.abspath(args.path)

    os.chdir(lfs_dir)

    create_directory_layout()

    if not install_required_packages_from_host(lfs_dir, verbose, jobs, measure_time):
        return False

    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)

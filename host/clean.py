# See LICENSE for license details.
from argparse import ArgumentParser
from os import geteuid, getuid, system, environ
from sys import exit
from shutil import rmtree
from os.path import isdir
from pwd import getpwuid

BUILDS_DIRECTORY_LAYOUT = ["bin", "etc", "lib", "lib64", "sbin", "usr", "var", "tools", "builds"]


def get_username():
    try:
        return environ["SUDO_USER"]
    except KeyError:
        return getpwuid(getuid())[0]


def clean_chroot(path: str):
    system(f"umount {path}/run {path}/proc {path}/sys")
    system(f"umount -l {path}/dev/pts")
    system(f"umount -l {path}/dev")
    if system(f"mount | grep {path}/dev") != 0:
        if isdir(f"{path}/dev"):
            rmtree(f"{path}/dev")
    else:
        print(f"Run manually command: rm {path}/dev/console {path}/dev/null")

    if isdir(f"{path}/proc"):
        rmtree(f"{path}/proc")
    if isdir(f"{path}/run"):
        rmtree(f"{path}/run")
    if isdir(f"{path}/sys"):
        rmtree(f"{path}/sys")

    user = get_username()
    system(f"chown -R {user} {path}")


def clean_sources(path: str):
    sources_dir = f"{path}/src"
    if isdir(sources_dir):
        rmtree(sources_dir)


def clean_cross(path: str):
    for directory in BUILDS_DIRECTORY_LAYOUT:
        dir_name = f"{path}/{directory}"
        if isdir(dir_name):
            rmtree(dir_name)


def main() -> int:
    parser = ArgumentParser(description='Handy cleanup script, if none of options are specified all are run')
    parser.add_argument('path', help='path to target system', type=str)
    parser.add_argument('-chroot', help='clean chroot', action='store_true')
    parser.add_argument('-sources', help='clean sources', action='store_true')
    parser.add_argument('-cross', help='clean cross toolchain', action='store_true')
    args = parser.parse_args()

    if geteuid() != 0:
        print("Insufficient privliges, run as root")
        return 1

    if args.sources:
        clean_sources(args.path)

    if args.cross:
        clean_cross(args.path)

    if args.chroot:
        clean_chroot(args.path)

    if not any([args.cross, args.chroot, args.sources]):
        clean_sources(args.path)
        clean_cross(args.path)
        clean_chroot(args.path)

    return 0


if __name__ == '__main__':
    exit(main())

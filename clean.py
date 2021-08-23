# See LICENSE for license details.
# todo: fix "using namespace std;" garbage
from argparse import ArgumentParser
from os import geteuid, getuid, system, environ, chdir
from sys import exit
from shutil import rmtree
from os.path import isdir, exists
from pwd import getpwuid

BUILDS_DIRECTORY_LAYOUT = ["bin", "etc", "lib", "lib64", "sbin", "usr", "var", "tools", "builds"]

CHROOT_DIRECTORY_LAYOUT = [
    "/etc/opt",
    "/etc/sysconfig",
    "/lib/firmware",
    "/media",
    "/media/floppy",
    "/media/cdrom",
    "/usr/include/usr/lib",
    "/usr/src",
    "/usr/local/bin",
    "/usr/local/include",
    "/usr/local/lib",
    "/usr/local/sbin",
    "/usr/local/src",
    "/usr/share/color",
    "/usr/share/dict",
    "/usr/local/share/color",
    "/usr/local/share/dict",
    "/usr/local/share/doc",
    "/usr/local/share/info",
    "/usr/local/share/locale",
    "/usr/local/share/man",
    "/usr/share/zoneinfo",
    "/usr/local/share/misc",
    "/usr/local/share/terminfo",
    "/usr/local/share/zoneinfo",
    "/usr/share/man/man2",
    "/usr/share/man/man6",
    "/usr/local/share/man/man1",
    "/usr/local/share/man/man2",
    "/usr/local/share/man/man3",
    "/usr/local/share/man/man4",
    "/usr/local/share/man/man5",
    "/usr/local/share/man/man6",
    "/usr/local/share/man/man7",
    "/usr/local/share/man/man8",
    "/var/cache",
    "/var/local",
    "/var/log",
    "/var/mail",
    "/var/opt",
    "/var/spool",
    "/var/lib/color",
    "/var/lib/misc",
    "/var/lib/locate"
]


def get_username():
    try:
        return environ["SUDO_USER"]
    except KeyError:
        return getpwuid(getuid())[0]


def clean_chroot(path: str):
    for dir_name in CHROOT_DIRECTORY_LAYOUT:
        folder = f"{path}{dir_name}"
        if isdir(folder):
            rmtree(folder)


def clean_chroot_prep(path: str):
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
    parser.add_argument('-chroot_prep', help='clean chroot preparations', action='store_true')
    parser.add_argument('-sources', help='clean sources', action='store_true')
    parser.add_argument('-cross', help='clean cross toolchain', action='store_true')
    parser.add_argument('-chroot', help='clean chroot', action='store_true')
    args = parser.parse_args()
    chdir(args.path)
    if not exists("lfs_sign.loc"):
        print("Error: provided lfs path doesn't have sign file; use sign_lfs.py to create one")
        return 1

    if geteuid() != 0:
        print("Insufficient privliges, run as root")
        return 1

    if args.sources:
        clean_sources(args.path)

    if args.cross:
        clean_cross(args.path)

    if args.chroot_prep:
        clean_chroot_prep(args.path)

    if args.chroot:
        clean_chroot(args.path)

    if not any([args.cross, args.chroot_prep, args.sources, args.chroot]):
        clean_sources(args.path)
        clean_cross(args.path)
        clean_chroot_prep(args.path)
        clean_chroot(args.path)

    return 0


if __name__ == '__main__':
    exit(main())

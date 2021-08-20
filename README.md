# ToddLinux

[![Build](https://github.com/adamjedrzejewski/ToddLinux/actions/workflows/build.yml/badge.svg)](https://github.com/adamjedrzejewski/ToddLinux/actions/workflows/build.yml)
[![License](https://img.shields.io/badge/license-MIT-yellow)](https://github.com/adamjedrzejewski/ToddLinux/blob/main/LICENSE)

[Linux From Scratch Book](https://www.linuxfromscratch.org/lfs/downloads/stable/LFS-BOOK-10.1.pdf)

## Install Prerequisites

```bash
sudo apt install -y bash binutils bison bzip2 coreutils diffutils findutils gawk gcc g++ grep gzip m4 make patch perl python3 sed tar texinfo xz-utils
```

## Create LFS Partition

```bash
fdisk /dev/XXX              # create partition
mkfs.ext4 /dev/XXX          # create filesystem
mkdir /path/to/dir          # create mount directory
mount /dev/XXX /path/to/dir # mount
```

## Terminology

- package: program e.g. GCC
- package source: source for package; one package might require multiple package sources
- environments:
    - host environment: initial machine used for the first builds (usually a virtual machine running on it's own "host"-the real hardware)
    - chroot environment: environment installed on the host used to combat shared object hell and build target
    - target environment: machine running the final build os

## How to Build?

- clone repository
- install prerequisites
- execute `host/check_req/check_requirements.py`, install any missing packages and create required sym links
- execute `host/fetch_sources/fetch_sources.py`
- execute `host/cross_tool_chain/build.py`
- execute `chroot_env/prepare_chroot.py`
- execute `chroot_env/tmp_tools/run_tool_scripts.py`
- ...

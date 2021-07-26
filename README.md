# ToddLinux

[Linux From Scratch Book](https://www.linuxfromscratch.org/lfs/downloads/stable/LFS-BOOK-10.1.pdf)

### Install prerequisites
```bash
sudo apt install -y bash binutils bison bzip2 coreutils diffutils findutils gawk gcc g++ grep gzip m4 make patch perl python3 sed tar texinfo xz-utils
```

### Create LFS partition
```bash
fdisk /dev/XXX              # create partition
mkfs.ext4 /dev/XXX          # create filesystem
mkdir /path/to/dir          # create mount directory
mount /dev/XXX /path/to/dir # mount
```
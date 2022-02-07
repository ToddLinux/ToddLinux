# Todd Linux Toolchain
The toolchain required to build ToddLinux ISO and ToddLinux operating system should be hosted separetely. In order to speed up build process the toolchain should be easily accessible, prefferably in a form of an archive hosted by ToddLinux developers.

## Toolchain components
No package management should be performed at toolchain level. \
The single archive should contain:
- [GNU Binutils](https://www.gnu.org/software/binutils/)
- [GNU C compiler](https://gcc.gnu.org/)
- [GNU C library](https://www.gnu.org/software/libc/)
- [GNU M4](https://www.gnu.org/software/m4/)
- [GNU ncurses](https://www.gnu.org/software/ncurses/)
- [GNU coreutils](https://www.gnu.org/software/coreutils/)
- [GNU diffutils](https://www.gnu.org/software/diffutils/)
- [GNU findutils](https://www.gnu.org/software/findutils/)
- [GNU gawk](https://www.gnu.org/software/gawk/)
- [GNU grep](https://www.gnu.org/software/grep/)
- [GNU make](https://www.gnu.org/software/make/)
- [GNU patch](https://www.gnu.org/software/patch)
- [GNU sed](https://www.gnu.org/software/sed/)
- [GNU tar](https://www.gnu.org/software/tar/)
- [GNU gzip](https://www.gnu.org/software/gzip)
- [xz](https://tukaani.org/xz/)
- [file](ftp://ftp.astron.com/pub/file/)
- [python 3](https://www.python.org/)
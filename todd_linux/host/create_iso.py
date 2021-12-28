import os
import shutil

from .sign_lfs import assert_signed

ISO_PATH = "/tmp/todd_linux.iso"


def create_iso(lfs_dir: str) -> bool:
    assert_signed(lfs_dir)

    # uno bruh momento
    shutil.copytree(f"{lfs_dir}/boot", f"{lfs_dir}/isolinux")

    print("Creating bootable ISO: ...")
    if os.system(f"umount -l -R -v {lfs_dir}/proc {lfs_dir}/dev {lfs_dir}/run {lfs_dir}/sys"):
        return False
    if os.system(f"mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -V TODD_LIVE {lfs_dir} > {ISO_PATH}"):
        return False
    print("Creating bootable ISO: ok")

    return True

    # print("Creating bootable ISO: ...")
    # if os.system(f"umount -l -R -v {lfs_dir}/proc {lfs_dir}/dev {lfs_dir}/run {lfs_dir}/sys"):
    #     return False
    # if os.system(f"grub-mkrescue -o {ISO_PATH} {lfs_dir}"):
    #     return False
    # print(f"ISO can be found at {ISO_PATH}")
    # print("Creating bootable ISO: ok")
    # return True

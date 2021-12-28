import os
import shutil

from datetime import datetime

from .sign_lfs import assert_signed


def create_iso(lfs_dir: str) -> bool:
    assert_signed(lfs_dir)

    iso_timestamp = datetime.now().strftime("%Y%m%d%H%M")
    iso_path = f"/tmp/todd_linux_{iso_timestamp}.iso"

    # uno bruh momento
    shutil.copytree(f"{lfs_dir}/boot", f"{lfs_dir}/isolinux", dirs_exist_ok=True)

    print("Creating bootable ISO: ...")
    if os.system(f"umount -l -R -v {lfs_dir}/proc {lfs_dir}/dev {lfs_dir}/run {lfs_dir}/sys"):
        return False
    if os.system(f"mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -V TODD_LIVE {lfs_dir} > {iso_path}"):
        return False
    print("Creating bootable ISO: ok")

    return True


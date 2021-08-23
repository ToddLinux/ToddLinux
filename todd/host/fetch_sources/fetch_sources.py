# See LICENSE for license details.
import sys
import os
import requests
import urllib
import pathlib
import csv

file_dir_path = pathlib.Path(__file__).parent.resolve()


class Source:
    def __init__(self, dir_name, link):
        self.dir_name = dir_name
        self.link = link

    def __repr__(self):
        return f"<Source '{self.dir_name}' '{self.link}'"


def dwn_file_in_new_folder(url: str) -> bool:
    local_filename = url.split('/')[-1]
    print(f"downloading {local_filename}:\t...\r", end="")
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            print(f"downloading {local_filename}:\tfailure")
            return False
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"downloading {local_filename}:\tok ")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        raise ValueError("Add path to LFS mount point as first argument")
    lfs_dir = os.path.abspath(sys.argv[1])
    os.chdir(lfs_dir)
    if not os.path.exists("lfs_sign.loc"):
        print("Error: provided lfs path doesn't have sign file; use sign_lfs.py to create one")
        return 1

    with open(f"{file_dir_path}/wget_list.csv", "r", newline="") as file:
        raw_sources = csv.DictReader(file, delimiter=";")
        sources = [Source(source["dir_name"], source["link"])
                   for source in raw_sources]

    os.mkdir("src")
    os.chdir("src")
    all_ok = True
    for source in sources:
        os.mkdir(source.dir_name)
        os.chdir(source.dir_name)
        if not dwn_file_in_new_folder(source.link):
            all_ok = False
        os.chdir("..")
    return 0 if all_ok else -1


if __name__ == "__main__":
    sys.exit(main())

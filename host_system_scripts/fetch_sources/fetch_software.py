# See LICENSE for license details.
import sys
import os
import requests
import urllib
import pathlib

file_dir_path = pathlib.Path(__file__).parent.resolve()


def dwn_file_in_new_folder(url: str):
    local_filename = url.split('/')[-1]
    print(f"downloading {local_filename}:\t...\r", end="")
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            print(f"downloading {local_filename}:\tit just doesn't work")
            return local_filename
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"downloading {local_filename}:\tok ")
    return local_filename


def main():
    if len(sys.argv) < 2:
        raise ValueError("Add path to LFS mount point as first argument")
    lfs_dir = sys.argv[1]

    with open(f"{file_dir_path}/wget-list", "r") as file:
        sources = [url.strip() for url in file.readlines()]

    os.chdir(lfs_dir)
    os.mkdir("src")
    os.chdir("src")
    for source in sources:
        filename = source.split('/')[-1]
        os.mkdir(filename)
        os.chdir(filename)
        dwn_file_in_new_folder(source)
        os.chdir("..")


if __name__ == "__main__":
    main()

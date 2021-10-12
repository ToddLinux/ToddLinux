# See LICENSE for license details.
import pathlib
from typing import Dict, Optional, List
from dataclasses import dataclass

import json
import os

FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
INDEX_FILE_PATH = "/var/lib/todd/status.json"
INDEX_FILE_DIR_PATH = "/var/lib/todd"


class PackageIndex:
    def __init__(self, name: str, version: str, files: List[str]):
        self.name = name
        self.version = version
        self.files = files


def append_index(lfs_dir: str, new_pkg: PackageIndex) -> None:
    index = read_index(lfs_dir)
    if new_pkg.name in index:
        raise ValueError(f"Can't append already installed package {new_pkg}")
    index[new_pkg.name] = new_pkg
    update_index(lfs_dir, index)


def remove_index(lfs_dir: str, del_pkg: PackageIndex) -> None:
    index = read_index(lfs_dir)
    if del_pkg.name not in index:
        raise ValueError(f"Can't remove index of not installed package {del_pkg}")
    del index[del_pkg.name]
    update_index(lfs_dir, index)


def read_index(lfs_dir: str) -> Dict[str, PackageIndex]:
    index: Dict[str, PackageIndex] = {}
    # index to be created?
    if not os.path.isfile(f"{lfs_dir}{INDEX_FILE_PATH}"):
        os.makedirs(f"{lfs_dir}{INDEX_FILE_DIR_PATH}", exist_ok=True)
        update_index(lfs_dir, index)
        return index

    with open(f"{lfs_dir}{INDEX_FILE_PATH}", "r") as file:
        pkgs_json = json.load(file)
        for pkg_json in pkgs_json.values():
            index[pkg_json["name"]] = PackageIndex(pkg_json["name"], pkg_json["version"], pkg_json["files"])
    return index


def update_index(lfs_dir: str, index: Dict[str, PackageIndex]) -> None:
    with open(f"{lfs_dir}{INDEX_FILE_PATH}", "w") as file:
        json.dump({pkg.name: pkg.__dict__ for pkg in index.values()}, file)

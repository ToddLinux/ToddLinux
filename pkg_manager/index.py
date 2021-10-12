# See LICENSE for license details.
import pathlib
from typing import Dict, Optional, List
from dataclasses import dataclass

import json

FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
BUILD_FOLDER = "/tmp/todd_linux_build"
Stub_TARGET_FOLDER = "/tmp/todd_linux_build"


@dataclass
class PackageIndex:
    name: str
    version: str
    files: List[str]


def append_index(lfs_dir: str, new_pkg: PackageIndex) -> None:
    pkgs = read_index(lfs_dir)
    if new_pkg.name in pkgs:
        raise ValueError(f"Can't append already installed package {new_pkg}")


def remove_index(lfs_dir: str, del_pkg: PackageIndex) -> None:
    pkgs = read_index(lfs_dir)
    if del_pkg.name not in pkgs:
        raise ValueError(f"Can't remove index of not installed package {del_pkg}")


def read_index(lfs_dir: str) -> Dict[str, PackageIndex]:
    index: Dict[str, PackageIndex] = {}
    with open(f"{lfs_dir}/var/lib/todd/status.json", "r") as file:
        pkgs_json = json.load(file)
        for pkg_json in pkgs_json:
            index[pkg_json["name"]] = PackageIndex(pkg_json["name"], pkg_json["version"], pkg_json["files"])
    return index


def update_index(lfs_dir: str, index: Dict[str, PackageIndex]) -> None:
    with open(f"{lfs_dir}/var/lib/todd/status.json", "w") as file:
        json.dump(index, file)

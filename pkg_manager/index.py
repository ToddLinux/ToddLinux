# See LICENSE for license details.
import pathlib
from typing import Optional, List

from .install import Package

FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
BUILD_FOLDER = "/tmp/todd_linux_build"
Stub_TARGET_FOLDER = "/tmp/todd_linux_build"


def append_index(package: Package) -> None:
    return None


def fetch_index(pkg_name: str) -> Optional[Package]:
    return None


def read_index() -> List[Package]:
    return []

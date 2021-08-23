# See LICENSE for license details.
import sys
import os
import shutil
import csv
import pathlib
import subprocess
import time
from typing import Optional, List, Dict

from datetime import timedelta
import requests
from time import time
from argparse import ArgumentParser


FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
BUILD_FOLDER = "/tmp/todd_linux_build"


# represents build and installation of <package>
class Package:
    def __init__(self, name: str, src_urls: List[str], repo: str, build_script: str = None):
        self.name = name
        self.src_urls = src_urls
        self.build_script = f"{repo}/{name}.sh" if build_script is None else f"{repo}/{build_script}"

    def __repr__(self):
        return f"<Package: '{self.name}' src_urls: {', '.join(self.src_urls)} build_script: '{self.build_script}'>"


def dwn_file(url: str) -> bool:
    local_filename = url.split('/')[-1]
    print(f"downloading {local_filename}: ...", end="")
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            print(f"downloading {local_filename}: failure", file=sys.stderr)
            return False
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"downloading {local_filename}: ok")
    return True


def install_package(package: Package, verbose=False) -> bool:
    print(f"preparing {package.name}: ...")
    # delete and create build folder
    if os.path.isdir(BUILD_FOLDER):
        shutil.rmtree(BUILD_FOLDER)
    os.mkdir(BUILD_FOLDER)
    os.chdir("/tmp/todd_linux_build")
    print(f"preparing {package.name}: ok")

    print(f"downloading sources for {package.name}: ...")
    for src in package.src_urls:
        if not dwn_file(src):
            return False

    print(f"running build script for {package.name}: ...")
    cmd_suffix = "" if verbose else " >/dev/null 2>&1"
    if os.system(f"{package.build_script}{cmd_suffix}") != 0:
        print(f"build script for {package.name}: failure", file=sys.stderr)
        return False

    print(f"running build script for {package.name}: ok")
    return True

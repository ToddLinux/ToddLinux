# See LICENSE for license details.
import csv
import pathlib
import sys
import json

from typing import List


FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{FILE_DIR_PATH}/../.."
sys.path.append(ROOT_PATH)
from pkg_manager import Requirement, check_req, SymRequirement, check_sym  # nopep8


# requirement factory (because defaults)
def get_requirement_factory(defaults):
    default_version_regex_pattern = defaults["version_regex_pattern"]
    default_later_version_ok = defaults["later_version_ok"]
    default_read_stderr_instead_of_stdout = defaults["read_stderr_instead_of_stdout"]

    def inner(object):
        name = object["name"]
        min_version = object["min_version"]
        command = object["command"]
        version_regex_pattern = object.get("version_regex_pattern", default_version_regex_pattern)
        later_version_ok = object.get("later_version_ok", default_later_version_ok)
        read_stderr_instead_of_stdout = object.get("read_stderr_instead_of_stdout", default_read_stderr_instead_of_stdout)

        return Requirement(name, min_version, command, version_regex_pattern, later_version_ok, read_stderr_instead_of_stdout)

    return inner


# load requirements file
def read_reqs() -> List[Requirement]:
    with open(f"{FILE_DIR_PATH}/host_reqs/reqs.json") as f:
        data = json.load(f)
        defaults = data["defaults"]
        req_factory = get_requirement_factory(defaults)
        reqs = [
            req_factory(req)
            for req in data["requirements"]
        ]

        return reqs


# return True if all packages are satisfied
def check_reqs() -> bool:
    requirements = read_reqs()
    return all(
        check_req(req)
        for req
        in requirements
    )


# return True if all sym links correct
def check_sym_links() -> bool:
    # load csv
    with open(f"{FILE_DIR_PATH}/host_reqs/req_sym_links.csv", "r", newline="") as file:
        raw_sym_requirements = csv.DictReader(file, delimiter=";")
        sym_requirements = [SymRequirement(req["cmd_name"],
                                           req["sym_link"]) for req in raw_sym_requirements]
    all_ok = True
    for req in sym_requirements:
        if not check_sym(req):
            all_ok = False
    return all_ok


def check_all_reqs() -> bool:
    print("checking requirements: ...")
    all_ok = True
    if not check_reqs():
        all_ok = False
    if not check_sym_links():
        all_ok = False
    if not all_ok:
        print("checking requirements: failure")
        return False
    print("checking requirements: ok")
    return True

# See LICENSE for license details.
import csv
import pathlib
import sys

FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{FILE_DIR_PATH}/../.."
sys.path.append(ROOT_PATH)
from pkg_manager import Requirement, check_req, SymRequirement, check_sym  # nopep8


# return True if all packages are satisfied
def check_reqs() -> bool:
    # load csv
    with open(f"{FILE_DIR_PATH}/host_reqs/reqs.csv", "r", newline="") as file:
        raw_requirements = csv.DictReader(file, delimiter=";")
        requirements = [Requirement(req["name"],
                                    req["min_version"],
                                    req["command"],
                                    req["version_regex_pattern"],
                                    req["later_version_ok"] == "true") for req in raw_requirements]
    all_ok = True
    for req in requirements:
        if not check_req(req):
            all_ok = False
    return all_ok


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

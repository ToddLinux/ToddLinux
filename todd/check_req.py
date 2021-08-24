# See LICENSE for license details.
import csv
import pathlib

from pkg_manager import Requirement, check_req, SymRequirement, check_sym

file_dir_path = pathlib.Path(__file__).parent.resolve()


# return True if all packages are satisfied
def check_reqs() -> bool:
    # load csv
    with open(f"{file_dir_path}/host_reqs/reqs.csv", "r", newline="") as file:
        raw_requirements = csv.DictReader(file, delimiter=";")
        requirements = [Requirement(req["name"],
                                    req["min_version"],
                                    req["command"],
                                    req["version_regex_pattern"]) for req in raw_requirements]
    all_ok = True
    for req in requirements:
        if not check_req(req):
            all_ok = False
    return all_ok


# return True if all sym links correct
def check_sym_links() -> bool:
    # load csv
    with open(f"{file_dir_path}/host_reqs/req_sym_links.csv", "r", newline="") as file:
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

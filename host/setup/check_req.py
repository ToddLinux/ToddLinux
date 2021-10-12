# See LICENSE for license details.
import csv
import pathlib
import sys
import json

from typing import Callable, List, Any
from pkg_manager import Requirement, check_req, SymRequirement, check_sym  # nopep8


FILE_DIR_PATH = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{FILE_DIR_PATH}/../.."
REQUIREMENTS_FILE = f"{FILE_DIR_PATH}/host_reqs/reqs.json"

sys.path.append(ROOT_PATH)


# TODO: failure scenario for missing values
# requirement factory (because defaults)
def get_requirement_factory(defaults: 'dict[str, Any]') -> Callable[['dict[str, Any]'], Requirement]:
    """
    Creates a factory function that produces Requirement objects based on the provided defaults.

    :param defaults: dictionary containing default values for field creation
    :return: a function that takes a dictionary with values for fields and creates a Requirement object based on these values and provided defaults
    """
    default_version_regex_pattern = defaults.get("version_regex_pattern", "((\\d+)(\\.(\\d+))+)")
    default_later_version_ok = defaults.get("later_version_ok", True)
    default_read_stderr_instead_of_stdout = defaults.get("read_stderr_instead_of_stdout", False)

    def inner(object: 'dict[str, Any]') -> Requirement:
        name = object["name"]
        min_version = object["min_version"]
        command = object["command"]
        version_regex_pattern = object.get("version_regex_pattern", default_version_regex_pattern)
        later_version_ok = object.get("later_version_ok", default_later_version_ok)
        read_stderr_instead_of_stdout = object.get("read_stderr_instead_of_stdout", default_read_stderr_instead_of_stdout)
        return Requirement(
            name,
            min_version,
            command,
            version_regex_pattern,
            later_version_ok,
            read_stderr_instead_of_stdout
        )

    return inner


# load requirements file
def read_reqs() -> List[Requirement]:
    """
    Load the requirements from requirements file.

    :return: a list of requirements
    """
    with open(REQUIREMENTS_FILE) as f:
        data = json.load(f)
        defaults = data["defaults"]
        req_factory = get_requirement_factory(defaults)
        return [
            req_factory(req)
            for req
            in data["requirements"]
        ]


# return True if all packages are satisfied
def check_reqs() -> bool:
    """
    Check if all requirements are satisfied.

    :return: true if all satisfied false otherwise
    """
    requirements = read_reqs()
    return all(
        check_req(req)
        for req
        in requirements
    )


# TODO: check recursive symlinks
# TODO: use json instead?
# return True if all sym links are correct
def check_sym_links() -> bool:
    """
    Check if all symlinks are correct.

    :return: true if all satisfied false otherwise
    """
    # load csv
    with open(f"{FILE_DIR_PATH}/host_reqs/req_sym_links.csv", "r", newline="") as file:
        raw_sym_requirements = csv.DictReader(file, delimiter=";")
        sym_requirements = [SymRequirement(req["cmd_name"],
                                           req["sym_link"]) for req in raw_sym_requirements]

    return all(
        check_sym(req)
        for req
        in sym_requirements
    )


def check_all_reqs() -> bool:
    """
    Check requirements for installed software and symlinks

    :return: true if all satisfied false otherwise
    """
    print("checking requirements: ...")
    all_ok = all([
        check_reqs(),
        check_sym_links()
    ])

    if all_ok:
        print("checking requirements: ok")
    else:
        print("checking requirements: failure")

    return all_ok

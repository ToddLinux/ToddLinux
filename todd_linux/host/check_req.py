# See LICENSE for license details.
import csv
import json
import pathlib
import re
import subprocess
from typing import Any, Callable, Dict, List

__all__ = ["check_all_reqs"]


BASE_DIR = pathlib.Path(__file__).parent.resolve()
ROOT_PATH = f"{BASE_DIR}/../.."

REQ_FILE = f"{ROOT_PATH}/todd_linux/host_reqs/reqs.json"
REQ_SYM_LINKS_FILE = f"{ROOT_PATH}/todd_linux/host_reqs/req_sym_links.csv"


class Requirement:
    """This program has to be installed with a specific version"""

    def __init__(
        self,
        name: str,
        min_version: str,
        command: List[str],
        version_regex_pattern: str,
        later_version_ok: bool,
        read_stderr_instead_of_stdout: bool,
    ):
        self.name = name
        self.min_version = min_version
        # quotes in command not supported
        self.command = command
        self.version_regex_pattern = version_regex_pattern
        self.later_version_ok = later_version_ok
        self.read_stderr_instead_of_stdout = read_stderr_instead_of_stdout

    def __repr__(self):
        return f"<Requirement name: '{self.name}' min_version: '{self.min_version}' command: '{self.command}' version_regex_pattern: '{self.version_regex_pattern}' later_version_ok: {self.later_version_ok}\tread_stderr_instead_of_stdout: {self.read_stderr_instead_of_stdout}>"


def get_installed_version(req: Requirement, output: str) -> str:
    """get installed version from command output"""
    pattern = re.compile(req.version_regex_pattern)
    match = pattern.findall(output.replace("\n", ""))
    if match:
        return match[0][0]
    raise ValueError(f"regex broken for {req}")


def satisfied(req: Requirement, installed_version) -> bool:
    """check if min version is satisfied with output of version check command"""
    try:
        min_parts = req.min_version.split(".")
        ins_parts = installed_version.split(".")

        # ignore any part that only exists in one
        for part in zip(min_parts, ins_parts):
            # sometimes version contain letters in the end, like '3.4.1a'
            if part[0][-1].isdigit():
                min_part = part[0]
                min_last_letter = ""
            else:
                min_part = part[0][:-1]
                min_last_letter = part[0][-1]

            if part[1][-1].isdigit():
                ins_part = part[1]
                ins_last_letter = ""
            else:
                ins_part = part[1][:-1]
                ins_last_letter = part[1][-1]

            if req.later_version_ok:
                # check number part
                if int(min_part) > int(ins_part):
                    return False
                if int(min_part) < int(ins_part):
                    return True

                # check letter part
                if min_last_letter > ins_last_letter:
                    return False
                if min_last_letter < ins_last_letter:
                    return True
            else:
                # everything has to be exact
                if int(min_part) != int(ins_part) or min_last_letter != ins_last_letter:
                    return False

        # everything is the same
        return True
    except ValueError:
        raise ValueError(f"Version broken for {req}")


def collect_stdout(command: List[str]):
    """run command and collect stdout only"""
    return subprocess.run(
        command,
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout.decode()


def collect_stderr(command: List[str]):
    """run command and collect stderr only"""
    # dedicated to bzip2
    return subprocess.run(
        command,
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    ).stderr.decode()


def collect_output(req: Requirement):
    """run requirement command and collect output"""
    if req.read_stderr_instead_of_stdout:
        return collect_stderr(req.command)
    else:
        return collect_stdout(req.command)


def check_req(req: Requirement) -> bool:
    """return False if not satisfied"""
    print(f"checking {req.name}: ...")
    try:
        output = collect_output(req)
        installed_version = get_installed_version(req, output)

        if not satisfied(req, installed_version):
            print(
                f"checking {req.name}: required version is '{req.min_version}' but only version '{installed_version}' is installed!"
            )
            return False
        else:
            # space in end is required to overwrite previous loading dots
            print(f"checking {req.name}: ok")
            return True
    except FileNotFoundError:
        print(f"checking {req.name}: package not installed!")
        return False


class SymRequirement:
    def __init__(self, cmd_name: str, sym_link: str):
        self.cmd_name = cmd_name
        self.sym_link = sym_link


def check_sym(req: SymRequirement) -> bool:
    """return False if not satisfied"""
    print(f"checking sym for {req.cmd_name}: ...")
    if str(pathlib.Path(req.sym_link).resolve()).endswith(req.cmd_name):
        print(f"checking sym for {req.cmd_name}: ok")
        return True
    else:
        print(f"checking sym for {req.cmd_name}: incorrect sym link at {req.sym_link}")
        return False


# TODO: failure scenario for missing values
def get_requirement_factory(defaults: Dict[str, Any]) -> Callable[[Dict[str, Any]], Requirement]:
    """
    Creates a factory function that produces Requirement objects based on the provided defaults.

    requirement factory because defaults

    :param defaults: dictionary containing default values for field creation
    :return: a function that takes a dictionary with values for fields and creates a Requirement object based on these values and provided defaults
    """
    default_version_regex_pattern = defaults.get("version_regex_pattern", "((\\d+)(\\.(\\d+))+)")
    default_later_version_ok = defaults.get("later_version_ok", True)
    default_read_stderr_instead_of_stdout = defaults.get("read_stderr_instead_of_stdout", False)

    def inner(object: Dict[str, Any]) -> Requirement:
        return Requirement(
            object["name"],
            object["min_version"],
            object["command"],
            object.get("version_regex_pattern", default_version_regex_pattern),
            object.get("later_version_ok", default_later_version_ok),
            object.get("read_stderr_instead_of_stdout", default_read_stderr_instead_of_stdout),
        )

    return inner


def read_reqs() -> List[Requirement]:
    """
    Load the requirements from requirements file.

    :return: a list of requirements
    """
    with open(REQ_FILE) as f:
        data = json.load(f)
        defaults = data["defaults"]
        req_factory = get_requirement_factory(defaults)
        return [req_factory(req) for req in data["requirements"]]


def check_reqs() -> bool:
    """
    Check if all requirements are satisfied.

    :return: True if all satisfied False otherwise
    """
    requirements = read_reqs()
    return all(check_req(req) for req in requirements)


# TODO: check recursive symlinks
# TODO: use json instead?
def check_sym_links() -> bool:
    """
    Check if all symlinks are correct.

    :return: True if all satisfied False otherwise
    """
    # load csv
    with open(REQ_SYM_LINKS_FILE, "r", newline="") as file:
        raw_sym_requirements = csv.DictReader(file, delimiter=";")
        sym_requirements = [SymRequirement(req["cmd_name"], req["sym_link"]) for req in raw_sym_requirements]

    return all(check_sym(req) for req in sym_requirements)


def check_all_reqs() -> bool:
    """
    Check requirements for installed software and symlinks

    :return: True if all satisfied False otherwise
    """
    print("checking requirements: ...")
    all_ok = all([check_reqs(), check_sym_links()])

    if all_ok:
        print("checking requirements: ok")
    else:
        print("checking requirements: failure")

    return all_ok

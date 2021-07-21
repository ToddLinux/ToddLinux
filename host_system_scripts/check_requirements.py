import csv
import subprocess
import re
import sys
from typing import Tuple


class Requirement:
    def __init__(self, name: str, min_version: str, command: str, version_regex_pattern: str):
        self.name = name
        self.min_version = min_version
        # quotes in command not supported
        self.command = command.split(" ")
        self.version_regex_pattern = version_regex_pattern

    def __repr__(self):
        return f"<Requirement name: '{self.name}'\tmin_version: '{self.min_version}'\tcommand: '{self.command}'\tversion_regex_pattern: '{self.version_regex_pattern}'>"


# check if min version is satisfied with output of version check command
def satisfied(req: Requirement, installed_version) -> bool:
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
        # everything is the same
        return True
    except ValueError:
        raise ValueError(f"Version broken for {req}")


# get installed version from command output
def get_installed_version(req: Requirement, output: str) -> str:
    pattern = re.compile(req.version_regex_pattern)
    match = pattern.findall(output.replace("\n", ""))
    if match:
        return match[0]
    raise ValueError(f"regex broken for {req}")


# return False if not satisfied
def check_pkg(req: Requirement) -> bool:
    print(f"checking {req.name}: ...\r", end="")
    try:
        output = subprocess.check_output(
            req.command, stderr=subprocess.STDOUT).decode()

        installed_version = get_installed_version(req, output)

        if not satisfied(req, installed_version):
            print(
                f"checking {req.name}: required version is '{req.min_version}' but only version '{installed_version}' is installed!")
            return False
        else:
            print(f"checking {req.name}: ok")
            return True
    except FileNotFoundError:
        print(f"checking {req.name}: package not installed!")
        return False


def main() -> int:
    # load csv
    with open("requirements.csv", "r", newline="") as file:
        raw_requirements = csv.DictReader(file, delimiter=";")
        requirements = [Requirement(req["name"],
                                    req["min_version"],
                                    req["command"],
                                    req["version_regex_pattern"]) for req in raw_requirements]
    all_ok = True
    for req in requirements:
        if not check_pkg(req):
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())

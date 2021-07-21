import csv
import subprocess
import re
from typing import Tuple


class Requirement:
    def __init__(self, name: str, min_version: str, command: str, version_regex_pattern: str):
        self.name = name
        self.min_version = min_version
        self.command = command
        self.version_regex_pattern = version_regex_pattern

    def __repr__(self):
        return f"<Requirement name: '{self.name}'\tmin_version: '{self.min_version}'\tcommand: '{self.command}'\tversion_regex_pattern: '{self.version_regex_pattern}'>"


# check if min version is satisfied with output of version check command
def check_version(min_version: str, output: str) -> Tuple[bool, str]:
    return False, ""


def check_pkg(req: Requirement) -> None:
    try:
        # quotes in command not supported
        output = subprocess.check_output(req.command.split(" ")).decode()
        satisfied, installed_version = check_version(req.min_version, output)
        if not satisfied:
            print(
                f"'{req.name}' requires version '{req.min_version}' but only version '{installed_version}' is installed!")

    except FileNotFoundError:
        print(f"'{req.name}' is not installed!")


def main():
    # load csv
    with open("requirements.csv", "r", newline="") as file:
        raw_requirements = csv.DictReader(file, delimiter=";")
        requirements = [Requirement(req["name"],
                                    req["min_version"],
                                    req["command"],
                                    req["version_regex_pattern"]) for req in raw_requirements]
    for req in requirements:
        check_pkg(req)
        exit(0)


if __name__ == "__main__":
    main()

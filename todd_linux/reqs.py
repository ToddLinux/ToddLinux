import re
import subprocess

from typing import List

__all__ = ["Requirement", "check_req"]


class Requirement:
    """This program has to be installed with a specific version"""

    def __init__(
        self,
        name: str,
        min_version: str,
        command: List[str],
        version_regex_pattern: str,
        later_version_ok: bool,
        read_stderr_instead_of_stdout: bool
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
    return subprocess.run(command,
                          check=True,
                          stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL).stdout.decode()


def collect_stderr(command: List[str]):
    """run command and collect stderr only"""
    # dedicated to bzip2
    return subprocess.run(command,
                          check=True,
                          stdin=subprocess.DEVNULL,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.PIPE).stderr.decode()


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
            print(f"checking {req.name}: required version is '{req.min_version}' but only version '{installed_version}' is installed!")
            return False
        else:
            # space in end is required to overwrite previous loading dots
            print(f"checking {req.name}: ok")
            return True
    except FileNotFoundError:
        print(f"checking {req.name}: package not installed!")
        return False

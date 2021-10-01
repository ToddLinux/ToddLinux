import re
import subprocess

from typing import List

# TODO: change this to dataclass
class Requirement:
    def __init__(self, name: str, min_version: str, command: List[str], version_regex_pattern: str, later_version_ok: bool, read_stderr_instead_of_stdout: bool):
        self.name = name
        self.min_version = min_version
        # quotes in command not supported
        self.command = command
        self.version_regex_pattern = version_regex_pattern
        self.later_version_ok = later_version_ok
        self.read_stderr_instead_of_stdout = read_stderr_instead_of_stdout

    def __repr__(self):
        return f"<Requirement name: '{self.name}'\tmin_version: '{self.min_version}'\tcommand: '{self.command}'\tversion_regex_pattern: '{self.version_regex_pattern}' later_version_ok: {self.later_version_ok}\tread_stderr_instead_of_stdout: {self.read_stderr_instead_of_stdout}>"


# get installed version from command output
def get_installed_version(req: Requirement, output: str) -> str:
    pattern = re.compile(req.version_regex_pattern)
    match = pattern.findall(output.replace("\n", ""))
    if match:
        return match[0][0]
    raise ValueError(f"regex broken for {req}")


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


# run command and collect stdout only
def collect_stdout(command):
    return subprocess.run(command,
                          check=True,
                          stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL).stdout.decode()


# run command and collect stderr only
def collect_stderr(command):
    # dedicated to bzip2
    return subprocess.run(command,
                          check=True,
                          stdin=subprocess.DEVNULL,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.PIPE).stderr.decode()


# run requirement command and collect output
def collect_output(requirement):
    if requirement.read_stderr_instead_of_stdout:
        return collect_stderr(requirement.command)
    else:
        return collect_stdout(requirement.command)


# return False if not satisfied
def check_req(req: Requirement) -> bool:
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

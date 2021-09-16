import pathlib

from dataclasses import dataclass


@dataclass
class SymRequirement:
    cmd_name: str
    sym_link: str


# return False if not satisfied
def check_sym(req: SymRequirement) -> bool:
    print(f"checking sym for {req.cmd_name}: ...")
    if str(pathlib.Path(req.sym_link).resolve()).endswith(req.cmd_name):
        # space in end is required to overwrite previous loading dots
        print(f"checking sym for {req.cmd_name}: ok")
        return True
    else:
        print(f"checking sym for {req.cmd_name}: incorrect sym link at {req.sym_link}")
        return False

import pathlib


__all__ = ["SymRequirement", "check_sym"]


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

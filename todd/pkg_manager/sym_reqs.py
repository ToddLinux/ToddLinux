import pathlib


class SymRequirement:
    def __init__(self, cmd_name, sym_link):
        self.cmd_name = cmd_name
        self.sym_link = sym_link

    def __repr__(self):
        return f"<SymRequirement cmd_name: '{self.cmd_name}'\t'{self.sym_link}'>"


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

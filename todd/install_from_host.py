import os
from typing import List

LOCK_FILE = "host_installed.lock"


# read already completed builds
def get_finished_builds() -> List[str]:
    finished_builds = []
    if os.path.isfile(LOCK_FILE):
        with open(LOCK_FILE, "r", newline="") as file:
            finished_builds = [line.strip() for line in file.readlines()]
    return finished_builds

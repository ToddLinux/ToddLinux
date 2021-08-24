import sys

import package_manager
import check_req


def main() -> int:
    all_ok = True
    if not check_req.check_requirements():
        all_ok = False
    if not check_req.check_sym_links():
        all_ok = False

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
import sys

from check_req import check_reqs, check_sym_links


def main() -> int:
    print("checking requirements: ...")
    all_ok = True
    if not check_reqs():
        all_ok = False
    if not check_sym_links():
        all_ok = False
    if not all_ok:
        print("checking requirements: failure")
        return 1
    print("checking requirements: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())

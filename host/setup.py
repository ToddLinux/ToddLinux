#!/usr/bin/env python3
import sys

from setup import setup


if __name__ == "__main__":
    sys.exit(0 if setup() else 1)

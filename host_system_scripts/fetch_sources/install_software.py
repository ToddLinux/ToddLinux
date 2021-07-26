import sys
import os


def main():
    if len(sys.argv) < 2:
        raise ValueError("Add path to LFS mount point as first argument")
    lfs_dir = sys.argv[1]
    os.chdir(lfs_dir)
    os.mkdir("src")
    print(os.getcwd())
    print(os.getcwd())
    print(os.listdir(os.getcwd()))


if __name__ == "__main__":
    main()

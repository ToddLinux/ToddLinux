import requests
import sys
import os
import shutil

PKG_CACHE_DIRECTORY = "/var/cache/todd"

# from .install import Package # wtf

def dwn_file(url: str, file_path: str, source_pretty_name: str) -> bool:
    """
    Download file

    :param url: source URI
    :param file_path: file to which the downloaded content will be to be written to
    :param source_pretty_name: name of the source, for logging purposes
    :return: true if successfully downloaded all package sources false otherwise
    """
    print(f"downloading {source_pretty_name}: ...")
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            print(f"downloading {source_pretty_name}: failure", file=sys.stderr)
            return False
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"downloading {source_pretty_name}: ok")
    return True


def get_local_file_name(url: str) -> str:
    """
    Get package source local file name from it's url

    :param url: source of the file
    :return: filename
    """
    return url.split("/")[-1]


def fetch_package_sources(package, package_dest_dir: str) -> bool:
    """
    Download all pakcage sources for package

    :param package: package for which the sources are being downloaded
    :param package_dest_dir: direcotry to which the package sources are going to be written to
    :return: true if successfully downloaded all package sources false otherwise
    """
    if not os.path.isdir(package_dest_dir):
        os.makedirs(package_dest_dir)
    for url in package.src_urls:
        local_file_name = get_local_file_name(url)
        dest_file = f"{package_dest_dir}/{local_file_name}"
        # TODO: checksum
        if not os.path.isfile(dest_file):
            if not dwn_file(url, dest_file, local_file_name):  # lol
                return False
        else:
            print("Source:", local_file_name, "for package", package.name, "already downloaded")

    return True


def is_cached(package, lfs_dir: str) -> bool:
    """
    Check if all package sources for specified package has been downloaded

    :param package: package for which sources are being checked
    :param lfs_dir: package management system root directory
    :return: true if all satisfied false otherwise
    """
    cache_dir = f"{lfs_dir}/{PKG_CACHE_DIRECTORY}"
    package_dest_dir = f"{cache_dir}/{package.name}/{package.version}"
    return all([
        os.path.isfile(f"{package_dest_dir}/{get_local_file_name(url)}")
        for url
        in package.src_urls
    ])


def clear_cache(lfs_dir: str):
    """
    Delete downloaded package sources

    :param lfs_dir: package management system root directory
    """
    shutil.rmtree(f"{lfs_dir}/{PKG_CACHE_DIRECTORY}")

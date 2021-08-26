# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf 2021.05.30.tar.gz
    cd python-certifi-2021.05.30
    return
}

python_install() {
    export PYTHONPATH="$LFS/usr/lib/python3.7/site-packages/"
    python3.7 setup.py install --prefix="$LFS/usr"
    return
}

unpack_src && python_install

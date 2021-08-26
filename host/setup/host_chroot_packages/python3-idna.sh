# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf v3.2.tar.gz
    cd idna-3.2
    return
}

python_install() {
    export PYTHONPATH="$LFS/usr/lib/python3.7/site-packages/"
    python3.7 setup.py install --prefix="$LFS/usr"
    return
}

unpack_src && python_install

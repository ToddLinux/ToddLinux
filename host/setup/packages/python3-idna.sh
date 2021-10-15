# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf v3.2.tar.gz
    cd idna-3.2
    return
}

python_install() {
    export PYTHONPATH="$TODD_FAKE_ROOT_DIR/usr/lib/python3.7/site-packages/"
    mkdir -p $TODD_FAKE_ROOT_DIR/usr/lib/python3.7/site-packages/
    python3.7 setup.py install --prefix="$TODD_FAKE_ROOT_DIR/usr"
    return
}

unpack_src && python_install

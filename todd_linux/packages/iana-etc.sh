# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

unpack_src() {
    tar xf iana-etc-20210611.tar.gz
    cd iana-etc-20210611
    return
}

copy() {
    mkdir $TODD_FAKE_ROOT_DIR/etc
    cp services protocols $TODD_FAKE_ROOT_DIR/etc
    return
}

unpack_src && copy

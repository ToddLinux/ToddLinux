#!/bin/bash
set -euo pipefail

echo "Hello, World"

unpack_src() {
    true
}

configure() {
    true
}

make_install() {
    true
}

unpack_src && configure && make_install

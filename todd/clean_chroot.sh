# See LICENSE for license details.
#!/bin/bash
set -euo pipefail

find /usr/{lib,libexec} -name \*.la -delete
rm -rf /usr/share/{info,man,doc}/*

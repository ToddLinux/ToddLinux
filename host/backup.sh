#!/bin/bash

[[ -d backup ]] || mkdir backup

FILENAME=$(date +%Y%m%d-%H%M%S)

cd backup

if [[ $# -ne 1 ]]; then
    echo Specify LFS_PATH as first argument
    exit 1
fi

LFS_PATH=$1
if [[ ! -d "$LFS_PATH" ]]; then
    echo not a valid path
    exit 1
fi

echo "It will take a while..~.."
tar cf "${FILENAME}.tar" --exclude="${LFS_PATH}/dev" --exclude="${LFS_PATH}/proc" --exclude="${LFS_PATH}/run" --exclude="${LFS_PATH}/sys" "$LFS_PATH"

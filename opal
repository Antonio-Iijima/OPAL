#!/bin/sh

path="$(dirname $0)"

case "$1" in
    "docs") rm -r "${path}/docs"
            pdoc3 --html --force --output-dir "${path}/docs" "${path}/src"
            mv "${path}/docs/src/"* "${path}/docs"
            rm -r "${path}/docs/src"
    ;;
    "ide") python3 "${path}/IDE.py"
    ;;
    *) python3 "${path}/LANG.py" $@
esac

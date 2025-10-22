#!/bin/sh

path="$(dirname $0)"

case "$1" in
    "docs") mv "${path}/docs/_config.yml" "$path"
            rm -r "${path}/docs"
            pdoc3 --html --force --output-dir "${path}/docs" "${path}/src"
            mv "${path}/docs/src/"* "${path}/docs"
            rm -r "${path}/docs/src"
            mv "${path}/_config.yml" "${path}/docs"
    ;;
    "ide") python3 "${path}/IDE.py"
    ;;
    *) python3 "${path}/LANG.py" $@
esac

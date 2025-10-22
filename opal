#!/bin/sh


path="$(dirname "$BASH_SOURCE")"

case "$1" in
    "docs") rm -r "${path}/docs/"*
            if [ "$2" = "-q" ]
            then pdoc3 --html --force --output-dir "${path}/docs" "${path}/src" > /dev/null
            else pdoc3 --html --force --output-dir "${path}/docs" "${path}/src"
            fi
            mv "${path}/docs/src/"* "${path}/docs"
            rm -r "${path}/docs/src"
    ;;
    "ide") python3 "${path}/IDE.py"
    ;;
    *) python3 "${path}/LANG.py" $@
esac

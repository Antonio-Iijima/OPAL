#!/bin/sh


path="$(dirname "$BASH_SOURCE")"
venv="$path"/.venv

if [ "$1" = "build" ]; then

    [ -d "$venv" ] && rm -r "$venv"
    python3 -m venv "$venv"
    "$venv"/bin/pip install -r "$path"/requirements.txt $@

else
    . "$venv"/bin/activate

    case "$1" in
        "build-docs")
            rm -r "$path"/docs/*
            
            [ "$2" = "-q" ] && pdoc3 --html --force --output-dir "$path"/docs "$path"/src > /dev/null \
            || pdoc3 --html --force --output-dir "$path"/docs "$path"/src

            mv "${path}/docs/src/"* "$path"/docs
            rm -r "$path"/docs/src
        ;;
        "-ide")
            shift
            python3 "$path"/IDE.py $@
        ;;
        *)
            python3 "$path"/LANG.py $@
    esac

    deactivate

fi

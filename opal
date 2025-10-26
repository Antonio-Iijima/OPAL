#!/bin/sh


path="$(dirname "$BASH_SOURCE")"
venv="$path"/.venv

case "$1" in
    "--help")
        python3 "$path"/LANG.py
        cat "$path"/.help
        ;;
    "--build")
        shift
        [ -d "$venv" ] && rm -r "$venv"
        python3 -m venv "$venv"
        "$venv"/bin/pip install -r "$path"/.requirements $@
        ;;
    *)
        . "$venv"/bin/activate

        case "$1" in
            "--build-docs")
                rm -r "$path"/docs/*
                
                [ "$2" = "-q" ] && pdoc3 --html --force --output-dir "$path"/docs "$path"/src > /dev/null \
                || pdoc3 --html --force --output-dir "$path"/docs "$path"/src

                mv "${path}/docs/src/"* "$path"/docs
                rm -r "$path"/docs/src
            ;;
            "--docs-dev")
                pdoc --http : "$path"/src/
            ;;
            "--ide")
                shift
                python3 "$path"/IDE.py $@
            ;;
            "--ide-dev")
                shift
                textual run --dev "$path"/IDE.py $@
            ;;
            "--console")
                shift
                textual console
            ;;
            *)
                python3 "$path"/LANG.py $@
        esac

        deactivate

esac

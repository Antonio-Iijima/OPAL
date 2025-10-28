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
                pdoc --math --footer-text "$(python3 "$path"/LANG.py)" --output-directory "$path"/docs "$path"/src
            ;;
            "--docs-dev")
                pdoc --math --footer-text "$(python3 "$path"/LANG.py)" --port 8080 "$path"/src
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

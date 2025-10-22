#!/bin/sh


if [ $1 = ide ]; then
    python3 src/ide/main.py
else
    python3 src/lang/main.py $@
fi

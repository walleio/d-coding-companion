#!/usr/bin/env zsh

file=$(<"$1")
python3 main.py "$1" "$file"

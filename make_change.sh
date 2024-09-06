#!/usr/bin/env zsh

sed -i" " "${2}s/.*/${3}/" "$1"

cat "$1"

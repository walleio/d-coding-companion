#!/usr/bin/env zsh

touch temporary
if [ "$2" = "gcc" ]; then
    printf "%s\n" "$1" > temporary.c
elif [ "$2" = "swift" ]; then
    echo "$1" > temporary.swift
elif [ "$2" = "swift" ]; then
    echo "$1" > temporary.swift
elif [ "$2" = "javac" ]; then
    echo "$1" > "$3"
else
    echo "$1" > temporary
fi

if [ "$2" = "./" ]; then
    chmod +x temporary
    error_output=$("${2}temporary" 2>&1)
elif [ "$2" = "gcc" ]; then
    error_output=$("$2" temporary.c 2>&1)
elif [ "$2" = "swift" ]; then
    error_output=$("$2" temporary.swift 2>&1)
elif [ "$2" = "javac" ]; then
    error_output=$("$2" "$3" 2>&1)
else
    error_output=$("$2" temporary 2>&1)
fi

if [ $? -ne 0 ]; then
    echo "$error_output"
else
    echo "no error"
fi

rm temporary*

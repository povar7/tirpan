#!/bin/sh

find . -name '*.pyc' -exec rm {} \;
rm -f tests/binop01.py tests/test_binop01.py

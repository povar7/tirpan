#!/bin/sh

find . -name '*.pyc' -exec rm {} \;
rm -f tests/unop01.py tests/test_unop01.py
rm -f tests/binop01.py tests/test_binop01.py

#!/bin/sh

python tests/gen_test_unop01.py
python tests/gen_test_binop01.py
./clean_pyc.sh
python tests/testrunner.py

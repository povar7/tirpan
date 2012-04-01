#!/bin/sh

python tests/gen_test_binop01.py
for test_file in tests/test_*.py; do
    python $test_file
done

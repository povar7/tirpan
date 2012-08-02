#!/bin/sh

python tests/gen_test_unop01.py
python tests/gen_test_binop01.py
for test_file in tests/test_*.py; do
    echo $test_file
    python $test_file
done

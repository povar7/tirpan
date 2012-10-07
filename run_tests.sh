#!/bin/sh

python tests/gen_test_unop01.py
python tests/gen_test_binop01.py
for test_file in tests/test_*.py; do
    echo
    echo $test_file
    ./clean_pyc.sh
    python $test_file
done

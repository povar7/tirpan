#!/bin/sh

for test_file in tests/test_*.py; do
    python $test_file
done

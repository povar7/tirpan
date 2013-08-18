#!/bin/sh

for f in tests/accept*.py; do
	python $f
done

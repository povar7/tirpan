#!/bin/sh

SUCCESS=1

for f in tests/accept*.py; do
	python $f
	if [ $? -ne 0 ]; then
		SUCCESS=0
	fi
done

if [ $SUCCESS -ne 0 ]; then
	echo OK
fi

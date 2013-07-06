#!/bin/sh

find . -name "*.py" -exec wc -L {} \; | sort -n | tail -1

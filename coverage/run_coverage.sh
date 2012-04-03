#!/bin/bash

if [ -e ".coverage" ]; then
    rm .coverage
fi

if [ -e "htmlcov" ]; then
    rm -r htmlcov
fi

python-coverage run ../test/run_tests.py > out.txt
python-coverage html --omit="/usr/share/*,/*test*"
firefox htmlcov/index.html
rm out.txt

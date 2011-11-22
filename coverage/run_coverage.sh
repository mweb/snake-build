#!/bin/bash

if [ -e ".coverage" ]; then
    rm .coverage
fi

if [ -e "htmlcov" ]; then
    rm -r htmlcov
fi

python-coverage run ../test/run_tests.py
python-coverage html
firefox htmlcov/index.html

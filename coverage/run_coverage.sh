#!/bin/bash

if [ -e ".coverage" ]; then
    rm .coverage
fi

python-coverage run ../test/run_tests.py
python-coverage html
firefox htmlcov/index.html

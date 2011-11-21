#!/bin/bash

rm .coverage
python-coverage run ../test/run_tests.py
python-coverage html
firefox htmlcov/index.html

#!/bin/bash

set -e

LONG=0
if [ $# -eq 1 ]; then
    if [ $1 = "long" ]; then
        LONG=1
    fi
fi

if [ -e ".coverage" ]; then
    rm .coverage
fi

if [ -e "htmlcov" ]; then
    rm -r htmlcov
fi

python-coverage run ../test/run_tests.py > out.txt
# run long tests?
if [ ${LONG} -eq 1 ]; then
    cd ../test/integration_test/
    ./test_resources.sh /tmp/ cov
    cd -
    mv .coverage .coverage.1
    cp ../test/integration_test/server/.coverage .coverage.2
    cp ../test/integration_test/client/.coverage .coverage.3
    python-coverage combine
fi

python-coverage html --omit="/usr/share/*,/*test*"
firefox htmlcov/index.html
rm out.txt

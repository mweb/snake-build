#!/bin/bash
#
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
#
# This file is part of Snake-Build.
#
# Snake-Build is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Snake-Build is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Snake-Build.  If not, see <http://www.gnu.org/licenses/>

# this script runs some integration tests for the resource server and the
# resource client.
#
# This script takes the following paramters:
# @PARAM1 TMP_DIRECTORY = The directory to use for temporary config files
#   (required to create the git repos for config)
# @PARAM2 COVERAGE = If set then python-coverage is used instead of python to
#   store the coverate informations.

set -e

if [ $# -eq 1 ]; then
    COVERAGE=0
elif [ $# -eq 2 ]; then
    COVERAGE=1
else
    echo "This script needs a valid tmp directory as a parameter. Abort."
    exit -1
fi

TMP_DIRECTORY=$1

# this is the entry point of the script
function main {
    create_configs "${TMP_DIRECTORY}/sb_integration"
    server_config="${TMP_DIRECTORY}/sb_integration/server_resource.conf"
    client_config="${TMP_DIRECTORY}/sb_integration/client_resource.conf"

    if [ -d server ]; then
        rm -rf server
    fi
    if [ -d client ]; then
        rm -rf client
    fi

    if [ ${COVERAGE} -eq 1 ]; then
        mkdir server
        mkdir client
    fi

    echo "Check with master"
    run_server ${server_config}
    sleep 1
    check_resources ${client_config} 4
    stop_server
    sleep 1
    echo "OK"
    echo

    echo "Check with v1.0"
    run_server ${server_config} v1.0
    sleep 1
    check_resources ${client_config} 2
    stop_server
    sleep 1
    echo "OK"
    echo

    echo "Check with v2.0"
    run_server ${server_config} v2.0
    check_resources ${client_config} 4
    sleep 1
    stop_server
    echo "OK"
    echo
}

# run the server with the given version of the config
function run_server {
    if [ $# -eq 2 ]; then
        PARAMS="--background --tag $2"
    else
        PARAMS="--background"
    fi

    if [ ${COVERAGE} -eq 0 ]; then
        python ../../bin/sb-resourceserver start ${PARAMS}
    else
        cd server
        python-coverage run -a ../../../bin/sb-resourceserver --configfile=$1 start ${PARAMS}
        cd -
    fi
}

# send stop signal to the server running in the background
function stop_server {
    if [ ${COVERAGE} -eq 0 ]; then
        python ../../bin/sb-resourceserver stop
    else
        cd server
        python-coverage run -a ../../../bin/sb-resourceserver stop
        cd -
    fi
}

# run the client command and see if the test resources are available as
# expected (the second paramter specifies the number of test resources that
# need to be available
function check_resources {
    # add one for the header
    expected_count=$(($2+1))

    if [ ${COVERAGE} -eq 0 ]; then
        count=`python ../../bin/sb-resourceclient --configfile=$1 status | wc -l`
    else
        cd client
        count=`python-coverage run -a ../../../bin/sb-resourceclient --configfile=$1 status | wc -l`
        cd -
    fi

    if [ ${count} -ne ${expected_count} ]; then
        echo "ERROR unexpected count received: ${count} but expected: ${expected_count}"
        exit -1
    fi
}

# create the config files including a git repos with two tags to use for tests
function create_configs {
    tmp_dir=$1
    if [ -d ${tmp_dir} ]; then
        rm -rf ${tmp_dir}
    fi
    mkdir -p ${tmp_dir}/bares
    mkdir -p ${tmp_dir}/resources

    cp data/client_resource.conf data/server_resource.conf ${tmp_dir}
    cp data/resource1.resource data/resource2.resource ${tmp_dir}/resources

    cd ${tmp_dir}/resources/
    git init
    git add *.resource
    git commit -m "added files"
    git tag -a v1.0 -m "created v1.0 tag"
    cd -

    cp data/resource3.resource data/resource4.resource ${tmp_dir}/resources
    cd ${tmp_dir}/resources/
    git add *.resource
    git commit -m "added more files"
    git tag -a v2.0 -m "created v2.0 tag"
    cd -

    git clone ${tmp_dir}/resources ${tmp_dir}/bares/resources.git --bare
    rm -rf ${tmp_dir}/resources

    echo "repository_local=${tmp_dir}" >> ${tmp_dir}/server_resource.conf
    echo "repository_data=${tmp_dir}/bares" >> ${tmp_dir}/server_resource.conf
}

main

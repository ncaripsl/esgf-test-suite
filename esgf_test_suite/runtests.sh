#!/bin/bash

# Set params.
TYPE=$1

# Extend python path.
export PYTHONPATH=$PYTHONPATH:$PWD

# Activate target virtual env.
#source ~/virtualenv/venv/bin/activate

# Serialization tests.
#if [ $TYPE = "s" ]; then
#    echo :: Executing serialization tests
#    nosetests -v -s .../test_serialization.py

# Publishing tests.
#elif [ $TYPE = "p" ]; then
#    echo :: Executing publishing tests
#    nosetests -v -s .../test_publishing.py

# General tests.
#elif [ $TYPE = "g" ]; then
#    echo :: Executing general  tests
#    nosetests -v -s .../test_general.py

#fi

#exit 0
#
#~/virtualenv/venv/bin/python ~/virtualenv/venv/bin/nosetests `python -m site --user-site`/esgf_test_suite-0.1-py2.7.egg/esgf_test_suite --nologcapture -v --nocapture
#nosetests `python -m site --user-site`/esgf_test_suite-0.1-py2.7.egg/esgf_test_suite -v --nocapture
_script="$(readlink -f ${BASH_SOURCE[0]})"
_base="$(dirname $_script)"
echo $_script
echo $_base

#nosetests 

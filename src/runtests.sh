#!/bin/bash

# Set params.
TYPE=$1

# Extend python path.
export PYTHONPATH=$PYTHONPATH:$PWD

# Activate target virtual env.
#source .../venv/bin/activate

#if [ $TYPE = "s" ]; then
#    nosetests -v -s .../tests/test_.py

#elif [ $TYPE = "g" ]; then
#    nosetests -v -s .../tests/test_.py

#else
#    nosetests -v -s .../tests/
#fi

#exit 0

nosetests -v -s --with-html

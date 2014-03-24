esgf_test_suite
===============

Python nosetests scripts for ESGF integration test and validation

## Purpose and limits of this tool:

ESGF Test Suite is a full python application. It is designed to perform integration tests on ESGF nodes. At this point of time, the scope is to test a single data node and its three peer services (idp services, index services and compute services).  
ESGF Test Suite offers to run high level tests from a desktop so the tested node can be validated from the end user's perspective. 
Current developments will also let admins to test and validate the stack by running tests on the node itself.

## Requirements:

Shell environment
Python 2.6
myproxy-logon
globus-url-copy
firefox

## Installation:

pip install esgf_test_suite

## Configuration:

[Python eggs installation dir]/esgf_test_suite/configuration.ini 
Modify the nodes section. If several nodes are specified, they all should be in the same federation. Account section do not need to be modified.

## Usage:

[Python eggs installation dir]/esgf_test_suite/runtests.sh


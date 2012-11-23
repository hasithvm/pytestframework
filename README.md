pytestframework
===============

A framework for testing competition entries, written in Python. Uses separate threads to test and verify program correctness using a defined set of testcases.

Currently supports C/C++ and Python for the compiler component, and any application that writes/reads to stdout/stdin for the test component. Tests are currently limited to a check-expect policy: stdout must match the output specified in a testcase XML listing.

Usage
=====

python run_tests.py $sourcefile $testcase



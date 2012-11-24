Copyright (C) 2012 Hasith Vidanamadura

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

pytestframework
===============

A framework for testing competition entries, written in Python. Uses separate threads to test and verify program correctness using a defined set of testcases.

Currently supports C/C++ and Python for the compiler component, and any application that writes/reads to stdout/stdin for the test component. Tests are currently limited to a check-expect policy: stdout must match the output specified in a testcase XML listing.

Usage
=====

python run_tests.py $sourcefile $testcase





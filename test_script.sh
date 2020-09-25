#!/bin/sh
createdb capstone_test
export TEST_DB_NAME="capstone_test"
export TEST_DB_PATH="username:password@localhost:5432"
python test_app.py
dropdb capstone_test


#!/bin/bash

find . -name "*.py" | xargs pylint --disable=missing-docstring

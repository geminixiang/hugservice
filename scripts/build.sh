#!/bin/bash
# basic reference for writing script for travis

set -ev
poetry export --without-hashes -f requirements.txt -o requirements.txt

cat requirements.txt
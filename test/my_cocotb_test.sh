#!/bin/bash


pushd ../ || exit 1

python3 -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install cocotb

command -v cocotb-config
cocotb-config --makefiles

make -C test clean
make -C test

popd || exit 1
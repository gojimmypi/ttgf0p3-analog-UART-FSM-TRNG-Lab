#!/bin/bash

# Stay inside TT-local area.
export TT_DIR="$HOME/ttsetup"
export YOSYS_SRC="/mnt/c/workspace/yosys"
export YOSYS_PREFIX="$TT_DIR/yosys-pyosys"

JOBS="${JOBS:-$(nproc)}"

mkdir -p "$TT_DIR/src"

# Get source if not already present.
#if [ ! -d "$YOSYS_SRC/.git" ]; then
#    git clone https://github.com/YosysHQ/yosys.git "$YOSYS_SRC"
#fi

cd "$YOSYS_SRC"

# Use your active TT venv Python.
python3 -m pip install pybind11 cxxheaderparser

# Clean local build dir only.
rm -rf "$YOSYS_SRC/build" "$YOSYS_PREFIX"


make -j"${JOBS}" \
    PREFIX="${YOSYS_PREFIX}" \
    ENABLE_PYOSYS=1 \
    PYOSYS_USE_UV=0
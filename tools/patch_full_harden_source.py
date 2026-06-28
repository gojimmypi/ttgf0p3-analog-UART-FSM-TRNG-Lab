#!/usr/bin/env python3
"""Temporarily make src/project.v acceptable to tt_tool.py --harden.

Analog custom-GDS submissions can expose VDPWR/VGND in their submitted
Verilog model. The regular Tiny Tapeout hardening path validates the user
module interface and rejects those power pins as extra ports. This script is
used only by tools/full_harden_local.sh while generating a real hardened GDS.
The caller backs up and restores src/project.v after hardening.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

VGND_PORT_RE = re.compile(r"^[ \t]*inout[ \t]+wire[ \t]+VGND,[ \t]*\n", re.MULTILINE)
VDPWR_PORT_RE = re.compile(r"^[ \t]*inout[ \t]+wire[ \t]+VDPWR,[ \t]*\n", re.MULTILINE)

UNUSED_ASSIGN_RE = re.compile(
    r"assign[ \t]+unused_ok[ \t]*=[ \t]*&\{ena,[ \t]*clk,[ \t]*rst_n,[ \t]*uio_in,[ \t]*VGND,[ \t]*VDPWR\};"
)

UNUSED_ASSIGN_REPLACEMENT = "assign unused_ok = &{ena, clk, rst_n, uio_in};"


def patch_project(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    text, vgnd_count = VGND_PORT_RE.subn("", text, count=1)
    text, vdpwr_count = VDPWR_PORT_RE.subn("", text, count=1)
    text, assign_count = UNUSED_ASSIGN_RE.subn(UNUSED_ASSIGN_REPLACEMENT, text, count=1)

    if vgnd_count != 1:
        raise RuntimeError("Did not find exactly one top-level VGND port in src/project.v")

    if vdpwr_count != 1:
        raise RuntimeError("Did not find exactly one top-level VDPWR port in src/project.v")

    if assign_count != 1:
        raise RuntimeError(
            "Did not find exactly one unused_ok assignment that references VGND/VDPWR"
        )

    if "module tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab" not in text:
        raise RuntimeError("Patch removed or hid the GF180 top module declaration")

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"Patched {path} for full hardening")
    print("  removed top-level VGND/VDPWR ports")
    print("  removed VGND/VDPWR from unused_ok")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="src/project.v", type=Path)
    args = parser.parse_args()

    patch_project(args.path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

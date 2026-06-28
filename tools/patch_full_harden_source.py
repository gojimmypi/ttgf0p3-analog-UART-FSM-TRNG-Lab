#!/usr/bin/env python3
"""Temporarily make src/project.v acceptable to tt_tool.py --harden.

Analog custom-GDS submissions can expose VDPWR/VGND in their submitted
Verilog model. The regular Tiny Tapeout hardening path validates the user
module interface and rejects those power pins as extra ports.

For this GF180 analog build, info.yaml allows six analog pins, ua[0] through
ua[5]. The cleaned analog DEF template therefore exposes only ua[0] through
ua[5]. This script also narrows the harden-time top-level ua port from [7:0]
to [5:0] so the design ports match that template.

This script is used only by tools/full_harden_local.sh or
full_harden_artifact.sh while generating a real hardened GDS. The caller backs
up and restores src/project.v after hardening.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

VGND_PORT_RE = re.compile(r"^[ \t]*inout[ \t]+wire[ \t]+VGND,[ \t]*\n", re.MULTILINE)
VDPWR_PORT_RE = re.compile(r"^[ \t]*inout[ \t]+wire[ \t]+VDPWR,[ \t]*\n", re.MULTILINE)

UA_PORT_RE = re.compile(
    r"^[ \t]*inout[ \t]+wire[ \t]+\[7:0\][ \t]+ua,[^\n]*\n",
    re.MULTILINE,
)

UNUSED_ASSIGN_RE = re.compile(
    r"assign[ \t]+unused_ok[ \t]*=[ \t]*&\{ena,[ \t]*clk,[ \t]*rst_n,[ \t]*uio_in,[ \t]*VGND,[ \t]*VDPWR\};"
)

UNUSED_ASSIGN_REPLACEMENT = "assign unused_ok = &{ena, clk, rst_n, uio_in};"


def patch_ua_port(match: re.Match[str]) -> str:
    return match.group(0).replace("[7:0]", "[5:0]", 1)


def patch_project(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    text, vgnd_count = VGND_PORT_RE.subn("", text, count=1)
    text, vdpwr_count = VDPWR_PORT_RE.subn("", text, count=1)
    text, ua_count = UA_PORT_RE.subn(patch_ua_port, text, count=1)
    text, assign_count = UNUSED_ASSIGN_RE.subn(UNUSED_ASSIGN_REPLACEMENT, text, count=1)

    if vgnd_count != 1:
        raise RuntimeError("Did not find exactly one top-level VGND port in src/project.v")

    if vdpwr_count != 1:
        raise RuntimeError("Did not find exactly one top-level VDPWR port in src/project.v")

    if ua_count != 1:
        raise RuntimeError("Did not find exactly one top-level ua[7:0] port in src/project.v")

    if assign_count != 1:
        raise RuntimeError(
            "Did not find exactly one unused_ok assignment that references VGND/VDPWR"
        )

    if "module tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab" not in text:
        raise RuntimeError("Patch removed or hid the GF180 top module declaration")

    if "inout  wire [7:0] ua" in text:
        raise RuntimeError("Top-level ua port still appears to be [7:0] after patch")

    if "inout  wire [5:0] ua" not in text:
        raise RuntimeError("Top-level ua port was not patched to [5:0]")

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"Patched {path} for full hardening")
    print("  removed top-level VGND/VDPWR ports")
    print("  removed VGND/VDPWR from unused_ok")
    print("  changed top-level ua port from [7:0] to [5:0]")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="src/project.v", type=Path)
    args = parser.parse_args()

    patch_project(args.path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

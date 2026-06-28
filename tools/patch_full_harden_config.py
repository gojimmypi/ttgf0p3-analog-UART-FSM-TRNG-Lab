#!/usr/bin/env python3
"""Patch Tiny Tapeout hardening config for the GF180 analog full-project build.

The standard tt_tool.py --create-user-config step currently writes the normal
1x2 digital DEF template.  That template does not contain the ua[*] analog
pins, so a full analog RTL hardening run would either fail at the DEF-template
stage or produce a layout that does not match the analog submission interface.

This script is intentionally small and repo-local.  Run it immediately after
`tt_tool.py --gf --create-user-config` and before `tt_tool.py --gf --harden`.
It updates src/user_config.json and src/config_merged.json so LibreLane hardens
this project against the GF180 analog 1x2 frame.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any

TOP = "tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab"
ANALOG_TEMPLATE = Path("mag/tt_analog_1x2.def")
PATCHED_TEMPLATE = Path("build/full_harden/tt_analog_1x2_vdpwr.def")
USER_CONFIG = Path("src/user_config.json")
BASE_CONFIG = Path("src/config.json")
MERGED_CONFIG = Path("src/config_merged.json")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def create_vdpwr_template() -> None:
    if not ANALOG_TEMPLATE.is_file():
        raise FileNotFoundError(ANALOG_TEMPLATE)

    text = ANALOG_TEMPLATE.read_text(encoding="utf-8")

    # The analog frame contains the correct analog pins and rows, but the
    # special power net is named VPWR.  This project's GF180 analog top and TT
    # precheck use VDPWR, so make a generated DEF copy with that name.
    text = re.sub(r"\bVPWR\b", "VDPWR", text)

    PATCHED_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
    PATCHED_TEMPLATE.write_text(text, encoding="utf-8", newline="\n")


def patch_config() -> None:
    if not USER_CONFIG.is_file():
        raise FileNotFoundError(
            f"{USER_CONFIG} not found. Run tt_tool.py --gf --create-user-config first."
        )

    create_vdpwr_template()

    user_config = read_json(USER_CONFIG)

    user_config.update(
        {
            "DESIGN_NAME": TOP,
            # config_merged.json lives in src/, so dir::../build/... resolves
            # to this generated analog DEF in the repository root.
            "FP_DEF_TEMPLATE": "dir::../build/full_harden/tt_analog_1x2_vdpwr.def",
            # Match the analog DEF/LEF dimensions: 346.640 x 325.360 um.
            "DIE_AREA": "0 0 346.64 325.36",
            "VDD_PIN": "VDPWR",
            "GND_PIN": "VGND",
            "RT_MAX_LAYER": "Metal4",
            # Global placement failed at 71.451% actual utilization with the
            # default 60% density target.  Keep the fixed analog frame, but let
            # global placement use a density above OpenROAD's suggested 72%.
            "PL_TARGET_DENSITY_PCT": 75,
        }
    )

    write_json(USER_CONFIG, user_config)

    if BASE_CONFIG.is_file():
        merged = read_json(BASE_CONFIG)
        merged.update(user_config)
        write_json(MERGED_CONFIG, merged)

    print("Patched full-project GF180 analog hardening config")
    print(f"  template: {PATCHED_TEMPLATE}")
    print(f"  DESIGN_NAME: {user_config['DESIGN_NAME']}")
    print(f"  FP_DEF_TEMPLATE: {user_config['FP_DEF_TEMPLATE']}")
    print(f"  DIE_AREA: {user_config['DIE_AREA']}")
    print(f"  VDD_PIN: {user_config['VDD_PIN']}")
    print(f"  GND_PIN: {user_config['GND_PIN']}")
    print(f"  RT_MAX_LAYER: {user_config['RT_MAX_LAYER']}")
    print(f"  PL_TARGET_DENSITY_PCT: {user_config['PL_TARGET_DENSITY_PCT']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    patch_config()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

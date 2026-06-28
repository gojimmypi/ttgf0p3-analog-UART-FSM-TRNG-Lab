#!/usr/bin/env python3
"""Patch generated LEF/GDS for the GF180 analog scaffold.

Magic exports the analog frame pins, but the scaffold also needs short inward
metal stubs for the enabled analog pins and explicit VGND/VDPWR project power
pins for Tiny Tapeout precheck.  This script makes those edits deterministic
for the local export flow.
"""
from __future__ import annotations

import argparse
from pathlib import Path

UA_LEF_RECTS = {
    "325.820 0.000 328.820 1.000": "325.820 0.000 328.820 30.000",
    "282.140 0.000 285.140 1.000": "282.140 0.000 285.140 30.000",
    "238.460 0.000 241.460 1.000": "238.460 0.000 241.460 30.000",
    "194.780 0.000 197.780 1.000": "194.780 0.000 197.780 30.000",
    "151.100 0.000 154.100 1.000": "151.100 0.000 154.100 30.000",
    "107.420 0.000 110.420 1.000": "107.420 0.000 110.420 30.000",
}

GDS_STUBS = [
    (325.82, 1.0, 328.82, 30.0),
    (282.14, 1.0, 285.14, 30.0),
    (238.46, 1.0, 241.46, 30.0),
    (194.78, 1.0, 197.78, 30.0),
    (151.10, 1.0, 154.10, 30.0),
    (107.42, 1.0, 110.42, 30.0),
]

POWER_LEF = '''  PIN VGND
    DIRECTION INOUT ;
    USE GROUND ;
    PORT
      LAYER Metal4 ;
        RECT 0.000 20.000 1.000 305.360 ;
    END
  END VGND
  PIN VDPWR
    DIRECTION INOUT ;
    USE POWER ;
    PORT
      LAYER Metal4 ;
        RECT 345.640 20.000 346.640 305.360 ;
    END
  END VDPWR
'''


def patch_lef(path: Path, top: str) -> None:
    text = path.read_text()
    for old, new in UA_LEF_RECTS.items():
        text = text.replace(f"RECT {old} ;", f"RECT {new} ;")

    if "PIN VGND" not in text:
        marker = f"END {top}\n"
        if marker not in text:
            raise RuntimeError(f"Could not find LEF macro end marker {marker.strip()}")
        text = text.replace(marker, POWER_LEF + marker)

    path.write_text(text)


def patch_gds(path: Path) -> None:
    import gdstk

    lib = gdstk.read_gds(str(path))
    top_cells = lib.top_level()
    if len(top_cells) != 1:
        raise RuntimeError("Expected exactly one top-level GDS cell")
    cell = top_cells[0]

    for x1, y1, x2, y2 in GDS_STUBS:
        cell.add(gdstk.rectangle((x1, y1), (x2, y2), layer=46, datatype=0))

    cell.add(gdstk.rectangle((0.0, 20.0), (1.0, 305.36), layer=46, datatype=0))
    cell.add(gdstk.rectangle((345.64, 20.0), (346.64, 305.36), layer=46, datatype=0))

    labels = {label.text for label in cell.labels}
    if "VGND" not in labels:
        cell.add(gdstk.Label("VGND", (0.5, 162.68), rotation=1.57079632679, layer=46, texttype=10))
    if "VDPWR" not in labels:
        cell.add(gdstk.Label("VDPWR", (346.14, 162.68), rotation=1.57079632679, layer=46, texttype=10))

    lib.write_gds(str(path))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", required=True)
    parser.add_argument("--lef", required=True)
    parser.add_argument("--gds", required=True)
    args = parser.parse_args()

    patch_lef(Path(args.lef), args.top)
    patch_gds(Path(args.gds))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

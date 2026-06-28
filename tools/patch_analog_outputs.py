#!/usr/bin/env python3
"""Patch generated LEF/GDS for the GF180 analog scaffold.

Keep the LEF analog pin dimensions identical to the TT analog template.  Add
only the post-export items that do not belong in the template pin geometry:
explicit full-height project power ports in LEF/GDS and short inward GDS metal
stubs for enabled analog pins.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

# GDS coordinates are in microns.  These stubs intentionally start just above
# the template ua pin rectangles so the LEF pin rectangles remain unchanged
# while the GDS has adjacent inward metal for precheck connectivity.
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
        RECT 0.000 0.000 1.000 325.360 ;
    END
  END VGND
  PIN VDPWR
    DIRECTION INOUT ;
    USE POWER ;
    PORT
      LAYER Metal4 ;
        RECT 345.640 0.000 346.640 325.360 ;
    END
  END VDPWR
'''


def remove_pin_block(text: str, pin: str) -> str:
    pattern = re.compile(
        rf"^[ \t]*PIN[ \t]+{re.escape(pin)}\n.*?^[ \t]*END[ \t]+{re.escape(pin)}\n",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub("", text)


def patch_lef(path: Path, top: str) -> None:
    text = path.read_text()

    # Normalize project power pins.  Do not modify the template ua[*] pin
    # rectangles; precheck compares those dimensions against tt_analog_1x2.def.
    text = remove_pin_block(text, "VGND")
    text = remove_pin_block(text, "VDPWR")

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

    cell.add(gdstk.rectangle((0.0, 0.0), (1.0, 325.36), layer=46, datatype=0))
    cell.add(gdstk.rectangle((345.64, 0.0), (346.64, 325.36), layer=46, datatype=0))

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

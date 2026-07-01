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

# Small real on-chip passive structure tied to ua[5].  The ua[5] side uses
# the normal inward ua[5] metal stub plus two top-metal pickup plates.  The
# other side is tied to the nearby template VGND Metal4 rail.  This is not a
# precision capacitor, but it is real silicon layout: top-metal area and
# same-layer fringe capacitance that the ua[5] charge/release/sample RTL can
# exercise after fabrication.  The coordinates stay in the bottom analog-frame
# region so the LEF pin rectangles remain unchanged.  Keep every added Metal4
# segment at least 0.40 um wide and spaced by at least 0.40 um so the patch has
# margin over the GF180 M4.1/M4.2a 0.28 um rules.
UA5_PASSIVE_CAP_RECTS = [
    # Extend the local VGND rail downward to the passive finger region.
    (99.92, 2.00, 101.52, 3.90),
    # Grounded M4 bridge and vertical finger beside the ua[5] probe stub.
    (99.92, 2.00, 106.85, 2.40),
    (106.45, 2.00, 106.85, 30.00),
    # ua[5]-connected pickup plates, touching the ua[5] inward stub.
    (109.80, 1.20, 130.00, 1.60),
    (109.80, 2.80, 130.00, 3.20),
    (129.60, 1.20, 130.00, 3.20),
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


def add_rect_once(cell, gdstk, rect: tuple[float, float, float, float]) -> None:
    x1, y1, x2, y2 = rect
    target = (round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3))

    for polygon in cell.polygons:
        if polygon.layer != 46 or polygon.datatype != 0:
            continue
        bbox = polygon.bounding_box()
        if bbox is None:
            continue
        found = (
            round(float(bbox[0][0]), 3),
            round(float(bbox[0][1]), 3),
            round(float(bbox[1][0]), 3),
            round(float(bbox[1][1]), 3),
        )
        if found == target:
            return

    cell.add(gdstk.rectangle((x1, y1), (x2, y2), layer=46, datatype=0))


def patch_gds(path: Path) -> None:
    import gdstk

    lib = gdstk.read_gds(str(path))
    top_cells = lib.top_level()
    if len(top_cells) != 1:
        raise RuntimeError("Expected exactly one top-level GDS cell")
    cell = top_cells[0]

    for rect in GDS_STUBS:
        add_rect_once(cell, gdstk, rect)

    for rect in UA5_PASSIVE_CAP_RECTS:
        add_rect_once(cell, gdstk, rect)

    add_rect_once(cell, gdstk, (0.0, 0.0, 1.0, 325.36))
    add_rect_once(cell, gdstk, (345.64, 0.0, 346.64, 325.36))

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

#!/usr/bin/env python3
"""Check that a custom-GDS submission contains real layout geometry.

The GF180 analog template by itself can pass basic packaging checks while still
containing only the project boundary, Metal4 pin rectangles, and labels.  That
is not a useful final design.  This script intentionally uses only the Python
standard library so it can run in GitHub Actions before custom_gds packaging.
"""
from __future__ import annotations

import argparse
import struct
from collections import Counter
from pathlib import Path

REC_BOUNDARY = 0x08
REC_PATH = 0x09
REC_SREF = 0x0A
REC_AREF = 0x0B
REC_TEXT = 0x0C
REC_LAYER = 0x0D
REC_DATATYPE = 0x0E
REC_TEXTTYPE = 0x16
REC_ENDEL = 0x11

# GF180 analog frame/template geometry that is not enough by itself.
# Layer 46 is Metal4.  Datatype 10 is used by labels/pin text in the current
# Magic export.  Layer 0 contains the top-level boundary.
FRAME_ONLY_LAYERS = {
    (0, 0),
    (46, 0),
    (46, 10),
}

MIN_REAL_POLYGONS = 100


def _read_i2(data: bytes) -> int | None:
    if len(data) < 2:
        return None
    return struct.unpack(">h", data[:2])[0]


def summarize_gds(path: Path) -> tuple[Counter[str], Counter[tuple[int | None, int | None]]]:
    data = path.read_bytes()
    offset = 0
    current_record: int | None = None
    current_layer: int | None = None
    current_type: int | None = None

    elements: Counter[str] = Counter()
    geometry: Counter[tuple[int | None, int | None]] = Counter()

    while offset + 4 <= len(data):
        length, record_type, _data_type = struct.unpack(">HBB", data[offset : offset + 4])
        if length < 4 or offset + length > len(data):
            raise RuntimeError(f"Invalid GDS record at byte offset {offset}")

        payload = data[offset + 4 : offset + length]

        if record_type == REC_BOUNDARY:
            current_record = record_type
            current_layer = None
            current_type = None
            elements["BOUNDARY"] += 1
        elif record_type == REC_PATH:
            current_record = record_type
            current_layer = None
            current_type = None
            elements["PATH"] += 1
        elif record_type == REC_SREF:
            current_record = record_type
            elements["SREF"] += 1
        elif record_type == REC_AREF:
            current_record = record_type
            elements["AREF"] += 1
        elif record_type == REC_TEXT:
            current_record = record_type
            current_layer = None
            current_type = None
            elements["TEXT"] += 1
        elif record_type == REC_LAYER:
            current_layer = _read_i2(payload)
        elif record_type in (REC_DATATYPE, REC_TEXTTYPE):
            current_type = _read_i2(payload)
        elif record_type == REC_ENDEL:
            if current_record in (REC_BOUNDARY, REC_PATH):
                geometry[(current_layer, current_type)] += 1
            current_record = None
            current_layer = None
            current_type = None

        offset += length

    if offset != len(data):
        raise RuntimeError("Trailing partial GDS record")

    return elements, geometry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gds", type=Path, help="GDS file to inspect")
    parser.add_argument(
        "--min-real-polygons",
        type=int,
        default=MIN_REAL_POLYGONS,
        help=f"minimum non-frame polygon/path count, default {MIN_REAL_POLYGONS}",
    )
    args = parser.parse_args()

    if not args.gds.is_file():
        raise FileNotFoundError(args.gds)

    elements, geometry = summarize_gds(args.gds)
    total_geometry = sum(geometry.values())
    real_geometry = sum(
        count for layer_type, count in geometry.items() if layer_type not in FRAME_ONLY_LAYERS
    )

    print(f"GDS content check: {args.gds}")
    print(f"  file size: {args.gds.stat().st_size} bytes")
    print(f"  elements: {dict(elements)}")
    print(f"  geometry total: {total_geometry}")
    print(f"  non-frame geometry: {real_geometry}")
    print("  top geometry layers:")
    for (layer, datatype), count in geometry.most_common(20):
        print(f"    layer={layer} datatype={datatype}: {count}")

    if real_geometry < args.min_real_polygons:
        print()
        print("ERROR: GDS looks like only the analog frame/pins, not the final design.")
        print("The current file has too little non-frame geometry.  Regenerate the")
        print("hardened layout and copy the final GDS/LEF into gds/ and lef/.")
        return 1

    print("OK: GDS contains real non-frame layout geometry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Strip disabled analog pin labels from hardened GF180 GDS output.

The TT harden and custom-GDS checks require the top-level Verilog and LEF to
keep the full ua[7:0] interface. For this project, info.yaml declares only six
paid analog pins, so ua[6] and ua[7] must not be advertised as connected analog
pins in the submitted GDS.

Keep the GDS routing/metal and LEF PIN blocks intact for DRC and TT pin checks.
Remove only the disabled ua[6]/ua[7] GDS text labels after hardening.
"""
from __future__ import annotations

import argparse
from pathlib import Path

try:
    import gdstk
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing Python package gdstk. Install with: python3 -m pip install gdstk"
    ) from exc


def strip_gds_labels(gds_path: Path, pin_names: list[str]) -> None:
    lib = gdstk.read_gds(str(gds_path))
    pin_set = set(pin_names)
    removed_labels = 0

    for cell in lib.cells:
        labels_to_remove = [label for label in cell.labels if str(label.text) in pin_set]
        if labels_to_remove:
            cell.remove(*labels_to_remove)
            removed_labels += len(labels_to_remove)

    lib.write_gds(str(gds_path))

    print(f"Stripped disabled analog pin labels from {gds_path}")
    print(f"  removed GDS labels: {removed_labels}")

    verify = gdstk.read_gds(str(gds_path))
    remaining_labels = []
    for cell in verify.cells:
        for label in cell.labels:
            if str(label.text) in pin_set:
                remaining_labels.append(str(label.text))

    if remaining_labels:
        raise RuntimeError(f"Disabled analog pin labels remain in GDS: {remaining_labels}")


def check_lef_pins(lef_path: Path, pin_names: list[str]) -> None:
    text = lef_path.read_text(encoding="utf-8")
    missing = [pin for pin in pin_names if f"PIN {pin}" not in text]
    if missing:
        raise RuntimeError(
            "Required LEF PIN blocks are missing: " + ", ".join(missing)
        )

    print(f"Kept required TT LEF PIN blocks in {lef_path}")
    for pin in pin_names:
        print(f"  kept LEF PIN {pin}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gds", required=True, type=Path)
    parser.add_argument("--lef", required=True, type=Path)
    parser.add_argument("--pins", nargs="+", default=["ua[6]", "ua[7]"])
    args = parser.parse_args()

    strip_gds_labels(args.gds, args.pins)
    check_lef_pins(args.lef, args.pins)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

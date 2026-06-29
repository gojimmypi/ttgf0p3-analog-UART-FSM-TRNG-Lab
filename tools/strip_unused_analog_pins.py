#!/usr/bin/env python3
"""Strip unused analog pad pins from hardened GF180 GDS/LEF outputs.

The TT harden interface requires the top-level ua bus to be 8 bits wide, but
this GF180 analog shuttle metadata allows only six analog pins. Harden with the
normal ua[7:0] interface, then remove physical pad metal/labels for ua[6] and
ua[7] from the submitted custom-GDS artifact.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

try:
    import gdstk
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing Python package gdstk. Install with: python3 -m pip install gdstk"
    ) from exc


@dataclass(frozen=True)
class Window:
    name: str
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    def intersects(self, bbox: tuple[tuple[float, float], tuple[float, float]]) -> bool:
        (xmin, ymin), (xmax, ymax) = bbox
        return not (
            xmax < self.xmin
            or xmin > self.xmax
            or ymax < self.ymin
            or ymin > self.ymax
        )

    def contains_point(self, x: float, y: float) -> bool:
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax


# These are the bottom-edge analog pin windows in microns for the GF180 1x2
# template. They intentionally cover only the pad metal area near y=0.
DEFAULT_WINDOWS = [
    Window("ua[6]", 62.0, -0.5, 68.5, 2.5),
    Window("ua[7]", 18.0, -0.5, 25.0, 2.5),
]


def bbox_of(item: object) -> tuple[tuple[float, float], tuple[float, float]] | None:
    if hasattr(item, "bounding_box"):
        bbox = item.bounding_box()
        if bbox is not None:
            return bbox
    return None


def strip_gds(gds_path: Path, windows: list[Window]) -> None:
    lib = gdstk.read_gds(str(gds_path))
    top_cells = lib.top_level()
    if not top_cells:
        raise RuntimeError(f"No top-level cells found in {gds_path}")

    removed_polygons = 0
    removed_paths = 0
    removed_labels = 0

    for cell in top_cells:
        to_remove = []

        for polygon in cell.polygons:
            bbox = bbox_of(polygon)
            if bbox is not None and any(window.intersects(bbox) for window in windows):
                to_remove.append(polygon)
                removed_polygons += 1

        for path in cell.paths:
            bbox = bbox_of(path)
            if bbox is not None and any(window.intersects(bbox) for window in windows):
                to_remove.append(path)
                removed_paths += 1

        for label in cell.labels:
            label_text = str(label.text)
            origin = getattr(label, "origin", None)
            in_window = False
            if origin is not None:
                in_window = any(
                    window.contains_point(float(origin[0]), float(origin[1]))
                    for window in windows
                )
            if label_text in {window.name for window in windows} or in_window:
                to_remove.append(label)
                removed_labels += 1

        if to_remove:
            cell.remove(*to_remove)

    lib.write_gds(str(gds_path))

    print(f"Stripped unused analog pins from {gds_path}")
    print(f"  removed top-level polygons: {removed_polygons}")
    print(f"  removed top-level paths:    {removed_paths}")
    print(f"  removed top-level labels:   {removed_labels}")

    # Verify no explicit labels remain.
    verify = gdstk.read_gds(str(gds_path))
    remaining_labels = []
    for cell in verify.top_level():
        for label in cell.labels:
            if str(label.text) in {window.name for window in windows}:
                remaining_labels.append(str(label.text))
    if remaining_labels:
        raise RuntimeError(f"Unused analog pin labels remain in GDS: {remaining_labels}")

    remaining_items = []
    for cell in verify.top_level():
        for item in [*cell.polygons, *cell.paths]:
            bbox = bbox_of(item)
            if bbox is not None and any(window.intersects(bbox) for window in windows):
                remaining_items.append(type(item).__name__)
    if remaining_items:
        raise RuntimeError(
            "Unused analog pin geometry remains in GDS windows: "
            + ", ".join(remaining_items)
        )


def strip_lef(lef_path: Path, pin_names: list[str]) -> None:
    text = lef_path.read_text(encoding="utf-8")
    original = text

    for pin in pin_names:
        escaped = re.escape(pin)
        pattern = re.compile(
            rf"^[ \t]*PIN[ \t]+{escaped}[ \t]*\n.*?^[ \t]*END[ \t]+{escaped}[ \t]*\n",
            re.MULTILINE | re.DOTALL,
        )
        text, count = pattern.subn("", text, count=1)
        if count != 1:
            raise RuntimeError(f"Did not remove exactly one LEF PIN block for {pin}")

    for pin in pin_names:
        if pin in text:
            raise RuntimeError(f"Unused analog pin name remains in LEF: {pin}")

    if text == original:
        raise RuntimeError(f"LEF was not changed: {lef_path}")

    lef_path.write_text(text, encoding="utf-8", newline="\n")
    print(f"Stripped unused analog pins from {lef_path}")
    for pin in pin_names:
        print(f"  removed LEF PIN {pin}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gds", required=True, type=Path)
    parser.add_argument("--lef", required=True, type=Path)
    parser.add_argument("--pins", nargs="+", default=["ua[6]", "ua[7]"])
    args = parser.parse_args()

    strip_gds(args.gds, DEFAULT_WINDOWS)
    strip_lef(args.lef, args.pins)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

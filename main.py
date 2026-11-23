#!/usr/bin/env python3
"""u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6 entrypoint.

Meme Sprint 3: AI Agent Goes Rogue. Writes one 1024x1024 PNG meme to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR).

The image is drawn by draw.py (Pillow, run locally at build time) and
shipped beside this file as entry.png; this program copies it so both
grader runs write byte-identical output. Python 3.13, standard library
only, deterministic, no network access.

Usage:
    python3 main.py
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
MAX_BYTES = 1_048_576  # gate: at most 1 MiB


def _check_png(path: Path) -> None:
    """Fail loudly instead of submitting an invalid or oversized image."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, must be 1024x1024")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB gate")


def main() -> None:
    _check_png(SRC)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out_dir / "entry.png")


if __name__ == "__main__":
    main()

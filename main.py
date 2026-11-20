"""news-image-20261120 v3: copy the verified bundled entry image.

The image was rendered offline and verified; this program just copies
it to MAKEFUN_OUTPUT_DIR/entry.png and verifies the copy byte-for-byte.
Stdlib only — no image library, no network, no randomness, no clock.
"""
import os
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parent / "entry.png"


def main():
    if not SRC.is_file():
        raise SystemExit("bundled entry.png missing next to main.py")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(SRC, dst)
    if dst.read_bytes() != SRC.read_bytes():
        raise SystemExit("entry.png copy mismatch")
    print("wrote", dst)


if __name__ == "__main__":
    main()

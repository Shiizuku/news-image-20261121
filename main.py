#!/usr/bin/env python3
"""news-image-20261121 entry: copy the pre-rendered broadsheet to /output.

The image (entry.png, 1024x823) sums up the world news of Saturday
21 November 2026: COP31 overtime in Antalya, the Kryvyi Rih strike,
the capture of 'El Chapo Isidro', the AI stock sell-off, the Peru
quake, and BepiColombo reaching Mercury. It was drawn at build time
with Pillow (see draw_image.py); this program only copies the bytes,
so both graded runs write exactly the same file.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print("missing entry.png next to main.py", file=sys.stderr)
        raise SystemExit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    # The two graded runs must write identical bytes; confirm the copy.
    if sha256(SRC) != sha256(dst):
        print("copy mismatch", file=sys.stderr)
        raise SystemExit(1)
    print("wrote", dst, sha256(dst)[:16])


if __name__ == "__main__":
    main()

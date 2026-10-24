"""Extend an image to a Flow aspect ratio without scaling its source pixels."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path


RATIOS = {"9:16": (9, 16), "16:9": (16, 9)}


def run(command: list[str], *, binary: bool = False) -> bytes | str:
    """Run a media command and return stdout.

    Args:
        command: Executable and arguments.
        binary: Return bytes when true, otherwise decoded text.

    Returns:
        Captured stdout.
    """
    result = subprocess.run(command, check=True, capture_output=True)
    return result.stdout if binary else result.stdout.decode("utf-8")


def dimensions(path: Path) -> tuple[int, int]:
    """Read image dimensions with ffprobe."""
    raw = run([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height", "-of", "json", str(path),
    ])
    stream = json.loads(raw)["streams"][0]
    return stream["width"], stream["height"]


def corner_color(path: Path, width: int, height: int) -> str:
    """Estimate a neutral fill color by averaging the four corner pixels."""
    pixels = []
    for x, y in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)):
        value = run([
            "ffmpeg", "-v", "error", "-i", str(path), "-vf",
            f"crop=1:1:{x}:{y},format=rgb24", "-frames:v", "1",
            "-f", "rawvideo", "pipe:1",
        ], binary=True)
        pixels.append(value[:3])
    rgb = tuple(round(sum(pixel[index] for pixel in pixels) / len(pixels)) for index in range(3))
    return "0x" + "".join(f"{channel:02x}" for channel in rgb)


def main() -> int:
    """Prepare an aspect-matched PNG for a Google Flow frame slot."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--aspect-ratio", choices=RATIOS, required=True)
    parser.add_argument("--color", help="Optional ffmpeg color such as 0x808080")
    args = parser.parse_args()

    width, height = dimensions(args.input)
    ratio_width, ratio_height = RATIOS[args.aspect_ratio]
    scale = math.ceil(max(width / ratio_width, height / ratio_height))
    target_width, target_height = ratio_width * scale, ratio_height * scale
    fill = args.color or corner_color(args.input, width, height)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(args.input), "-vf",
        f"pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:color={fill}",
        "-frames:v", "1", str(args.output),
    ], check=True)
    print(f"Prepared {args.output.resolve()} ({target_width}x{target_height}, {args.aspect_ratio}, fill {fill})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

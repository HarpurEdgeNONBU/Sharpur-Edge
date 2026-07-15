"""Generate a simple trash-can PNG icon (no emoji, no network)."""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "assets" / "icons" / "trash.png"


def main() -> None:
    size = 48
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    color = (200, 60, 60, 255)
    # lid
    d.rectangle([12, 12, 36, 16], fill=color)
    d.rectangle([20, 8, 28, 12], fill=color)
    # can body
    d.rectangle([14, 16, 34, 40], outline=color, width=3)
    # vertical stripes
    for x in (20, 24, 28):
        d.line([(x, 20), (x, 36)], fill=color, width=2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

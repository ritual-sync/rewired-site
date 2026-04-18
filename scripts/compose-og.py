#!/usr/bin/env python3
"""
Compose the Rewired Open Graph image (1200×630) via Pillow.

Produces static/images/og/rewired-og.jpg — the image referenced by the OG
+ Twitter Card meta tags in layouts/_default/baseof.html and served to
link-preview scrapers at /images/og/rewired-og.jpg.

Why Pillow instead of rsvg-convert:
  - rsvg-convert ≥ 2.60 blocks external file:// references for security,
    silently dropping embedded <image xlink:href="file://..."> elements
    without warning. Pillow reads JPGs directly with no such restriction.
  - rsvg-convert uses system fonts (fontconfig); Cinzel + Space Grotesk
    are only available as woff2 web fonts in the arcaeon theme. This
    script converts the theme's woff2 files to TTF at runtime via
    fontTools so Pillow can render with the site's exact typefaces.

Composition:
  - Trinity row at top: Matt portrait | R mark | Jaye Anne portrait
    (three 280×280 squares, 40px gaps, centered).
  - Wordmark "Rewired" centered below in Fusion Gold Cinzel.
  - Tagline centered below the wordmark in Solar White Space Grotesk.

Run:
  python3 scripts/compose-og.py

Regenerate whenever the R mark, portraits, or tagline change. Remember to
force a re-scrape on social surfaces (Facebook Debugger, Twitter/X Card
Validator, Slack, iMessage) since link-preview caches are aggressive.
"""
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from pathlib import Path
import tempfile

SITE = Path(__file__).resolve().parent.parent
W, H = 1200, 630

# ARCÆON warm-core subset (D-11)
VOID_PURPLE = (26, 15, 46)     # #1a0f2e
FUSION_GOLD = (255, 179, 71)   # #ffb347
SOLAR_WHITE = (255, 244, 230)  # #fff4e6

# Source assets
MATT_PORTRAIT      = SITE / "static/images/portraits/matt.jpg"
MARK               = SITE / "static/images/logos/rewired-mark.jpg"
JAYE_ANNE_PORTRAIT = SITE / "static/images/portraits/jaye-anne.jpg"

# Web fonts (woff2) — converted to TTF at runtime for Pillow
CINZEL_WOFF2        = SITE / "themes/arcaeon/static/fonts/cinzel-latin-wght-normal.woff2"
SPACE_GROTESK_WOFF2 = SITE / "themes/arcaeon/static/fonts/space-grotesk-latin-wght-normal.woff2"

# Output
OUT = SITE / "static/images/og/rewired-og.jpg"

# Tagline sourced from hugo.toml [params].tagline — keep in sync manually
TAGLINE = "We left the systems. We're finding what's alive."


def woff2_to_ttf(woff2_path: Path) -> Path:
    """Convert a woff2 web font to TTF in a temp file. Pillow reads TTF but not woff2 directly."""
    font = TTFont(str(woff2_path))
    font.flavor = None
    fd, tmp_path = tempfile.mkstemp(suffix=".ttf", prefix="rewired-og-font-")
    font.save(tmp_path)
    return Path(tmp_path)


def paste_square(canvas: Image.Image, src: Path, x: int, y: int, size: int) -> None:
    """Open a (nominally square) JPG, resize with high-quality filter, paste at (x, y)."""
    img = Image.open(src).convert("RGB").resize((size, size), Image.LANCZOS)
    canvas.paste(img, (x, y))


def main() -> int:
    canvas = Image.new("RGB", (W, H), VOID_PURPLE)

    size, gap = 280, 40
    left = (W - (3 * size + 2 * gap)) // 2  # centered: 140
    y_top = 60

    paste_square(canvas, MATT_PORTRAIT,      left,                    y_top, size)
    paste_square(canvas, MARK,               left + size + gap,       y_top, size)
    paste_square(canvas, JAYE_ANNE_PORTRAIT, left + 2 * (size + gap), y_top, size)

    # Load site's web fonts via on-the-fly woff2→TTF conversion
    cinzel_ttf        = woff2_to_ttf(CINZEL_WOFF2)
    space_grotesk_ttf = woff2_to_ttf(SPACE_GROTESK_WOFF2)

    draw = ImageDraw.Draw(canvas)

    # Wordmark — Cinzel 112pt, Fusion Gold, centered
    wordmark_font = ImageFont.truetype(str(cinzel_ttf), 112)
    wordmark = "Rewired"
    wbbox = wordmark_font.getbbox(wordmark)
    word_x = (W - (wbbox[2] - wbbox[0])) // 2
    word_y = 380
    draw.text((word_x, word_y), wordmark, font=wordmark_font, fill=FUSION_GOLD)

    # Tagline — Space Grotesk 28pt, Solar White, centered
    tagline_font = ImageFont.truetype(str(space_grotesk_ttf), 28)
    tbbox = tagline_font.getbbox(TAGLINE)
    tag_x = (W - (tbbox[2] - tbbox[0])) // 2
    tag_y = 540
    draw.text((tag_x, tag_y), TAGLINE, font=tagline_font, fill=SOLAR_WHITE)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT, format="JPEG", quality=85, optimize=True)
    print(f"wrote {OUT.relative_to(SITE)}  ({OUT.stat().st_size:,} bytes, {W}×{H})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

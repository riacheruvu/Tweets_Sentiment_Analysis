"""Regenerate the article PNGs. Requires Pillow; the Jev CLI does not."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).parent
BG = "#F4F1E8"
INK = "#172033"
MUTED = "#657085"
CARD = "#FFFFFF"
NAVY = "#19263D"
MINT = "#83DCC2"
BLUE = "#6D9EEB"
CORAL = "#F28F79"
GOLD = "#E9B95D"
PALE_BLUE = "#E8EFFB"
PALE_MINT = "#E5F5EF"
PALE_CORAL = "#FCEBE7"
PALE_GOLD = "#FBF2DD"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, size: int, color: str = INK, bold: bool = False) -> None:
    draw.text(xy, text, font=font(size, bold), fill=color)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, radius: int = 24) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def comparison() -> None:
    image = Image.new("RGB", (1600, 900), BG)
    draw = ImageDraw.Draw(image)
    label(draw, (88, 62), "A SENTIMENT PROJECT, REVISITED", 20, MUTED, True)
    label(draw, (88, 103), "Same question. Two ways to learn.", 46, INK, True)
    label(draw, (88, 166), "What opinions do people express about self-driving cars?", 25, MUTED)

    # 2019 panel
    rounded(draw, (80, 245, 770, 710), CARD)
    rounded(draw, (112, 275, 260, 325), PALE_BLUE, 18)
    label(draw, (137, 286), "2019", 25, INK, True)
    label(draw, (112, 356), "LEARN FROM LABELED EXAMPLES", 18, MUTED, True)
    labels = [("Tweet text", 112, PALE_BLUE), ("Word\nembeddings", 272, PALE_GOLD), ("CNN", 465, PALE_CORAL), ("6 labels", 605, PALE_MINT)]
    for name, x, fill in labels:
        box_w = 136 if name.startswith("Word") else 126
        rounded(draw, (x, 462, x + box_w, 544), fill, 16)
        for line_index, line in enumerate(name.split("\n")):
            line_w = draw.textbbox((0, 0), line, font=font(17, True))[2]
            label(draw, (x + (box_w - line_w) // 2, 480 + line_index * 22), line, 17, INK, True)
    for x1, x2 in [(238, 272), (412, 465), (591, 605)]:
        draw.line((x1, 503, x2 - 7, 503), fill=MUTED, width=3)
        draw.polygon([(x2 - 8, 497), (x2, 503), (x2 - 8, 509)], fill=MUTED)
    label(draw, (112, 600), "The model learns patterns from annotated tweets.", 21, INK)
    label(draw, (112, 638), "Representation and training are visible in the notebook.", 18, MUTED)

    # 2026 panel
    rounded(draw, (830, 245, 1520, 710), CARD)
    rounded(draw, (862, 275, 1010, 325), PALE_MINT, 18)
    label(draw, (886, 286), "2026", 25, INK, True)
    label(draw, (862, 356), "ASK FOR A TYPED DECISION", 18, MUTED, True)
    steps = [("Tweet\nstate", 862, PALE_BLUE, 126), ("Choice\nquestion", 1010, PALE_GOLD, 134), ("Jev", 1168, PALE_MINT, 110), ("Label +\nprobabilities", 1302, PALE_CORAL, 174)]
    for text, x, fill, width in steps:
        rounded(draw, (x, 462, x + width, 554), fill, 16)
        for i, line in enumerate(text.split("\n")):
            tw = draw.textbbox((0, 0), line, font=font(17, True))[2]
            label(draw, (x + (width - tw) // 2, 480 + i * 22), line, 17, INK, True)
    for x1, x2 in [(988, 1010), (1144, 1168), (1278, 1302)]:
        draw.line((x1, 508, x2 - 7, 508), fill=MUTED, width=3)
        draw.polygon([(x2 - 8, 502), (x2, 508), (x2 - 8, 514)], fill=MUTED)
    label(draw, (862, 600), "The app defines the choices; Jev returns probabilities.", 21, INK)
    label(draw, (862, 638), "Code validates the answer and decides what happens next.", 18, MUTED)

    rounded(draw, (80, 755, 1520, 830), NAVY, 18)
    label(draw, (116, 778), "Different assumptions. Compare both on the same human-reviewed examples.", 22, "#FFFFFF", True)
    image.save(OUT / "2019-vs-2026.png", optimize=True)


def result_chart() -> None:
    image = Image.new("RGB", (1600, 1050), BG)
    draw = ImageDraw.Draw(image)
    label(draw, (88, 58), "A LIVE MODEL RESPONSE", 20, MUTED, True)
    label(draw, (88, 100), "One mixed tweet. One typed answer.", 44, INK, True)
    rounded(draw, (80, 180, 1520, 305), CARD, 22)
    label(draw, (112, 208), '“I love the idea of a self-driving car, but I would not trust it on an icy road.”', 25, INK)
    label(draw, (112, 260), "Input", 16, MUTED, True)

    # selected result
    rounded(draw, (80, 340, 500, 484), NAVY, 22)
    label(draw, (112, 365), "SELECTED LABEL", 16, "#CFD8E6", True)
    label(draw, (112, 397), "positive", 38, MINT, True)
    label(draw, (343, 409), "68%", 25, "#FFFFFF", True)

    rounded(draw, (525, 340, 955, 484), CARD, 22)
    label(draw, (557, 365), "JEV CONFIDENCE", 16, MUTED, True)
    label(draw, (557, 397), "0.61", 38, INK, True)
    label(draw, (680, 410), "a separate output", 18, MUTED)

    rounded(draw, (980, 340, 1520, 484), PALE_GOLD, 22)
    label(draw, (1012, 365), "MODEL BUILD", 16, MUTED, True)
    label(draw, (1012, 400), "typesafe/jev-1.13-20260917", 23, INK, True)

    label(draw, (112, 535), "PROBABILITY FOR EACH CHOICE", 17, MUTED, True)
    rows = [
        ("Very positive", 0.00, MUTED),
        ("Positive", 0.68, BLUE),
        ("Neutral", 0.15, GOLD),
        ("Negative", 0.17, CORAL),
        ("Very negative", 0.00, MUTED),
        ("Not relevant", 0.00, MUTED),
    ]
    start_y = 581
    label_x, bar_x, bar_w = 112, 390, 840
    for i, (name, value, color) in enumerate(rows):
        y = start_y + i * 56
        label(draw, (label_x, y + 5), name, 19, INK, value > 0)
        draw.rounded_rectangle((bar_x, y + 7, bar_x + bar_w, y + 27), radius=10, fill="#E1E5EB")
        if value > 0:
            draw.rounded_rectangle((bar_x, y + 7, bar_x + max(4, int(bar_w * value)), y + 27), radius=10, fill=color)
        label(draw, (bar_x + bar_w + 24, y + 2), f"{value:.0%}", 19, INK, True)

    rounded(draw, (80, 940, 1520, 1010), PALE_BLUE, 18)
    label(draw, (112, 962), "0.68 is the probability for the chosen label. 0.61 is Jev's confidence. Neither is measured accuracy.", 19, INK, True)
    image.save(OUT / "mixed-tweet-result.png", optimize=True)


if __name__ == "__main__":
    comparison()
    result_chart()

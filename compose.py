#!/usr/bin/env python3
"""Compose the front page for news-image-20261121.

Draws one 1024x1024 newspaper front page summing up the world news of
Saturday 21 November 2026. Every word on the page is rendered here with
Pillow, so the finished image carries no garbled AI text. The four
editorial illustrations in assets/ contain no text of their own.

The layout, top to bottom: a masthead, a red date strip, a lead row
(Poland + COP31, each with a picture), a second row (Wall Street +
Cyclone Akvan, each with a picture), a text-only grid (Denmark, the
UK-EU deal, The Hague, the Gulf), and an ALSO TODAY column of short
briefs. 20 stories in all, across seven regions.

Deterministic: no network, no clock, no randomness. Running this
script twice produces the same entry.png byte for byte.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (248, 244, 235)
INK = (24, 24, 24)
RED = (176, 32, 32)
NAVY = (30, 56, 92)
GREY = (96, 92, 84)
RULE = (182, 174, 160)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def crop_to(img, tw, th):
    """Centre-crop to the target aspect ratio, then resize to it."""
    iw, ih = img.size
    want = tw / th
    have = iw / ih
    if have > want:
        nw = int(ih * want)
        x0 = (iw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / want)
        y0 = (ih - nh) // 2
        img = img.crop((0, y0, iw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def wrap_text(draw, text, fnt, width):
    """Greedy word wrap: lines that fit inside `width` pixels."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def block(draw, x, y, text, fnt, width, fill=INK, gap=4):
    """Draw a wrapped paragraph; return the y just below it."""
    for line in wrap_text(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=load(SANS_BOLD, 14), fill=RED)
    return y + 20


def story(draw, x, y, width, place, headline, deck, hsize=26, dsize=15):
    """A kicker, a headline and a deck; returns the y below the deck."""
    y = kicker(draw, x, y, place)
    y = block(draw, x, y, headline, load(SERIF, hsize), width, gap=2)
    y = block(draw, x, y + 3, deck, load(SANS, dsize), width, gap=3)
    return y


def picture(page, name, x, y, tw, th):
    img = Image.open(os.path.join(ASSETS, name)).convert("RGB")
    page.paste(crop_to(img, tw, th), (x, y))


def rule(draw, y):
    draw.line([(32, y), (992, y)], fill=RULE, width=2)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead -------------------------------------------------------
    d.text((32, 12), "THE WORLD IN ONE DAY",
           font=load(SERIF, 54), fill=INK)
    d.text((32, 74), "A front page of Saturday's world news",
           font=load(SERIF_REG, 19), fill=GREY)

    # ---- Date strip -----------------------------------------------------
    d.rectangle([0, 104, W, 138], fill=RED)
    d.text((32, 111), "SATURDAY  21  NOVEMBER  2026",
           font=load(SANS_BOLD, 23), fill=(255, 255, 255))
    d.text((688, 115), "21 STORIES  •  7 REGIONS",
           font=load(SANS_BOLD, 15), fill=(255, 236, 222))

    # ---- Row 1: Poland (lead) + COP31 ----------------------------------
    picture(page, "media-generation-poland-jets-0-fe82a787-2f23-4a65-9671-fe48d8cb18e7.webp",
            32, 146, 596, 140)
    picture(page, "media-generation-cop31-hall-0-b634eb88-976e-4208-a5b0-0f99edb32ebd.webp",
            656, 146, 336, 140)
    story(d, 32, 294, 596, "EASTERN POLAND",
          "Russian missiles land in Poland; NATO calls it a grave violation",
          "Two missiles and a suspected jet drone came down in the east "
          "during a huge strike on Ukraine. Warsaw calls it a likely "
          "deliberate provocation; NATO scrambled jets, and its chief, "
          "Mark Rutte, is due in Warsaw today. Nobody was hurt.",
          hsize=27, dsize=16)
    story(d, 656, 294, 336, "ANTALYA",
          "Climate talks run past deadline as fossil fuels vanish from draft",
          "The summit slipped into overtime with no fossil-fuel phase-out "
          "in the text. The EU warns of a fossil summit; a new draft is "
          "due today.",
          hsize=23, dsize=14)

    # ---- Row 2: Wall Street + Cyclone Akvan ----------------------------
    rule(d, 468)
    picture(page, "media-generation-wall-street-0-faa1608a-720c-4860-9499-e8c06e5a6a85.webp",
            32, 478, 472, 110)
    picture(page, "media-generation-cyclone-0-6385040a-8c65-471e-a6cb-64601716bec6.webp",
            520, 478, 472, 110)
    story(d, 32, 596, 472, "NEW YORK",
          "Wall Street slides into correction as AI shares plunge",
          "Stocks fell about 3.7% as the sell-off in AI and chip shares "
          "pushed the S&P 500 and the Dow into correction.",
          hsize=21, dsize=14)
    story(d, 520, 596, 472, "ODISHA, INDIA",
          "Cyclone Akvan strikes India's east coast",
          "The storm crossed near Gopalpur after about 300,000 people were "
          "evacuated; rescue teams moved in as it weakened.",
          hsize=21, dsize=14)

    # ---- Row 3: text-only grid, two stories per column -----------------
    rule(d, 706)
    yl = story(d, 32, 716, 472, "COPENHAGEN",
               "Denmark expels Russian envoy over 'assassination plot'",
               "Two men are charged over a plot to kill rapper Kyivstoner; "
               "Copenhagen blames Russian intelligence and Moscow denies it.",
               hsize=16, dsize=12)
    story(d, 32, yl + 8, 472, "THE HAGUE",
          "World court ruling spurs Myanmar action calls",
          "Rights groups press governments to act after the ICJ found "
          "Myanmar committed genocide.",
          hsize=16, dsize=12)
    yr = story(d, 520, 716, 472, "BRUSSELS",
               "Britain and EU seal reset deal on trade and youth",
               "Agrifood checks go, carbon markets link up, and 100,000 "
               "under-30s a year may live and work on either side.",
               hsize=16, dsize=12)
    story(d, 520, yr + 8, 472, "STRAIT OF HORMUZ",
          "Iran war drags on as missiles fly over Riyadh",
          "The war nears its ninth month; the Saudi-led coalition downs "
          "Houthi missiles and strikes Hodeidah.",
          hsize=16, dsize=12)

    # ---- Also today -----------------------------------------------------
    rule(d, 880)
    d.text((32, 888), "ALSO TODAY",
           font=load(SANS_BOLD, 14), fill=RED)
    d.text((520, 888), "ALSO TODAY  —  CONTINUED",
           font=load(SANS_BOLD, 14), fill=RED)

    left = [
        "Shenzhen summit of Trump, Xi and Putin ends with few results.",
        "Bolsonaro in hospital with severe abdominal pain.",
        "Pill hailed as breakthrough for pancreatic cancer.",
        "Wellington: India 159/1; Jaiswal-Rahul century stand.",
        "NSE becomes world's 5th-largest exchange, passing Nasdaq.",
        "Nepal PM Balendra Shah to visit India on 22-23 Nov.",
        "Indonesia fire losses could reach $30bn.",
    ]
    right = [
        "Malaysia to resettle 10,000 Rohingya in Turkiye.",
        "Pakistan checkpoint bombing kills five, injures 13.",
        "Nikhil Gupta jailed about 19 years over Pannun plot.",
        "JPMorgan, Visa, Mastercard hit by vendor cyberattack.",
        "Carlsen forfeits rapid games at chess tournament.",
        "Russian transport plane crash in Siberia kills 17.",
    ]
    brief_font = load(SANS, 11)
    y = 912
    for item in left:
        d.text((32, y), "\u2022  " + item, font=brief_font, fill=INK)
        y += 14
    y = 912
    for item in right:
        d.text((520, y), "\u2022  " + item, font=brief_font, fill=INK)
        y += 14

    page.save(os.path.join(HERE, "entry.png"), optimize=True)


if __name__ == "__main__":
    main()

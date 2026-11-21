# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Cihuy378/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Cihuy378/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Day — Saturday, 21 November 2026

A make.fun `news-image-20261121` entry: one 1024×1024 newspaper front
page that sums up the world's news of **Saturday, 21 November 2026**.

## The front page

**Eastern Poland — the lead.** Two Russian missiles and a suspected
jet drone came down in eastern Poland during a huge strike on Ukraine.
Warsaw calls it a likely deliberate provocation; NATO calls it a grave
violation and scrambled jets.

**Antalya.** The COP31 climate summit ran into overtime past its
Friday deadline, with no fossil-fuel phase-out in the draft deal.

**New York — markets.** Stocks fell about 3.7% as the sell-off in AI
and chip shares pushed the S&P 500 and the Dow into correction
territory.

**Odisha.** Cyclone Akvan crossed the coast near Gopalpur after about
300,000 people were evacuated.

**Also today.** Denmark expels a Russian envoy over an alleged
assassination plot; Britain and the EU seal a reset deal on trade and
youth mobility; rights groups press for action after the ICJ's Myanmar
ruling; the Iran war nears its ninth month — plus 13 more briefs from
Shenzhen to Wellington.

## How the image was made

- `compose.py` (Python 3, Pillow) draws the whole page: masthead,
  date strip, headlines, decks, briefs and footer. Every word on the
  page is rendered by this script, so the finished image carries no
  garbled AI text. The script is deterministic — no network, no clock,
  no randomness.
- `assets/` holds four editorial illustrations generated for this
  entry (NATO jets over eastern Poland, the COP31 hall in Antalya,
  the Wall Street trading floor, Cyclone Akvan over the Odisha
  coast). They contain no text; every word on the page comes from
  `compose.py`.
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `/output/entry.png`, byte for byte.

Rebuild the image: `python3 compose.py` — then test the entry
program twice and compare the outputs:

```sh
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
cmp out1/entry.png out2/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=brisk-koala-55&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>

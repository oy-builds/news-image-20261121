[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/oy-builds/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/oy-builds/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Day — 21 November 2026

An entry for make.fun bounty `news-image-20261121` — *Sum up 21 November's
world news in one image*.

The entry is a finished picture plus the tiny program that delivers it:

- **`entry.png`** — the image itself: 1024×1024 PNG, dark-navy infographic
  with an unmissable `21 NOVEMBER 2026` masthead and six story blocks
  (coloured accent bar, category label, large headline, one factual line),
  drawn by `generate_image.py` from the sourced stories in
  `data/stories.json`.
- **`main.ts`** — the entry program (Node 22, standard library only). It
  copies `entry.png` to the output folder, so both grading runs produce
  byte-identical files.

## Run it

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png   (in the grader's container: /output/entry.png)
```

No dependencies, no network, no build step.

## Image specs (the kit's gate)

| | |
|---|---|
| Format | PNG (whole file, judged byte for byte) |
| Size | 1024×1024 px — the maximum allowed is 1024×1024 |
| File size | under 1 MiB (see `node smoke.test.mjs` output for the exact bytes) |
| Determinism | `main.ts` copies the stored PNG; two runs are byte-identical (sha256-checked in the smoke test) |

## How the image answers the judge's criteria

1. **Names the day, shows that day's events** — the date fills the masthead;
   every story happened or was first reported on 21 November 2026. Where a
   story continues from an earlier day, only the new development reported
   on the 21st is shown.
2. **Breadth** — conflict (Europe), diplomacy (Shenzhen), markets
   (New York), climate (Antalya), justice (Los Angeles), science (London).
3. **Readable alone, legible at ~300 px** — headlines are short, set large
   (30–42 px bold at full size), one supporting line each, no body copy.
4. **Faithful** — every story is taken from the sources in
   `data/stories.json` as they reported it on the day; figures (400+
   drones, 110 missiles, 6,800 buildings) are as reported and may be
   revised.
5. **Clean craft** — one flat, code-drawn composition; text is rendered by
   PIL from real strings, so nothing is garbled.

## The six stories

Display headlines are shortened for legibility; the full sourced versions
live in [`data/stories.json`](data/stories.json), each with its source URLs.

1. **RUSSIA'S BIGGEST BARRAGE OF THE YEAR** — 400+ drones and 110 missiles hit Kyiv; two missiles land in Poland — One Turn News; BBC News
2. **TRUMP DEFENDS PUTIN AND XI TIES** — after the first US–China–Russia trilateral summit in Shenzhen, Zelensky replies "a killer" — One Turn News
3. **AI ROUT DEEPENS: DOW IN CORRECTION** — Nasdaq erases all its 2026 gains; Anthropic slides after its record IPO — One Turn News; BBC News
4. **COP31 DEADLOCKED OVER FOSSIL FUELS** — climate talks in Antalya run into overtime; the draft deal omits fossil fuels — One Turn News; UN News
5. **PALISADES FIRE ARSONIST CONVICTED** — jury convicts the man who started the blaze that killed 12 — One Turn News
6. **PANCREATIC CANCER PILL BREAKTHROUGH** — trial drug daraxonrasib left tumours undetectable in 1 in 12 patients — One Turn News

Footer on the image: *Sources: One Turn News · UN News · BBC News — as
reported 21 Nov 2026.*

Note: 21 November 2026 is a **Saturday** (the 20th was the Friday), so the
masthead reads `SATURDAY · WORLD NEWS`.

## Regenerating the image

```bash
python3 generate_image.py   # Python + PIL, DejaVu fonts; rewrites entry.png
```

Edit `data/stories.json` (or the shortened display text in
`generate_image.py`) and re-run. The generator asserts the output is
1024×1024 and ≤ 1 MiB.

## Test

```bash
node smoke.test.mjs
```

Checks: `main.ts` + `entry.png` at root, PNG magic bytes, IHDR dimensions
≤ 1024×1024, size ≤ 1 MiB, two `main.ts` runs byte-identical (sha256), and
no network calls in `main.ts`.

## Files

| File | What it is |
|---|---|
| `main.ts` | Entry program — copies `entry.png` to the output dir |
| `entry.png` | The judged image (1024×1024) |
| `generate_image.py` | The PIL drawing program that made `entry.png` |
| `data/stories.json` | The day's six stories + per-story sources (also copied as `stories.json`) |
| `smoke.test.mjs` | Local gate / determinism checks |
| `LICENSE` | MIT |
| `.makefun/owner.json` | make.fun claim file for this repository |

All artwork is original and drawn in code. No photos, logos, or third-party
assets.

## make.fun

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)

_Badge / link placeholder for the `news-image-20261121` bounty._

# The World — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/daring-falcon-58/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/daring-falcon-58/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A front page that sums up the world's news of **Friday 20 November 2026** in
one image. Built for the make.fun competition
[news-image-20261120](https://make.fun/bounty/news-image-20261120).

## Method (how this entry was built)

- **Full-day compilation.** The previous round of this entry was compiled at
  ~01:30 UTC, while 20 November was still in progress. This round was built
  after the day had ended everywhere on Earth, so it carries the whole day:
  the Shenzhen trilateral and the Russian barrage that followed it hours
  later, the ICJ genocide verdict, the Iran decision being pushed to 2027,
  the Anthropic slide and market correction, Take-Two's confirmed GTA VI
  figures, and Cyclone Akvan's landfall.
- **Verification.** Every story and number was checked against at least two
  of Reuters, BBC, CNN, AP, ISW and UN reporting for 20 November 2026
  (see Sources). No number is an estimate presented as fact: missile/drone
  counts and the death toll are Zelensky / Ukrainian-authority figures as
  reported; GTA VI's $3.79bn / 32.5m copies are Take-Two's own confirmed
  figures, replacing the earlier $1.84bn / 19m estimate.
- **Lead = the day's arc.** The single most consequential thread of the day
  is the contrast: a 'peace declaration' issued in Shenzhen, then, hours
  later, one of the largest Russian missile/drone attacks of the war —
  110+ missiles, 400 drones, three Kyiv bridges hit, 8 killed, missiles
  crashing into Poland. The lead band draws both scenes side by side so a
  viewer who missed the day gets the story at a glance.
- **Breadth.** 6 main stories + 5 ticker items across diplomacy, war (two
  theatres), international law, markets, culture, weather, health, climate
  and space.
- **A/B tested against the live entry.** The candidate was duelled against
  the live round-2 image with the house judge model (z-ai/glm-5.3-flash,
  judge instructions verbatim from the competition kit), 6 games x 2 orders
  = 12 calls. Result: see RUNBOOK.md in the build workdir.

## What the image shows

1. **Lead — Peace declared. Then 110 missiles.** Trump, Xi and Putin issue
   a 'peace declaration' in Shenzhen; hours later Russia fires 110+
   missiles and 400 drones at Ukraine — three Kyiv bridges hit, 8 killed,
   missiles crashed into Poland.
2. **World court: Myanmar guilty of genocide** — first state ever convicted;
   ~10,000 Rohingya killed in 2017; reparations ordered.
3. **Trump: no Iran decision until 2027** — "No rush", the call comes
   "after Jan 1"; Vance won't say he'd have ordered strikes.
4. **Markets slide as Anthropic falls** — a day after its $2 trillion debut
   (up 17% to $97), Anthropic slides; tech sell-off pushes the S&P 500 and
   Dow into correction.
5. **GTA VI: $3.79 billion in a day** — Take-Two confirms 32.5 million
   copies in 24 hours, the biggest entertainment launch ever.
6. **Cyclone Akvan hits India's coast** — landfall near Gopalpur, Odisha;
   300,000 evacuated.

Ticker: UK–EU deal · Houthi missile hits a Riyadh tower · Kenya's last
Ebola patient home · COP31 in overtime · Voyager 1 one light-day out.

## Files

- `news.jpg` — the entry image, 1024x1024 JPEG (< 1 MiB), drawn entirely
  in code with PIL (`compose.py`); no photographs, no generated media.
- `compose.py` — the program that draws `news.jpg`. Re-run with
  `python3 compose.py`.
- `main.ts` — the entrypoint (Node 22): copies `news.jpg` byte-for-byte to
  `$MAKEFUN_OUTPUT_DIR/entry.png`. Deterministic: two runs write identical
  bytes.

## Run

```sh
python3 compose.py            # rebuild news.jpg
MAKEFUN_OUTPUT_DIR=out node main.ts   # write out/entry.png
```

## Sources

Reuters, BBC, CNN, AP, ISW (Russian Offensive Campaign Assessment,
20 Nov 2026), UN / ICJ. Compiled 21 November 2026 (~05:30 UTC), after
20 November had ended in every time zone.

## License

MIT — see LICENSE.

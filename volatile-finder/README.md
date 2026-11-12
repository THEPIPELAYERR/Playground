# Volatile Stock Finder

Finds the stocks that are swinging the most right now, for a plan of putting
**$1 a day** into a volatile stock. It can also backtest that plan.

> Not financial advice. Volatile means it can drop as fast as it rises.
> At $1/day your most you can put in is about $250 per trading year, so set
> it up with money you're fine losing.

## Setup

```bash
pip install -r requirements.txt
```

Price data comes free from Yahoo Finance through `yfinance`, so you don't need an API key.

## Find volatile stocks

```bash
python volfinder.py                       # whole US market: ~1,700 stocks, about 3 minutes
python volfinder.py --quick               # only the built-in list of ~100 volatile names (fast)
python volfinder.py --top 50 --min-cap 1000   # top 50, only companies worth $1B+
python volfinder.py --tickers TSLA,GME,MARA,IONQ
python volfinder.py --html report.html --csv report.csv
```

By default it pulls every US-listed stock worth over $300M that trades at least
1M shares a day (from Yahoo's screener), then ranks them by how hard they've
swung over the **last 3 and 6 months**.

Example output:

```
  # TICKER     PRICE  VOL 3M  VOL 6M 6M RANGE  BIG DAY AVG MOVE 5%+ DAYS   RETURN   $VOL/d  SCORE  RISK
  1 BRUN        5.93    135%    138%     740%     +27%     6.7%       65     -77%      47M   99.5  EXTREME
...
Today's pick: BRUN (6-month range 740%, moves ~6.7% a day, risk EXTREME)
```

| Column | Meaning |
|---|---|
| VOL 3M / VOL 6M | Annualised volatility over the last 3 and 6 months: how wildly the price jumps around |
| 6M RANGE | How far the 6-month high is above the 6-month low (740% = the high was 8.4x the low) |
| BIG DAY | Largest single-day move in the last 6 months |
| AVG MOVE | Average size of one day's move, up or down |
| 5%+ DAYS | Days with a move of 5% or more |
| RETURN | Gain or loss over the window (`--days`, default 126 = 6 months) |
| $VOL/d | Dollars traded per day (bigger means easier to buy and sell) |
| SCORE | 0–100 blend: 30% vol 3M, 30% vol 6M, 20% 6M range, 10% ATR, 10% big days |

What the scan leaves out by default:
- stocks under **$2** (penny stocks): change with `--min-price`
- anything trading under **$20M/day**: change with `--min-dollar-vol`
- leveraged/inverse ETFs (TQQQ, SOXL, UVXY…), because they lose value over
  time by design and suit day trades better than daily buying. Add them back with `--include-leveraged`

## Backtest the $1/day plan

```bash
python volfinder.py sim MARA --days 250   # $1 every trading day into MARA for ~1 year
python volfinder.py sim                   # same, using today's #1 pick
python volfinder.py sim --rotate          # each day buy whatever was most volatile the day before
python volfinder.py sim TSLA --amount 5   # $5/day instead
```

The tool buys fractional shares at each day's close. Your broker must support
fractional shares to do this for real (Robinhood, Fidelity, Schwab, Cash App,
Webull and others do).

**Note:** the backtest only looks at the past, so the stocks it ranks are ones
that were volatile and still listed today. Stocks that crashed and were delisted
are missing, so real results can come out worse.

## Tests

```bash
python -m pytest -q    # runs offline with fake price data
```

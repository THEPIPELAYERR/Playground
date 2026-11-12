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
python volfinder.py                       # scan ~110 known high-volatility tickers
python volfinder.py --top 10 --days 30    # top 10 over the last 30 trading days
python volfinder.py --tickers TSLA,GME,MARA,IONQ
python volfinder.py --html report.html --csv report.csv
```

Example output:

```
  # TICKER     PRICE  VOL/yr AVG MOVE   ATR% 5%+ DAYS   RETURN  MAX DD   $VOL/d  SCORE  RISK
  1 WILD       98.34    111%     5.7%   8.9%       44    +144%    -33%     118M  100.0  VERY HIGH
...
Today's pick: WILD (moves ~5.7% a day, risk VERY HIGH)
```

| Column | Meaning |
|---|---|
| VOL/yr | Annualised volatility: how much the price swings in a typical year |
| AVG MOVE | Average size of one day's move, up or down |
| ATR% | Average daily high-to-low range over the last 14 days, as % of price |
| 5%+ DAYS | Days in the window with a move of 5% or more |
| RETURN / MAX DD | Gain or loss over the window, and the worst fall from a high |
| $VOL/d | Dollars traded per day (bigger means easier to buy and sell) |
| SCORE | 0–100 blend of the above (45% vol, 25% ATR, 20% avg move, 10% big days) |

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

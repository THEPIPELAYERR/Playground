#!/usr/bin/env python3
"""Volatile Stock Finder.

Scans a list of tickers, measures how much each one swings, and ranks them so
you can pick a volatile stock for a $1-a-day buying plan. It can also backtest
that plan: "what if I had put $1 a day into X over the last N days?"

Usage examples:
    python volfinder.py                     # scan the whole US market (3- and 6-month swings)
    python volfinder.py --quick             # only the built-in list of ~100 volatile names
    python volfinder.py --top 10 --days 60  # shorter window, top 10
    python volfinder.py --tickers TSLA,GME,MARA
    python volfinder.py sim MARA --days 365 # backtest $1/day into MARA
    python volfinder.py sim --rotate        # each day buy that day's most volatile pick
    python volfinder.py --csv out.csv --html report.html
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass, asdict

import pandas as pd

from universe import DEFAULT_UNIVERSE, LEVERAGED_ETFS

TRADING_DAYS = 252


# ---------------------------------------------------------------- data

def discover(min_cap_m: float, min_volume: float, min_price: float) -> list[str]:
    """Every US-listed stock above a size/liquidity floor, from Yahoo's screener."""
    import yfinance as yf
    from yfinance import EquityQuery as Q

    query = Q("and", [
        Q("eq", ["region", "us"]),
        Q("is-in", ["exchange", "NMS", "NYQ", "ASE", "NGM", "NCM"]),
        Q("gt", ["intradaymarketcap", min_cap_m * 1e6]),
        Q("gt", ["avgdailyvol3m", min_volume]),
        Q("gt", ["intradayprice", min_price]),
    ])
    found, offset = [], 0
    while True:
        res = yf.screen(query, offset=offset, size=250,
                        sortField="intradaymarketcap", sortAsc=False)
        quotes = res.get("quotes", [])
        found += [q["symbol"] for q in quotes if q.get("quoteType", "EQUITY") == "EQUITY"]
        offset += len(quotes)
        if not quotes or offset >= res.get("total", 0):
            break
    return found


def download(tickers: list[str], days: int, chunk: int = 150) -> dict[str, pd.DataFrame]:
    """Daily OHLCV for each ticker, covering at least `days` trading days."""
    import yfinance as yf

    # Ask for extra calendar days so we get enough trading days plus warm-up.
    period_days = int(days * 1.6) + 40
    out = {}
    for i in range(0, len(tickers), chunk):
        batch = tickers[i:i + chunk]
        if len(tickers) > chunk:
            print(f"  {min(i + chunk, len(tickers))}/{len(tickers)}", file=sys.stderr)
        raw = yf.download(
            batch, period=f"{period_days}d", interval="1d",
            auto_adjust=True, group_by="ticker", progress=False, threads=True,
        )
        for t in batch:
            try:
                df = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
            except KeyError:
                continue
            df = df.dropna(subset=["Close"])
            if len(df) >= 30:
                out[t] = df
    return out


# ---------------------------------------------------------------- metrics

@dataclass
class Stats:
    ticker: str
    price: float
    vol_3m: float          # annualised volatility over the last 63 trading days, %
    vol_6m: float          # annualised volatility over the last 126 trading days, %
    range_6m: float        # 6-month high vs 6-month low, % (how far it swung end to end)
    biggest_day: float     # largest single-day move in the last 6 months, % (signed)
    vol_annual: float      # annualised volatility over the --days window, %
    avg_move: float        # average absolute daily move, %
    atr_pct: float         # 14-day average true range as % of price
    big_days: int          # days with a move of 5% or more
    max_drawdown: float    # worst peak-to-trough fall, %
    ret: float             # total return over the window, %
    dollar_vol_m: float    # average daily traded value, $ millions
    score: float = 0.0

    @property
    def risk(self) -> str:
        v = max(self.vol_3m, self.vol_6m)
        if v >= 120: return "EXTREME"
        if v >= 80:  return "VERY HIGH"
        if v >= 50:  return "HIGH"
        return "MODERATE"


def ann_vol(close: pd.Series) -> float:
    logr = (close / close.shift()).apply(math.log).dropna()
    return float(logr.std() * math.sqrt(TRADING_DAYS) * 100)


def compute_stats(ticker: str, df: pd.DataFrame, days: int) -> Stats | None:
    full = df
    df = df.tail(days + 1)
    if len(df) < 20:
        return None
    six = full.tail(127)
    six_rets = six["Close"].pct_change().dropna()
    big = six_rets.loc[six_rets.abs().idxmax()] if len(six_rets) else 0.0
    close, high, low, vol = df["Close"], df["High"], df["Low"], df["Volume"]
    rets = close.pct_change().dropna()
    logr = (close / close.shift()).apply(math.log).dropna()

    prev = close.shift()
    tr = pd.concat([high - low, (high - prev).abs(), (low - prev).abs()], axis=1).max(axis=1)
    atr = tr.tail(14).mean()

    running_peak = close.cummax()
    mdd = ((close / running_peak) - 1).min()

    return Stats(
        ticker=ticker,
        price=float(close.iloc[-1]),
        vol_3m=ann_vol(full["Close"].tail(64)),
        vol_6m=ann_vol(six["Close"]),
        range_6m=float((six["High"].max() / six["Low"].min() - 1) * 100),
        biggest_day=float(big * 100),
        vol_annual=float(logr.std() * math.sqrt(TRADING_DAYS) * 100),
        avg_move=float(rets.abs().mean() * 100),
        atr_pct=float(atr / close.iloc[-1] * 100),
        big_days=int((rets.abs() >= 0.05).sum()),
        max_drawdown=float(mdd * 100),
        ret=float((close.iloc[-1] / close.iloc[0] - 1) * 100),
        dollar_vol_m=float((close * vol).mean() / 1e6),
    )


def rank(stats: list[Stats]) -> list[Stats]:
    """Blend of volatility measures, each turned into a 0-1 percentile."""
    if not stats:
        return []
    df = pd.DataFrame([asdict(s) for s in stats])
    score = (
        0.30 * df["vol_3m"].rank(pct=True)
        + 0.30 * df["vol_6m"].rank(pct=True)
        + 0.20 * df["range_6m"].rank(pct=True)
        + 0.10 * df["atr_pct"].rank(pct=True)
        + 0.10 * df["big_days"].rank(pct=True)
    )
    for s, sc in zip(stats, score):
        s.score = round(float(sc) * 100, 1)
    return sorted(stats, key=lambda s: s.score, reverse=True)


def scan(data: dict[str, pd.DataFrame], days: int, min_price: float,
         min_dollar_vol_m: float) -> tuple[list[Stats], list[str]]:
    kept, dropped = [], []
    for t, df in data.items():
        s = compute_stats(t, df, days)
        if s is None:
            dropped.append(f"{t} (not enough history)")
        elif s.price < min_price:
            dropped.append(f"{t} (price ${s.price:.2f} < ${min_price:g})")
        elif s.dollar_vol_m < min_dollar_vol_m:
            dropped.append(f"{t} (volume ${s.dollar_vol_m:.1f}M/day too thin)")
        else:
            kept.append(s)
    return rank(kept), dropped


# ---------------------------------------------------------------- $1/day backtest

@dataclass
class SimResult:
    label: str
    days: int
    invested: float
    value: float
    shares: dict[str, float]

    @property
    def pnl(self) -> float: return self.value - self.invested
    @property
    def pnl_pct(self) -> float: return self.pnl / self.invested * 100 if self.invested else 0.0


def simulate_fixed(ticker: str, df: pd.DataFrame, days: int, amount: float = 1.0) -> SimResult:
    """Buy `amount` dollars of one ticker at every daily close (fractional shares)."""
    close = df["Close"].tail(days)
    shares = float((amount / close).sum())
    return SimResult(ticker, len(close), amount * len(close), shares * float(close.iloc[-1]),
                     {ticker: shares})


def simulate_rotate(data: dict[str, pd.DataFrame], days: int, lookback: int,
                    amount: float = 1.0) -> SimResult:
    """Each day, buy `amount` of whichever ticker was most volatile over the
    previous `lookback` days, using only data available on that day."""
    closes = pd.DataFrame({t: d["Close"] for t, d in data.items()}).sort_index()
    logr = (closes / closes.shift()).apply(lambda c: c.map(math.log))
    rolling_vol = logr.rolling(lookback, min_periods=lookback).std()
    dates = closes.index[-days:]
    shares: dict[str, float] = {}
    n = 0
    for d in dates:
        # volatility known at the previous close -> no look-ahead
        i = closes.index.get_loc(d)
        if i == 0:
            continue
        v = rolling_vol.iloc[i - 1].dropna()
        price_today = closes.loc[d]
        v = v[price_today[v.index].notna()]
        if v.empty:
            continue
        pick = v.idxmax()
        shares[pick] = shares.get(pick, 0.0) + amount / float(price_today[pick])
        n += 1
    last = closes.ffill().iloc[-1]
    value = sum(sh * float(last[t]) for t, sh in shares.items())
    return SimResult(f"rotate (most volatile, {lookback}d lookback)", n, amount * n, value, shares)


# ---------------------------------------------------------------- output

def fmt_table(stats: list[Stats], top: int) -> str:
    head = (f"{'#':>3} {'TICKER':<6} {'PRICE':>9} {'VOL 3M':>7} {'VOL 6M':>7} {'6M RANGE':>8} "
            f"{'BIG DAY':>8} {'AVG MOVE':>8} {'5%+ DAYS':>8} {'RETURN':>8} {'$VOL/d':>8} {'SCORE':>6}  RISK")
    lines = [head, "-" * len(head)]
    for i, s in enumerate(stats[:top], 1):
        lines.append(
            f"{i:>3} {s.ticker:<6} {s.price:>9.2f} {s.vol_3m:>6.0f}% {s.vol_6m:>6.0f}% "
            f"{s.range_6m:>7.0f}% {s.biggest_day:>+7.0f}% {s.avg_move:>7.1f}% {s.big_days:>8} "
            f"{s.ret:>+7.0f}% {s.dollar_vol_m:>7.0f}M {s.score:>6.1f}  {s.risk}")
    return "\n".join(lines)


def fmt_sim(r: SimResult) -> str:
    lines = [f"\n$1/day plan: {r.label}",
             f"  Days bought : {r.days}",
             f"  Put in      : ${r.invested:,.2f}",
             f"  Worth now   : ${r.value:,.2f}",
             f"  Profit/loss : {'+' if r.pnl >= 0 else '-'}${abs(r.pnl):,.2f} ({r.pnl_pct:+.1f}%)"]
    if len(r.shares) > 1:
        lines.append("  Holdings    : " + ", ".join(
            f"{t} {sh:.4f}" for t, sh in sorted(r.shares.items(), key=lambda kv: -kv[1])[:8]))
    return "\n".join(lines)


def write_html(path: str, stats: list[Stats], top: int, days: int) -> None:
    rows = "".join(
        f"<tr><td>{i}</td><td><b>{s.ticker}</b></td><td>${s.price:,.2f}</td>"
        f"<td>{s.vol_3m:.0f}%</td><td>{s.vol_6m:.0f}%</td><td>{s.range_6m:.0f}%</td>"
        f"<td class={'up' if s.biggest_day >= 0 else 'dn'}>{s.biggest_day:+.0f}%</td>"
        f"<td>{s.avg_move:.1f}%</td><td>{s.big_days}</td>"
        f"<td class={'up' if s.ret >= 0 else 'dn'}>{s.ret:+.0f}%</td>"
        f"<td class=dn>{s.max_drawdown:.0f}%</td><td>${s.dollar_vol_m:,.0f}M</td>"
        f"<td>{s.score:.1f}</td><td class='r {s.risk.split()[-1].lower()}'>{s.risk}</td></tr>"
        for i, s in enumerate(stats[:top], 1))
    stamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
    html = f"""<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Volatile Stock Finder</title>
<style>body{{margin:0;background:#111;color:#eee;font:14px/1.5 system-ui,sans-serif;padding:24px 16px}}
h1{{margin:0}}p{{color:#999}}.wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;min-width:900px}}
th,td{{padding:8px 10px;text-align:right;border-bottom:1px solid #2a2a2a}}th{{color:#aaa;font-weight:600}}
td:nth-child(2),th:nth-child(2){{text-align:left}}.up{{color:#5fd38d}}.dn{{color:#ff7a7a}}
.r{{font-weight:700}}.extreme{{color:#ff5a5a}}.high{{color:#ffb347}}.moderate{{color:#9ad}}</style></head>
<body><h1>Volatile Stock Finder</h1><p>Ranked by 3- and 6-month swings · window {days} trading days · generated {stamp}. Not financial advice.</p>
<div class=wrap><table><tr><th>#</th><th>Ticker</th><th>Price</th><th>Vol 3M</th><th>Vol 6M</th>
<th>6M range</th><th>Biggest day</th><th>Avg move</th><th>5%+ days</th><th>Return</th><th>Max DD</th><th>$Vol/day</th><th>Score</th><th>Risk</th></tr>
{rows}</table></div></body></html>"""
    with open(path, "w") as f:
        f.write(html)


# ---------------------------------------------------------------- CLI

def load_tickers(args) -> list[str]:
    if args.tickers:
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    elif args.file:
        with open(args.file) as f:
            tickers = [t.strip().upper() for t in f.read().replace(",", " ").split() if t.strip()]
    else:
        tickers = list(DEFAULT_UNIVERSE)
        if not args.quick:
            print("Finding every US stock above the size/volume floor...", file=sys.stderr)
            try:
                found = discover(args.min_cap, 1_000_000, args.min_price)
                tickers = list(dict.fromkeys(tickers + found))
                print(f"  {len(found)} found", file=sys.stderr)
            except Exception as e:  # screener down: fall back to the built-in list
                print(f"  market screener failed ({e}); using the built-in list", file=sys.stderr)
        if not args.include_leveraged:
            tickers = [t for t in tickers if t not in LEVERAGED_ETFS]
    return tickers


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Find volatile stocks for a $1/day plan.")
    p.add_argument("mode", nargs="?", default="scan", choices=["scan", "sim"],
                   help="scan = rank tickers (default); sim = backtest $1/day")
    p.add_argument("sim_ticker", nargs="?", help="ticker to backtest (sim mode); default = today's #1")
    p.add_argument("--tickers", help="comma-separated tickers to scan instead of the default list")
    p.add_argument("--file", help="text file of tickers (space, comma or newline separated)")
    p.add_argument("--quick", action="store_true",
                   help="skip the market-wide search; scan only the built-in list")
    p.add_argument("--min-cap", type=float, default=300,
                   help="market-wide search: smallest market cap in $M (default 300)")
    p.add_argument("--days", type=int, default=126,
                   help="window for return/avg move/drawdown, in trading days (default 126 = 6 months)")
    p.add_argument("--top", type=int, default=20, help="how many to show (default 20)")
    p.add_argument("--min-price", type=float, default=2.0, help="skip stocks under this price (default $2)")
    p.add_argument("--min-dollar-vol", type=float, default=20.0,
                   help="skip stocks trading less than this many $M per day (default 20)")
    p.add_argument("--include-leveraged", action="store_true", help="include leveraged/inverse ETFs")
    p.add_argument("--rotate", action="store_true", help="sim: buy each day's most volatile pick")
    p.add_argument("--lookback", type=int, default=20, help="sim --rotate: volatility lookback (default 20)")
    p.add_argument("--amount", type=float, default=1.0, help="sim: dollars per day (default 1)")
    p.add_argument("--csv", help="also save the ranking to this CSV file")
    p.add_argument("--html", help="also save the ranking to this HTML file")
    args = p.parse_args(argv)

    tickers = load_tickers(args)
    if args.mode == "sim" and args.sim_ticker and args.sim_ticker.upper() not in tickers:
        tickers.append(args.sim_ticker.upper())

    print(f"Downloading {len(tickers)} tickers...", file=sys.stderr)
    data = download(tickers, max(args.days, 126) + args.lookback)
    if not data:
        print("No data came back. Check your internet connection or the ticker symbols.", file=sys.stderr)
        return 1

    if args.mode == "scan":
        ranked, dropped = scan(data, args.days, args.min_price, args.min_dollar_vol)
        print(f"\nBiggest swings over the last 3-6 months "
              f"({len(ranked)} of {len(data)} stocks passed filters):\n")
        print(fmt_table(ranked, args.top))
        if dropped:
            print(f"\nSkipped {len(dropped)}: " + ", ".join(dropped[:15])
                  + (" ..." if len(dropped) > 15 else ""))
        if ranked:
            top1 = ranked[0]
            print(f"\nToday's pick: {top1.ticker} (6-month range {top1.range_6m:.0f}%, "
                  f"moves ~{top1.avg_move:.1f}% a day, risk {top1.risk})")
        if args.csv:
            pd.DataFrame([asdict(s) | {"risk": s.risk} for s in ranked]).to_csv(args.csv, index=False)
            print(f"Saved {args.csv}")
        if args.html:
            write_html(args.html, ranked, args.top, args.days)
            print(f"Saved {args.html}")
        return 0

    # sim
    if args.rotate:
        ranked, _ = scan(data, args.days, args.min_price, args.min_dollar_vol)
        pool = {s.ticker: data[s.ticker] for s in ranked}
        if not pool:
            print("Nothing passed the filters.", file=sys.stderr)
            return 1
        print(fmt_sim(simulate_rotate(pool, args.days, args.lookback, args.amount)))
        return 0

    t = (args.sim_ticker or "").upper()
    if not t:
        ranked, _ = scan(data, args.days, args.min_price, args.min_dollar_vol)
        if not ranked:
            print("Nothing passed the filters.", file=sys.stderr)
            return 1
        t = ranked[0].ticker
    if t not in data:
        print(f"No data for {t}.", file=sys.stderr)
        return 1
    print(fmt_sim(simulate_fixed(t, data[t], args.days, args.amount)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

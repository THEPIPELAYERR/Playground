"""Offline tests: fake price data, no internet needed.  Run: python -m pytest -q"""
import numpy as np
import pandas as pd

import volfinder


def fake(seed, vol, price=50.0, n=200, volume=2_000_000):
    rng = np.random.default_rng(seed)
    close = price * np.exp(np.cumsum(rng.normal(0, vol, n)))
    idx = pd.bdate_range(end="2026-11-11", periods=n)
    return pd.DataFrame({"Open": close, "High": close * (1 + vol / 2), "Low": close * (1 - vol / 2),
                         "Close": close, "Volume": volume}, index=idx)


DATA = {"CALM": fake(1, 0.005), "MID": fake(2, 0.02), "WILD": fake(3, 0.07),
        "PENNY": fake(4, 0.08, price=0.5), "THIN": fake(5, 0.09, volume=1000)}


def test_ranks_most_volatile_first_and_filters():
    ranked, dropped = volfinder.scan(DATA, 90, min_price=2, min_dollar_vol_m=20)
    assert [s.ticker for s in ranked] == ["WILD", "MID", "CALM"]
    assert any("PENNY" in d for d in dropped) and any("THIN" in d for d in dropped)
    assert ranked[0].vol_annual > 80 and ranked[-1].vol_annual < 15
    assert ranked[0].vol_6m > ranked[1].vol_6m and ranked[0].range_6m > 100


def test_fixed_sim_math():
    df = DATA["MID"]
    r = volfinder.simulate_fixed("MID", df, 30)
    assert r.invested == 30
    close = df["Close"].tail(30)
    assert abs(r.value - (1 / close).sum() * close.iloc[-1]) < 1e-9


def test_rotate_sim_runs_and_buys_volatile():
    r = volfinder.simulate_rotate({k: DATA[k] for k in ("CALM", "MID", "WILD")}, 60, 20)
    assert r.days == 60 and r.invested == 60
    assert max(r.shares, key=lambda t: r.shares[t] * DATA[t]["Close"].iloc[-1]) == "WILD"


def test_cli_end_to_end(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(volfinder, "download", lambda t, d: DATA)
    monkeypatch.setattr(volfinder, "discover", lambda *a: ["WILD"])
    assert volfinder.main(["--html", str(tmp_path / "r.html"), "--csv", str(tmp_path / "r.csv")]) == 0
    out = capsys.readouterr().out
    assert "Today's pick: WILD" in out
    assert (tmp_path / "r.html").exists() and (tmp_path / "r.csv").exists()
    assert volfinder.main(["sim", "MID", "--days", "60"]) == 0
    assert volfinder.main(["sim", "--rotate", "--days", "60"]) == 0
    print(capsys.readouterr().out)

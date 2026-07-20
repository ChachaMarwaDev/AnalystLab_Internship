# AAPL Stock Exploration — Summary Report

**Data source:** Yahoo Finance (`yfinance`) | **Period:** Jan 2020 – Jul 2026 | **Frequency:** Daily OHLCV

---

## 1. Pipeline Overview

| Stage | What was done |
|---|---|
| **Loading** | Pulled daily OHLCV data for AAPL via `yfinance`; flattened the MultiIndex columns yfinance returns by default. |
| **Exploration** | Checked shape, dtypes, summary stats, and null counts. |
| **Cleaning** | Sorted by date, cast index to `datetime`, dropped any residual empty rows. |
| **Feature engineering** | Derived daily and rolling-window features (below). |
| **Time series analysis** | Computed moving averages, monthly returns, and annualized rolling volatility. |
| **Visualization** | Five charts covering price trend, volume, volatility bands, monthly returns, and return distribution. |

## 2. Features Created

- **Daily Change** = Close − Open
- **Daily Pct Change** = (Close − Open) / Open × 100
- **Daily Range** = High − Low
- **Log Return** = ln(Close / previous Close)
- **MA_7, MA_20, MA_30** — rolling moving averages (short, medium, longer-term trend)
- **BB_std, BB_upper, BB_lower** — 20-day Bollinger-style volatility bands (MA_20 ± 2 std)
- **Volatility_30d** — 30-day rolling std of log returns, annualized (×√252)
- **Monthly summary table** — month-end close, average daily % change, average daily range, and month-over-month return

## 3. Trends Identified

- **Long-term trend:** AAPL climbed from roughly $75 (early 2020) to a peak near $315 by mid-2026, with the 30-day MA confirming a sustained uptrend interrupted by clear pullback periods (mid-2022, early-2025).
- **Volume:** Trading volume was highest and most volatile in 2020 (COVID-era spikes above 400M shares/day) and has trended steadily lower since, settling into a calmer range with only occasional spikes (e.g., a ~320M spike around late 2024, another near mid-2026).
- **Volatility bands:** The Bollinger channel narrows during steady uptrends (e.g., 2023) and widens sharply around drawdowns (e.g., early 2025), which is the expected signature of rising short-term volatility during price corrections.
- **Monthly returns:** Returns are mostly in the ±10% range, with a few outsized months (+15–22%) early in the series (2020) reflecting higher post-pandemic volatility, and generally smaller swings in later years.
- **Daily returns distribution:** Roughly bell-shaped and centered near 0%, but with fat tails — a handful of days beyond ±5%, consistent with typical equity return behavior (leptokurtic, not normal).

## 4. Key Insights

1. AAPL's growth has not been linear — multi-month corrections (2022, early 2025) interrupt an otherwise strong uptrend, so trend-following signals need to account for meaningful pullback risk.
2. Elevated trading volume tends to coincide with price volatility (2020, occasional 2024–2026 spikes), suggesting volume spikes can serve as an early flag for volatility regime changes.
3. The 30-day volatility measure confirms risk is not constant over time — it clusters around known drawdown periods, supporting a case for volatility-aware position sizing rather than a fixed-risk approach.
4. The return distribution's fat tails mean extreme single-day moves are more common than a normal distribution would predict — risk models assuming normality would understate tail risk.

## 5. Data-Driven Recommendations

- **For trend analysis:** Use the 30-day MA as the primary trend filter and treat sustained breaks below it (as seen in 2022 and early 2025) as early correction signals.
- **For risk management:** Incorporate the 30-day rolling volatility measure into position sizing — reduce exposure when volatility is rising, not just when price is falling.
- **For entry/exit timing:** Bollinger band width can flag regime shifts — a rapid widening often precedes or accompanies larger price swings, useful as a volatility-based (not directional) signal.
- **For volume-based signals:** Treat volume spikes above ~2x the trailing average as a trigger to re-check volatility and news context before acting on a price move.
- **Next steps:** Extend the analysis with a benchmark comparison (e.g., AAPL vs. S&P 500) to separate stock-specific moves from broad market trends, and backtest the MA/volatility signals above before using them for actual trade decisions.

---
*Generated from `exploration.ipynb` — AnalystLab Internship portfolio project.*
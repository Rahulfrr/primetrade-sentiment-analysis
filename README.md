# Bitcoin Market Sentiment vs Trader Performance

Analysis of the relationship between Fear/Greed market sentiment and trader performance,
using Hyperliquid historical trade data (~211k trades, May 2023–May 2025) merged with the
daily Fear/Greed Index.

## Method

1. Parsed trade timestamps to daily dates, joined against the Fear/Greed Index on date.
2. Collapsed the 5-level classification (Extreme Fear, Fear, Neutral, Greed, Extreme Greed)
   into 3 buckets (Fear, Neutral, Greed) for cleaner comparison.
3. Compared performance across all trade rows, and separately on only "closed" trades
   (non-zero Closed PnL, i.e. realized outcomes).
4. Checked position sizing behavior and per-account consistency across regimes.

## Findings

| Metric | Fear | Greed | Neutral |
|---|---|---|---|
| Win rate (all trades) | 40.8% | 42.0% | 39.7% |
| Win rate (closed trades) | 84.4% | 82.5% | 82.4% |
| Avg PnL per closed trade | $101.86 | $105.70 | $71.20 |
| Median trade size (USD) | $749 | $552 | $548 |

**1. Traders size up during Fear, not Greed.**
Median trade size is ~35% larger during Fear periods. This runs counter to the common
assumption that Greed drives reckless position sizing. It more likely reflects
conviction-buying or averaging-down behavior during dips.

**2. Win rate is nearly flat across regimes.**
Sentiment does not meaningfully change whether a trade wins. The differences (39.7%–42.0%)
are within noise. Sentiment affects sizing and behavior, not trade selection quality.

**3. Greed shows a small edge in average PnL per closed trade**, but the gap versus Fear
is modest (~4%) and should not be read as a strong effect.

**4. 67.7% of traders active in both regimes perform better during Greed.**
Most traders do better going with the crowd than against it, in this dataset.

## Important caveat

The trade data only covers May 2023–May 2025, largely a bull market. "Greed periods perform
better" may simply reflect that Greed days coincided with uptrend days in this specific
window, not a universal relationship between sentiment and edge. This dataset alone cannot
separate sentiment-driven behavior from broader market-regime effects — a longer window
spanning a bear market would be needed to test that.

## Files

- `analysis.py` — full analysis code

Raw data files are excluded from this repo (trader data is ~46MB, too large to
commit sensibly). Source datasets:
- Fear/Greed Index: provided sentiment dataset
- Hyperliquid historical trade data: provided trader dataset

To reproduce: place `fear_greed_index.csv` and `trader_data.csv` in the repo root,
then run the script below.

## How to run

```bash
pip install pandas
python analysis.py
```

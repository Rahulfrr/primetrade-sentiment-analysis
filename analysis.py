"""
Bitcoin Market Sentiment vs Trader Performance Analysis
Datasets: Fear/Greed Index (Alternative.me) + Hyperliquid historical trade data
"""

import pandas as pd

# ---- Load ----
trader = pd.read_csv('trader_data.csv')
sentiment = pd.read_csv('fear_greed_index.csv')

# ---- Clean & parse ----
trader['date'] = pd.to_datetime(trader['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce').dt.date
sentiment['date'] = pd.to_datetime(sentiment['date']).dt.date
trader['Closed PnL'] = pd.to_numeric(trader['Closed PnL'], errors='coerce')
trader['Size USD'] = pd.to_numeric(trader['Size USD'], errors='coerce')

# ---- Merge ----
df = trader.merge(sentiment[['date', 'classification', 'value']], on='date', how='left')
df = df.dropna(subset=['classification'])

def simplify(c):
    if 'Fear' in str(c):
        return 'Fear'
    if 'Greed' in str(c):
        return 'Greed'
    return 'Neutral'

df['sentiment_simple'] = df['classification'].apply(simplify)

# ---- Analysis 1: performance by sentiment (all trade rows) ----
perf_all = df.groupby('sentiment_simple').agg(
    trades=('Closed PnL', 'count'),
    avg_pnl=('Closed PnL', 'mean'),
    win_rate=('Closed PnL', lambda x: (x > 0).mean()),
    avg_size_usd=('Size USD', 'mean')
)

# ---- Analysis 2: performance on closed (realized) trades only ----
closed = df[df['Closed PnL'] != 0]
perf_closed = closed.groupby('sentiment_simple').agg(
    trades=('Closed PnL', 'count'),
    avg_pnl=('Closed PnL', 'mean'),
    median_pnl=('Closed PnL', 'median'),
    win_rate=('Closed PnL', lambda x: (x > 0).mean())
)

# ---- Analysis 3: position sizing by sentiment ----
size_by_sentiment = df.groupby('sentiment_simple')['Size USD'].median()

# ---- Analysis 4: per-trader consistency (Fear vs Greed) ----
acct_sent = closed.groupby(['Account', 'sentiment_simple'])['Closed PnL'].mean().unstack()
acct_sent = acct_sent.dropna(subset=['Fear', 'Greed'])
better_in_fear = (acct_sent['Fear'] > acct_sent['Greed']).sum()
better_in_greed = len(acct_sent) - better_in_fear

if __name__ == '__main__':
    print("=== Performance by sentiment (all trades) ===")
    print(perf_all, "\n")

    print("=== Performance on closed trades only ===")
    print(perf_closed, "\n")

    print("=== Median trade size (USD) by sentiment ===")
    print(size_by_sentiment, "\n")

    print(f"Accounts active in both Fear & Greed: {len(acct_sent)}")
    print(f"  Better in Fear:  {better_in_fear} ({better_in_fear/len(acct_sent)*100:.1f}%)")
    print(f"  Better in Greed: {better_in_greed} ({better_in_greed/len(acct_sent)*100:.1f}%)")

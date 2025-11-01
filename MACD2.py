import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

plt.style.use("dark_background")

# --- Global styling tweaks ---
plt.rcParams.update({
    "axes.facecolor": "#000000",
    "figure.facecolor": "#000000",
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "#333333",
    "legend.facecolor": "#111111",
    "legend.edgecolor": "#222222",
    "font.size": 10
})

# MACD settings
short_window = 12
long_window = 26
signal_window = 9

# Load data
df = pd.read_csv('data.csv')
df['date'] = pd.to_datetime(df['date'])

# Calculate EMAs and MACD
df['EMA12'] = df['close'].ewm(span=short_window, adjust=False).mean()
df['EMA26'] = df['close'].ewm(span=long_window, adjust=False).mean()
df['MACD'] = df['EMA12'] - df['EMA26']
df['Signal'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
df['hist_difference'] = df['MACD'] - df['Signal']
df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()
df["trendDirection"] = np.where(df["close"] > df["EMA200"], "up", "down")

# ---- Buy Signal ----
df['Buy_Signal'] = 0
for i in range(1, len(df)):
    if (
        df['hist_difference'].iloc[i-1] < 0 and df['hist_difference'].iloc[i] > 0 and
        df['MACD'].iloc[i] < 0 and df['Signal'].iloc[i] < 0 and
        df['trendDirection'].iloc[i] == "up"
    ):
        df.loc[df.index[i], 'Buy_Signal'] = 1

# ---- Portfolio Simulation with trade tracking ----
initial_cash = 1000
cash = initial_cash
in_trade = False
entry_price = 0
entry_date = None
trades = []
portfolio_values = []

# ---- Adjustable Risk Management ----
stop_loss_pct = 0.02      # Sell if price drops 2%
profit_ratio = 1.5        # 1.5x profit vs loss
take_profit_pct = stop_loss_pct * profit_ratio  # e.g. 3% take-profit if stop_loss_pct=2%

for i in range(len(df)):
    price = df['close'].iloc[i]
    date = df['date'].iloc[i]

    if not in_trade:
        if df['Buy_Signal'].iloc[i] == 1:
            entry_price = price
            stop_price = entry_price * (1 - stop_loss_pct)
            target_price = entry_price * (1 + take_profit_pct)
            entry_date = date
            in_trade = True
            print(f"BUY at {entry_price:.2f} on {date.date()} | Target: {target_price:.2f}, Stop: {stop_price:.2f}")
    else:
        if price >= target_price:
            cash = cash * (target_price / entry_price)
            print(f"SELL (TP HIT) at {target_price:.2f} on {date.date()} | Portfolio: {cash:.2f}")
            trades.append((entry_date, date, entry_price, target_price, 'win'))
            in_trade = False
        elif price <= stop_price:
            cash = cash * (stop_price / entry_price)
            print(f"SELL (STOP HIT) at {stop_price:.2f} on {date.date()} | Portfolio: {cash:.2f}")
            trades.append((entry_date, date, entry_price, stop_price, 'loss'))
            in_trade = False

    portfolio_values.append(cash)

df['Portfolio'] = portfolio_values

# ---- Main Plots ----
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True,
                                    gridspec_kw={'height_ratios': [2, 1, 1]},
                                    figsize=(16, 9))   # YouTube ratio

# --- Top plot: Closing Price + EMA200 ---
ax1.plot(df["date"], df["close"], color="#00BFFF", linewidth=1.5, label="Close Price")
ax1.plot(df["date"], df["EMA200"], color="#FF5555", linestyle="--", linewidth=1.2, label="EMA 200")

# Mark buy points
buy_points = df[df['Buy_Signal'] == 1]
ax1.scatter(buy_points["date"], buy_points["close"], color="#00FF88", marker="^", s=100, label="Buy Signal", zorder=5)

# Draw trade overlays: stop (red), target (green)
for trade in trades:
    start_date, end_date, entry, exit_price, result = trade
    color = "#00FF88" if result == "win" else "#FF5555"
    ax1.hlines(y=exit_price, xmin=start_date, xmax=end_date, colors=color, linestyles="--", linewidth=1.8)

ax1.legend(loc="upper left", fontsize=10)
ax1.set_ylabel("Price ($)")
ax1.grid(True, linestyle="--", alpha=0.3)

# --- Middle plot: MACD + Signal ---
ax2.plot(df["date"], df["MACD"], color="#1E90FF", linewidth=1.2, label="MACD")
ax2.plot(df["date"], df["Signal"], color="#FFB347", linewidth=1.2, label="Signal")
ax2.axhline(0, color="#888888", linestyle="--", linewidth=1)

for i in buy_points.index:
    ax2.annotate('↑', 
                 (df['date'].iloc[i], df['MACD'].iloc[i]), 
                 color='#00FF88', fontsize=12, ha='center')

ax2.legend(loc="upper left", fontsize=9)
ax2.set_ylabel("MACD")
ax2.grid(True, linestyle="--", alpha=0.3)

# --- Bottom plot: Histogram ---
colors = ["#00FF88" if h >= 0 else "#FF5555" for h in df["hist_difference"]]
ax3.bar(df["date"], df["hist_difference"], color=colors, width=1)
ax3.axhline(0, color="#666666", linestyle="--", linewidth=1)
ax3.set_ylabel("Histogram")
ax3.set_xlabel("Date")
ax3.grid(True, linestyle="--", alpha=0.3)

# --- Format x-axis ---
ax3.xaxis.set_major_locator(mdates.YearLocator())
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
fig.autofmt_xdate()

plt.tight_layout()
plt.show()


# ---- Portfolio Value Over Time (YouTube 16:9 layout) ----
plt.figure(figsize=(16, 9))
plt.plot(df["date"], df["Portfolio"], color="#9370DB", linewidth=2.5, label="Portfolio Value")
plt.title("Portfolio Value Over Time", color="white", fontsize=16)
plt.xlabel("Date", color="white")
plt.ylabel("Portfolio Value ($)", color="white")
plt.grid(True, linestyle="--", alpha=0.3)
plt.legend(facecolor="#111111", edgecolor="#222222", fontsize=10, loc="upper left")

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gcf().autofmt_xdate()

plt.tight_layout()
# Optional: Save in full HD resolution
# plt.savefig('portfolio_plot.png', dpi=200, bbox_inches='tight')
plt.show()

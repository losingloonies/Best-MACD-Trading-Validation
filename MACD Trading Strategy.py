import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("dark_background")

# MACD Settings
short_window = 12
long_window = 26
signal_window = 9

#Loading the stock data
df = pd.read_csv('data.csv')
df["date"] = pd.to_datetime(df["date"])

#calculating EMAs and MACDs
df["EMA12"] = df["close"].ewm(span = short_window, adjust=False).mean()
df["EMA26"] = df["close"].ewm(span = long_window, adjust=False).mean()
df["MACD"] = df["EMA12"] - df["EMA26"]
df["Signal"] = df["MACD"].ewm(span=signal_window, adjust=False).mean()
df["hist_difference"] = df["MACD"]-df["Signal"]

#Create buy signal
df["Buy_Signal"] = 0
for i in range(1, len(df)):
    if(
        df["hist_difference"].iloc[i-1] < 0 and df["hist_difference"].iloc[i] > 0 and
        df["MACD"].iloc[i] < 0 and df["Signal"].iloc[i] < 0
    ):
        df.loc[df.index[i], "Buy_Signal"] = 1

buy_points = df[df["Buy_Signal"] == 1]

#Plotting Figures
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(16, 9))

#Top Plot
ax1.plot(df["date"], df["close"], label="Close")
ax1.scatter(buy_points["date"], buy_points["close"], color="#00FF88", marker="^", s=50, label="Buy Signal", zorder=5)
ax1.legend()

#Middle Plot
ax2.plot(df["date"], df["MACD"], color="#00BFFF", label="MACD")
ax2.plot(df["date"], df["Signal"], color="#FF5555", label="Signal")
ax2.scatter(buy_points["date"], buy_points["MACD"], color="#00FF88", marker="^", s=50, label="Buy Signal", zorder=5)
ax2.axhline(0)
ax2.legend()

#Bottom plot


plt.show()
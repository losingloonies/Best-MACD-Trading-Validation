import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#MACD - number of days for moving average
MACD_moving_avg = 12
Signal_moving_avg = 26

df=pd.read_csv('data.csv')

#Use the closing value to calculate a moving average
df["MACD"] = df["close"].rolling(window=MACD_moving_avg).mean()
df["Signal"] = df["close"].rolling(window=Signal_moving_avg).mean()
df["hist_difference"] = df["MACD"]-df["Signal"]

print(df.tail())


fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]}, figsize=(12, 8))

# Top plot: price and MACD lines
ax1.plot(df["timestamp"], df["close"], color="black", label="Close")
ax1.plot(df["timestamp"], df["MACD"], color="blue", label="MACD")
ax1.plot(df["timestamp"], df["Signal"], color="orange", label="Signal")
ax1.legend(loc="upper left")
ax1.set_ylabel("Price / MACD")

# Bottom plot: histogram with advanced coloring
colors = []
hist = df["hist_difference"].values
for i in range(len(hist)):
    if hist[i] >= 0:
        # Check if next bar is higher and positive
        if i < len(hist) - 1 and hist[i+1] > hist[i] and hist[i+1] > 0:
            colors.append("darkgreen")
        else:
            colors.append("green")
    else:
        # Check if next bar is lower (more negative) and negative
        if i < len(hist) - 1 and hist[i+1] < hist[i] and hist[i+1] < 0:
            colors.append("darkred")
        else:
            colors.append("red")

ax2.bar(df["timestamp"], df["hist_difference"], color=colors, width=1)
ax2.set_ylabel("MACD Histogram")
ax2.set_xlabel("Timestamp")

plt.tight_layout()
plt.show()
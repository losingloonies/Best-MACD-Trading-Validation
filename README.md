#  Validating the "Best MACD Trading Strategy"

This project tests and validates the **MACD (Moving Average Convergence Divergence)** trading strategy discussed in a YouTube video.  
The script simulates trades, applies risk management, and visualizes performance across multiple time-series plots.

 **Watch my breakdown video here:**  
[▶LosingLoonies YouTube Channel](https://www.youtube.com/@LosingLoonies)

 **Original video I tested this strategy from:**  
[Best MACD Strategy Video (External Source)](https://www.youtube.com/watch?v=rf_EQvubKlk&t=6s)

---

## Overview

This Python script:
- Loads historical stock data (`data.csv`)
- Computes **MACD**, **Signal Line**, and **Histogram**
- Identifies **buy signals** based on MACD crossovers and EMA200 trend filtering
- Simulates portfolio growth with **adjustable stop-loss** and **take-profit ratios**
- Visualizes:
  - Price with EMA200 and trade markers
  - MACD + Signal overlays
  - Histogram bars
  - Portfolio value growth over time

---

## Strategy Logic

**Buy Entry Conditions**
- MACD histogram crosses from negative → positive  
- Both MACD and Signal are below 0 (momentum shift from bearish to bullish)  
- Closing price is **above EMA200** (confirming uptrend)

**Risk Management**
- **Stop Loss:** 2% (default)
- **Take Profit:** 1.5× stop loss (3% in this config)
- Each trade is executed sequentially (no compounding positions)

---

##isual Outputs

The script produces the following plots in a YouTube-friendly **16:9 layout**:
1. **Price Chart:** Close price, EMA200, and buy markers  
2. **MACD Plot:** MACD, Signal, and crossover arrows  
3. **Histogram Plot:** Green (positive) vs red (negative) bars  
4. **Portfolio Value:** Growth curve based on executed trades

---

## Requirements

Install the dependencies before running:

```bash
pip install numpy pandas matplotlib

# ============================================
# BASIC MARKET ANALYSIS (BEGINNER FRIENDLY)
# Random Walk + AR(1) + Regression + Beta
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------
# 1. LOAD DATA
# --------------------------------------------

file_path = "/Users/gurtejsingh/Desktop/Code/NIFTY 50-25-11-2024-to-25-11-2025.csv"   # <-- change if needed
data = pd.read_csv(file_path)

# clean column names
data.columns = data.columns.str.strip()

# convert date
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

prices = data['Close']

# --------------------------------------------
# 2. RETURNS
# --------------------------------------------

returns = prices.pct_change().dropna()

# --------------------------------------------
# 3. RANDOM WALK (DRUNK MAN MODEL)
# --------------------------------------------

mean_return = returns.mean()
std_return = returns.std()

print("\n--- RANDOM WALK CHECK ---")
print("Average daily return:", mean_return)

# simulate drunk man walk
np.random.seed(42)
random_steps = np.random.choice([-1, 1], size=len(prices))
drunk_walk = random_steps.cumsum()

plt.figure(figsize=(10,4))
plt.plot(drunk_walk)
plt.title("Drunk Man Random Walk")
plt.show()

# --------------------------------------------
# 4. BASIC AR(1) (VERY SIMPLE)
# r_today = a + b * r_yesterday
# --------------------------------------------

returns_lag = returns.shift(1).dropna()
returns_now = returns.iloc[1:]

# simple linear formula
b = np.cov(returns_now, returns_lag)[0][1] / np.var(returns_lag)

print("\n--- AR(1) BASIC ---")
print("AR(1) coefficient (b):", b)

# --------------------------------------------
# 5. LINEAR REGRESSION (PRICE TREND)
# --------------------------------------------

x = np.arange(len(prices))
y = prices.values

slope, intercept = np.polyfit(x, y, 1)

trend = slope * x + intercept

plt.figure(figsize=(10,4))
plt.plot(prices, label="Actual Price")
plt.plot(prices.index, trend, label="Trend Line")
plt.legend()
plt.title("Price Trend (Linear Regression)")
plt.show()

# --------------------------------------------
# 6. BETA (VOLATILITY RISK)
# Using NIFTY itself as market proxy (simple)
# --------------------------------------------

market_returns = returns
stock_returns = returns

beta = np.cov(stock_returns, market_returns)[0][1] / np.var(market_returns)

print("\n--- BETA (RISK) ---")
print("Beta:", beta)

# --------------------------------------------
# 7. FINAL OBSERVATIONS
# --------------------------------------------

print("\n========== FINAL OBSERVATIONS ==========")

# Randomness
if abs(b) < 0.05:
    print("Randomness: Market is mostly RANDOM (efficient).")
else:
    print("Randomness: Some predictability exists.")

# Buy or Not
if slope > 0:
    print("Buy Decision: LONG-TERM BUY (upward trend).")
else:
    print("Buy Decision: AVOID / HOLD (no clear growth).")

# Overvalued / Undervalued
current_price = prices.iloc[-1]
trend_price = trend[-1]

if current_price > trend_price:
    print("Valuation: OVERVALUED (price above trend).")
else:
    print("Valuation: UNDERVALUED (price below trend).")

# Risk
if beta > 1:
    print("Risk Level: HIGH volatility (riskier than market).")
else:
    print("Risk Level: LOW to MODERATE volatility.")

print("========================================")

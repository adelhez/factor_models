from utils import align_data_from_time
from assets import Asset
import numpy as np


# Estimate Beta with an unique risk-free rate.
def estimate_beta():
    rf = 0.04
    apple = Asset("AAPL")
    market = Asset("^GSPC")
    stock_data, mkt_data = align_data_from_time(apple.raw_data, market.raw_data)
    stock_excess_returns = stock_data["Adj Close"].pct_change().iloc[1:].to_numpy().flatten() - rf
    mkt_escess_returns = mkt_data["Adj Close"].pct_change().iloc[1:].to_numpy().flatten() - rf
    param = np.polyfit(mkt_escess_returns, stock_excess_returns, deg=1)
    print(f"Beta is {param[1]}")
    return stock_excess_returns, mkt_escess_returns, param




if __name__ == "__main__":
    estimate_beta()



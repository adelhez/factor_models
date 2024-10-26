from utils import align_data_from_time
from assets import Stock, TreasuryBill
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Estimate Beta with an unique risk-free rate.
def estimate_beta():
    treasury_bill = TreasuryBill("^FVX")
    stock = Stock("AAPL")
    market = Stock("^GSPC")
    # rf = treasury_bill.get_rf_rate()
    rf = 0.01
    stock_data, mkt_data = align_data_from_time([stock.raw_data, market.raw_data])
    stock_excess_returns = stock.get_periodic_returns("YE", stock_data) - rf
    mkt_escess_returns = market.get_periodic_returns("YE", mkt_data) - rf
    print(stock_excess_returns.size)
    print(mkt_escess_returns.size)
    param = np.polyfit(mkt_escess_returns, stock_excess_returns, deg=1)
    print(f"Beta is {param[0]}")
    return stock_excess_returns, mkt_escess_returns, param

def estimate_beta_yearly():
    stock = Stock("AAPL")
    treasury_bill = TreasuryBill("^FVX")
    market = Stock("^GSPC") 

    stock_data, mkt_data, tb_data = align_data_from_time([stock.raw_data, market.raw_data, treasury_bill.raw_data])
    rf_rates = treasury_bill.get_periodic_mean(tb_data, freq="YE")
    stock_excess_returns = apply_rf(stock.get_periodic_returns("YE", stock_data), rf_rates)
    mkt_escess_returns = apply_rf(market.get_periodic_returns("YE", mkt_data), rf_rates)
    param = np.polyfit(mkt_escess_returns, stock_excess_returns, deg=1)
    print(f"Beta is {param[0]}")
    return stock_excess_returns, mkt_escess_returns, param


def apply_rf(excess_returns: np.ndarray, rf_rates: np.ndarray):
    if len(excess_returns) != len(rf_rates):
        print(f"Excess returns {len(excess_returns)} and risk-free rates {len(rf_rates)} should have the same periodicity.")
    return np.array([excess_returns[i] - rf_rates[i] for i in range(0, len(excess_returns))]) 



if __name__ == "__main__":
    #stock_excess_returns, mkt_escess_returns, param = estimate_beta()
    stock_excess_returns, mkt_escess_returns, param = estimate_beta_yearly()
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.scatter(mkt_escess_returns, stock_excess_returns, s=60, alpha=0.7, edgecolors="k")
    xreg = np.linspace(min(mkt_escess_returns), max(mkt_escess_returns), num=100)
    ax.plot(xreg, param[1] + param[0] * xreg, color="k", lw=2.5, alpha=0.7)
    ax.set_title("Security Market Line (SLM)")
    ax.set_xlabel("Market excess returns")
    ax.set_ylabel("Security excess returns")
    fig.savefig('images/security_market_line.png', dpi=fig.dpi)




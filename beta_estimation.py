from utils import align_data_from_time, get_excess_returns
from assets import Stock, TreasuryBill, Asset
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum


class Periodicity(Enum):
    MONTHLY = "ME", 1/12
    QUATERLY = "3ME", 3/12
    SEMI_ANNUALLY = "6ME", 1/2
    ANNUALLY = "YE", 1

    def __init__(self, alias, nbr):
        self.alias = alias
        self.nbr = nbr


# Estimate Beta with an unique risk-free rate.
def estimate_beta(asset, market, treasury_bill):
    rf = treasury_bill.get_current_rf_rate()
    asset_data, mkt_data = align_data_from_time([asset.raw_data, market.raw_data])
    stock_excess_returns = asset.get_periodic_returns("YE", asset_data) - rf
    mkt_escess_returns = market.get_periodic_returns("YE", mkt_data) - rf
    param = np.polyfit(mkt_escess_returns, stock_excess_returns, deg=1)
    print(f"Beta is {param[0]}")
    return stock_excess_returns, mkt_escess_returns, param

def estimate_beta(asset: Asset, market: Asset, treasury_bill: TreasuryBill, periodicity: Periodicity = None):
    # Get data starting from same date.
    asset_data, mkt_data, tb_data = align_data_from_time([asset.raw_data, market.raw_data, treasury_bill.raw_data])
    
    # Calculte the risk-free rate(s)
    rf_rates = treasury_bill.get_periodic_rf_rate(tb_data, periodicity.alias)
    # Calculate the excess returns over the risk-free rate(s).
    stock_excess_returns = get_excess_returns(asset.get_periodic_returns(asset_data, periodicity.alias), rf_rates)
    mkt_excess_returns = get_excess_returns(market.get_periodic_returns(mkt_data, periodicity.alias), rf_rates)

    # Interpolate the excess market returns and the excess asset returns.
    param = np.polyfit(mkt_excess_returns, stock_excess_returns, deg=1)
    print(f"The estimated beta of {asset.name} is = {param[0]:4f}")
    return stock_excess_returns, mkt_excess_returns, param



if __name__ == "__main__":
    stock = Stock("AAPL")
    market = Stock("^GSPC")
    treasury_bill = TreasuryBill("^IRX")
    stock_excess_returns, mkt_escess_returns, param = estimate_beta(stock, market, treasury_bill, Periodicity.ANNUALLY)
    #stock_excess_returns, mkt_escess_returns, param = estimate_beta(stock, market, treasury_bill, Periodicity.QUATERLY)

    fig, ax = plt.subplots(figsize=(9, 9))
    ax.scatter(mkt_escess_returns, stock_excess_returns, s=60, alpha=0.7, edgecolors="k")
    xreg = np.linspace(min(mkt_escess_returns), max(mkt_escess_returns), num=100)
    ax.plot(xreg, param[1] + param[0] * xreg, color="k", lw=2.5, alpha=0.7)
    ax.set_title("Security Market Line (SLM)")
    ax.set_xlabel("Market excess returns")
    ax.set_ylabel("Security excess returns")
    fig.savefig('images/security_market_line.png', dpi=fig.dpi)




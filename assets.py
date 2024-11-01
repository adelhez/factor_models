import yfinance as yf
import numpy as np
import pandas as pd
from enum import Enum

class Periodicity(Enum):
    MONTHLY = "ME", 1/12
    QUATERLY = "3ME", 3/12
    SEMI_ANNUALLY = "6ME", 1/2
    ANNUALLY = "YE", 1

    def __init__(self, alias, nbr):
        self.alias = alias
        self.nbr = nbr

class Asset(): 
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.name = self.ticker.info["shortName"]
        self.raw_data = yf.download(symbol)


class Stock(Asset):
    def __init__(self, symbol: str):
        super().__init__(symbol)

    @staticmethod
    def get_returns(data) -> np.ndarray:
        # Remove first line with NaN return 
        return data["Adj Close"].pct_change().iloc[1:].to_numpy().flatten()
    
    @staticmethod
    def get_periodic_returns(data, freq) -> np.ndarray:
        return data["Adj Close"].pct_change().resample(freq).agg(lambda x: (x + 1).prod() - 1).to_numpy().flatten()


class TreasuryBill(Asset):
    def __init__(self, symbol: str):
        """Treasury Bill used as risk-free rates.
        Arg:
            symbol: str: "^IRX": 13weeks Treasury Yield 
                         "^FVX": 5years Treasury Yield 
                         "^TYX": 10years Treasury Yield 
        """
        super().__init__(symbol)

    def get_current_rf_rate(self):
        """Get the current risk-free rate"""
        return self.get_prices()[-1]/100

    @staticmethod
    def get_periodic_rf_rate(data, freq: Periodicity) -> np.ndarray:
        # In addition to the periodicity, the choice of the TreasuryBill is important.
        # Get the mean risk-free rate for the specified period, which are given on an yearly basis.
        rf_df = data.groupby(pd.Grouper(level="Date", freq=freq.alias)).mean()
        yearly_rf_rates = rf_df["Adj Close"].values.flatten()/100
        # Get the risk-free rates on the periodic basis.
        periodic_rf_rates = (1 + yearly_rf_rates)**freq.nbr - 1
        return periodic_rf_rates


if __name__ == "__main__":
    stock = Asset("^FVX")
    data = stock.raw_data
    g = data.groupby(pd.Grouper(level="Date", freq="ME"))
    dfs = [group for _,group in g]
    print(dfs[1]["Adj Close"].mean().values[0])
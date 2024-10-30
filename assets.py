import yfinance as yf
import numpy as np
import pandas as pd

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
    def get_periodic_rf_rate(data, freq) -> np.ndarray:
        g = data.groupby(pd.Grouper(level="Date", freq=freq))
        df_list = [group for _,group in g]
        periodic_mean = np.array([])
        for df in df_list:
            periodic_mean = np.append(periodic_mean, df["Adj Close"].mean().values[0]/100)
        return periodic_mean


if __name__ == "__main__":
    stock = Asset("^FVX")
    data = stock.raw_data
    g = data.groupby(pd.Grouper(level="Date", freq="ME"))
    dfs = [group for _,group in g]
    print(dfs[1]["Adj Close"].mean().values[0])
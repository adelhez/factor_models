import yfinance as yf
import numpy as np
import pandas as pd

class Asset(): 
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.raw_data = yf.download(symbol)


class Stock(Asset):
    def __init__(self, symbol: str):
        super().__init__(symbol)

    def get_returns(self, df=None) -> np.ndarray:
        if df is None:
            df = self.raw_data
        # Remove first line with NaN return 
        return df["Adj Close"].pct_change().iloc[1:].to_numpy().flatten()
    
    def get_periodic_returns(self, freq, df=None) -> np.ndarray:
        if df is None:
            df = self.raw_data
        return df["Adj Close"].pct_change().resample(freq).agg(lambda x: (x + 1).prod() - 1).to_numpy().flatten()


class TreasuryBill(Asset):
    def __init__(self, symbol: str):
        # "^IRX": Treasury Yield 13weeks
        # "^FVX": Treasury Yield 5years
        # "^TYX": Treasury Yield 10years
        super().__init__(symbol)

    def get_rf_rate(self):
        return self.get_prices()[-1]/100
    
    def get_rf_rates(self) -> np.ndarray:
        return self.get_prices()/100    

    def get_periodic_mean(self, data, freq) -> np.ndarray:
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
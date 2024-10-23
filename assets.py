import yfinance as yf
import numpy as np

class Asset():
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.data = yf.download(symbol)
        self.pd_prices = self.data["Adj Close"]
        self.pd_returns = self.data["Adj Close"].pct_change()
    
    def get_prices(self) -> np.ndarray:
        return self.pd_prices.to_numpy().flatten()

    def get_returns(self) -> np.ndarray:
        # Remove first line with NaN return 
        return self.pd_returns.iloc[1:].to_numpy().flatten()


class TreasuryBill(Asset):
    def __init__(self, symbol: str):
        # "^IRX": Treasury Yield 13weeks
        # "^FVX": Treasury Yield 5years
        # "^TYX": Treasury Yield 10years
        super().__init__(symbol)

    def get_rf_rate(self):
        return self.get_prices()[-1]
    
    def get_rf_rates(self) -> np.ndarray:
        return self.get_prices()     


if __name__ == "__main__":
    stock = Asset("^FVX")
    data = stock.data
    print(data)
    print(data.isnull().sum())
    print(stock._get_returns())
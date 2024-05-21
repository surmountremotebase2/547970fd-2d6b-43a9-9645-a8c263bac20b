from surmount.base_class import Strategy, TargetAllocation
from surmount.data import FundamentalData, MarketData
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming there's a way to request all tickers or a subset where you might find such criteria
        self.candidate_tickers = ["Example list of tickers"]  # This list might come from an external source or market data
        self.fundamental_data_list = [FundamentalData(ticker) for ticker in self.candidate_tickers]   

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        # Dynamic asset list based on qualifying criteria; updated periodically
        return self.candidate_tickers

    @property
    def data(self):
        return self.fundamental_data_list
    
    def filter_stocks(self, data):
        """Filter stocks based on P/E, Dividend Yield, and Market Cap criteria."""
        qualified_tickers = []

        for ticker in self.candidate_tickers:
            pe_ratio = data[f"{ticker}_pe_ratio"]
            dividend_yield = data[f"{ticker}_dividend_yield"]
            market_cap = data[f"{ticker}_market_cap"]

            if pe_ratio < 10 and dividend_yield > 0.08 and market_cap > 500000000:
                qualified_tickers.append(ticker)

        # Sort or prioritize based on further logic if needed
        return qualified_tickers[:20]  # Top 20 stocks as per the requirement
    
    def run(self, data):
        # Assuming
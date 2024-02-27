from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, STDEV
from surmount.logging import log
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["ExampleTicker"]  # Add your target tickers here
        
        # Custom parameters for the strategy
        self.notional_dollar_volume_threshold = 100000000
        self.volume_threshold = 5000000
        self.sma_length = 200
        self.stdev_length = 20
        self.stdev_multiplier = 3
        self.profit_target = 0.03  # 3%
        self.max_drawdown = 0.01  # 1%
        
    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [OHLCV(i) for i in self.tickers]  # Assuming OHLCV data class exists and is structured accordingly

    def run(self, data):
        allocations = {}
        
        for ticker in self.tickers:
            ohlcv_data = data["ohlcv"][ticker]  # Accessing the OHLCV data for the ticker

            if not ohlcv_data:
                continue

            # Calculate SMA and Standard Deviation
            sma_data = SMA(ticker, ohlcv_data, self.sma_length)
            stdev_data = STDEV(ticker, ohlcv_data, self.stdev_length)
            
            if not sma_data or not stdev_data:
                continue
            
            latest_close = ohlcv_data[-1]['close']
            latest_volume = ohlcv_data[-1]['volume']
            notional_dollar_volume = latest_close * latest_volume

            # Check conditions: volume, notional dollar volume, SMA, and standard deviation criteria
            if (latest_volume > self.volume_threshold and 
                notional_dollar_volume > self.notional_dollar_volume_threshold and 
                latest_close > sma_data[-1] and  # Assuming we're now "400 days or more above its 200 SMA"
                (latest_close > sma_data[-1] + stdev_data[-1] * self.stdev_multiplier)):  # 3 SD move to the upside
                
                # Strategy: Short the stock
                allocations[ticker] = -1  # Representing a short position; you'll need to adjust based on your actual position calculation
            else:
                allocations[ticker] = 0  # No action

        return TargetAllocation(allocations)
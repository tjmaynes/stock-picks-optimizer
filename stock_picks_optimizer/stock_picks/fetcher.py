from typing import List, Dict
from requests import Session
from requests_cache import CacheMixin
from requests_cache.backends.sqlite import SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
import yfinance as yf


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


class StockPicksFetcher:
    def __init__(self) -> None:
        self.session = CachedLimiterSession(
            limiter=Limiter(
                RequestRate(2, Duration.SECOND * 5)
            ),  # max 2 requests per 5 seconds
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache("yfinance.cache"),
        )
        self.session.headers["User-agent"] = "stock-picks-optimizer/0.1.0"

    def get_last_prices(self, symbols: List[str]) -> Dict[str, float]:
        stock_info = yf.Tickers(" ".join(symbols), session=self.session)

        results = {}
        for symbol in symbols:
            info = stock_info.tickers[symbol].fast_info
            results[symbol] = round(info.last_price, 2)

        return results

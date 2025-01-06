from typing import List, Dict
import yfinance as yf
from requests import Session


class FetchLatestStockPricesUseCase:
    def __init__(self, session: Session) -> None:
        self.session = session

    def invoke(self, symbols: List[str]) -> Dict[str, float]:
        stock_info = yf.Tickers(" ".join(symbols), session=self.session)

        results = {}
        for symbol in symbols:
            info = stock_info.tickers[symbol].fast_info
            results[symbol] = round(info.last_price, 2)

        return results

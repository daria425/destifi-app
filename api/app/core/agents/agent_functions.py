from typing import List, Dict
import json

def extract_stock_sentiment(
    symbol: str,
    sentiment_score: float,
    sentiment_category: str,
    key_news:List[str],
) -> str:
    """
    Extracts structured stock sentiment details.

    :param symbol: The stock ticker symbol (e.g., 'AAPL').
    :param sentiment_score: The overall sentiment score (-1 to 1).
    :param sentiment_category: Sentiment classification ('Bullish', 'Neutral', 'Bearish').
    :param key_news: List of key news related to the stock.

    :return: A JSON string containing structured stock sentiment data.
    """
    stock_data = {
        "symbol": symbol,
        "sentiment_score": sentiment_score,
        "sentiment_category": sentiment_category,
        "key_news": key_news
    }
    
    return json.dumps(stock_data, indent=4)


def extract_market_sentiment(
    stock_data: List[Dict]
) -> str:
    """
    Extracts structured sentiment data for multiple stocks.

    :param stock_data: A list of dictionaries, each containing stock sentiment details.

    :return: A JSON string containing a list of structured stock sentiment data.
    """
    market_data = {"stocks": stock_data}
    
    return json.dumps(market_data, indent=4)
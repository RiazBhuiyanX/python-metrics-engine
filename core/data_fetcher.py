import ccxt
import pandas as pd

# =======================
# Constants
# =======================
DEFAULT_SYMBOL = "BTC/USDT"
DEFAULT_TIMEFRAME = "5m"
DEFAULT_LIMIT = 1000


def fetch_binance_data(
    symbol=DEFAULT_SYMBOL, timeframe=DEFAULT_TIMEFRAME, limit=DEFAULT_LIMIT
):
    """
    Fetch historical OHLCV data from Binance using CCXT.

    Returns:
        pd.DataFrame: DataFrame with OHLCV data and localized timestamps.
    """

    # Connect to Binance exchange via ccxt
    exchange = ccxt.binance()
    try:
        # API CALL: Fetch historical data
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    except ccxt.NetworkError as e:
        print(f"[ERROR] Network error during API call to Binance: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"[ERROR] Failed to fetch data. Check symbol/timeframe or API key: {e}")
        return pd.DataFrame()

    # Convert to DataFrame and name columns
    df = pd.DataFrame(
        ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    # Drop last candle (usually incomplete)
    df = df.iloc[:-1]

    # Convert timestamp to localized datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["timestamp"] = (
        df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Europe/Sofia")
    )

    # Save to CSV for inspection
    df.to_csv("data/btc_usdt_ohlcv.csv", index=False)

    return df

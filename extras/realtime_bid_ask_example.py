# ⚠️ Important: This file is NOT used in the main simulation.
# Example of fetching real-time bid and ask prices from Binance using ccxt

import ccxt

# Connect to Binance through ccxt
exchange = ccxt.binance()

# Choose market symbols
symbol = 'BTC/USDT'

# Getting best 5 bids and asks
orderbook = exchange.fetch_order_book(symbol, limit=5)

# Getting the best bid and ask
best_bid = orderbook['bids'][0][0] if orderbook['bids'] else None
best_ask = orderbook['asks'][0][0] if orderbook['asks'] else None

# Show the best bid and ask
print("Real-time best prices from Binance:")
print(f"Best Bid: {best_bid}")
print(f"Best Ask: {best_ask}")


#!/usr/bin/env python3
"""
Test script for market data fetching
"""
import sys
from market_data import MarketDataFetcher

def main():
    print("=" * 60)
    print("Testing Market Data Fetcher")
    print("=" * 60)

    # Initialize fetcher
    fetcher = MarketDataFetcher()

    # Test coins
    coins = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'DOGE']

    print(f"\nFetching prices for: {', '.join(coins)}")
    print("-" * 60)

    # Get prices
    prices = fetcher.get_current_prices(coins)

    if prices:
        print("\n✓ Successfully fetched prices:\n")
        for coin, data in prices.items():
            price = data['price']
            change = data['change_24h']
            change_symbol = "↑" if change >= 0 else "↓"
            change_color = "+" if change >= 0 else ""

            print(f"  {coin:6} ${price:>12,.2f}  {change_symbol} {change_color}{change:.2f}%")

        print("\n" + "=" * 60)
        print(f"✓ Test completed successfully! Got {len(prices)}/{len(coins)} prices")
        print("=" * 60)
        return 0
    else:
        print("\n✗ Failed to fetch prices!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())

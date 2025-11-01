#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test multiple data sources integration
"""

from market_data import MarketDataFetcher

def test_data_sources():
    """Test all data sources with different priorities"""

    test_coins = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'DOGE']

    print("=" * 80)
    print("Testing Data Sources Integration")
    print("=" * 80)

    # Test 1: Odaily first (default)
    print("\n[Test 1] Priority: Odaily > 528btc > Binance > CoinGecko")
    fetcher1 = MarketDataFetcher(data_source_priority=['odaily', '528btc', 'binance', 'coingecko'])
    prices1 = fetcher1.get_current_prices(test_coins)
    if prices1:
        print(f"✓ Successfully fetched {len(prices1)} prices")
        for coin, data in prices1.items():
            print(f"  {coin}: ${data['price']} ({data['change_24h']:+.2f}%)")
    else:
        print("✗ Failed to fetch prices")

    # Test 2: 528btc first
    print("\n[Test 2] Priority: 528btc > Binance > CoinGecko")
    fetcher2 = MarketDataFetcher(data_source_priority=['528btc', 'binance', 'coingecko'])
    prices2 = fetcher2.get_current_prices(test_coins)
    if prices2:
        print(f"✓ Successfully fetched {len(prices2)} prices")
        for coin, data in prices2.items():
            print(f"  {coin}: ${data['price']} ({data['change_24h']:+.2f}%)")
    else:
        print("✗ Failed to fetch prices")

    # Test 3: Binance only
    print("\n[Test 3] Priority: Binance only")
    fetcher3 = MarketDataFetcher(data_source_priority=['binance'])
    prices3 = fetcher3.get_current_prices(test_coins)
    if prices3:
        print(f"✓ Successfully fetched {len(prices3)} prices")
        for coin, data in prices3.items():
            print(f"  {coin}: ${data['price']} ({data['change_24h']:+.2f}%)")
    else:
        print("✗ Failed to fetch prices")

    print("\n" + "=" * 80)
    print("Test completed")
    print("=" * 80)

if __name__ == "__main__":
    test_data_sources()

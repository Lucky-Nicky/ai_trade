#!/usr/bin/env python3
"""Check if 528btc.com prices are updating"""
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def get_prices():
    """Fetch current prices from 528btc.com"""
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    response = requests.get('https://www.528btc.com/', headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    prices = {}
    for coin in ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'DOGE']:
        coin_element = soup.find('div', class_='walking_name', string=coin)
        if coin_element:
            parent = coin_element.parent
            price_elem = parent.find('div', class_='walking_price')
            change_elem = parent.find('div', class_='walking_change')

            if price_elem and change_elem:
                price = price_elem.text.strip().replace('$', '').replace(',', '')
                change = change_elem.text.strip().replace('%', '')
                prices[coin] = {'price': price, 'change': change}

    return prices

print("=" * 70)
print("检查 528btc.com 价格是否实时更新")
print("=" * 70)

print("\n第一次获取 (现在):")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
prices1 = get_prices()
for coin, data in prices1.items():
    print(f"  {coin:6} ${data['price']:>12}  变化: {data['change']:>6}%")

print("\n等待 20 秒...")
time.sleep(20)

print("\n第二次获取 (20秒后):")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
prices2 = get_prices()
for coin, data in prices2.items():
    print(f"  {coin:6} ${data['price']:>12}  变化: {data['change']:>6}%")

print("\n" + "=" * 70)
print("对比结果:")
print("=" * 70)

changed = False
for coin in prices1.keys():
    if prices1[coin] != prices2[coin]:
        print(f"❌ {coin}: 价格或涨跌幅发生变化")
        print(f"   第一次: ${prices1[coin]['price']} ({prices1[coin]['change']}%)")
        print(f"   第二次: ${prices2[coin]['price']} ({prices2[coin]['change']}%)")
        changed = True

if not changed:
    print("\n✓ 所有币种的价格和涨跌幅在 20 秒内保持不变")
    print("  这说明 528btc.com 的数据更新频率可能 >= 20秒")
    print("  或者当前时段市场价格变化较小")

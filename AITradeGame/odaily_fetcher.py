#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Odaily星球日报加密货币市场数据获取模块
功能：获取全部币种的交易对、最新价、涨跌幅、最高价、最低价、24H成交额、市值等信息
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List


class OdailyFetcher:
    """Odaily市场数据获取器"""

    def __init__(self):
        self.base_url = 'https://www.odaily.news/zh-CN/market'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
        }

    def get_crypto_market_data(self) -> List[Dict[str, str]]:
        """
        获取加密货币市场数据

        Returns:
            List[Dict]: 包含币种市场信息的列表
        """
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找主要的市场数据表格（第一个表格包含完整的市场数据）
            tables = soup.find_all('table')
            if not tables:
                print("[ERROR] Odaily: 未找到数据表格")
                return []

            main_table = tables[0]  # 使用第一个表格，它包含主要市场数据

            # 查找表格数据行
            tbody = main_table.find('tbody')
            if not tbody:
                print("[ERROR] Odaily: 未找到表格数据")
                return []

            rows = tbody.find_all('tr')
            crypto_data = []

            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 8:  # 确保有足够的列
                    row_data = {}

                    # 提取每一列的数据
                    for i, cell in enumerate(cells):
                        cell_text = cell.get_text().strip()

                        if i == 0:  # 排名
                            row_data['rank'] = cell_text
                        elif i == 1:  # 交易对
                            row_data['trading_pair'] = cell_text
                        elif i == 2:  # 最新价
                            row_data['latest_price'] = cell_text
                        elif i == 3:  # 涨跌幅
                            row_data['change_24h'] = cell_text
                        elif i == 4:  # 最高价
                            row_data['high_price'] = cell_text
                        elif i == 5:  # 最低价
                            row_data['low_price'] = cell_text
                        elif i == 6:  # 24H成交额
                            row_data['volume_24h'] = cell_text
                        elif i == 7:  # 市值
                            row_data['market_cap'] = cell_text

                    # 只添加有效数据的行
                    if row_data.get('trading_pair') and row_data.get('latest_price'):
                        crypto_data.append(row_data)

            return crypto_data

        except requests.RequestException as e:
            print(f"[ERROR] Odaily网络请求错误: {e}")
            return []
        except Exception as e:
            print(f"[ERROR] Odaily数据解析错误: {e}")
            return []

    def get_prices_for_coins(self, coins: List[str]) -> Dict[str, Dict]:
        """
        获取指定币种的价格信息（格式化为统一接口）

        Args:
            coins: 币种列表，例如 ['BTC', 'ETH', 'SOL']

        Returns:
            Dict: 币种价格字典
        """
        try:
            all_data = self.get_crypto_market_data()

            if not all_data:
                print("[ERROR] Odaily: 未能获取到市场数据")
                return {}

            prices = {}

            for coin in coins:
                # 查找匹配的交易对（例如 BTC/USDT 匹配 BTC）
                for data in all_data:
                    trading_pair = data.get('trading_pair', '')

                    # 尝试多种匹配方式
                    if (trading_pair.upper().startswith(coin.upper() + '/') or
                        trading_pair.upper().startswith(coin.upper() + 'USDT') or
                        trading_pair.upper() == coin.upper()):

                        # 解析价格
                        price_str = data.get('latest_price', '').replace('$', '').replace(',', '')
                        try:
                            price = float(price_str)
                        except:
                            continue

                        # 解析涨跌幅
                        change_str = data.get('change_24h', '').replace('%', '').replace('+', '')
                        try:
                            change_24h = float(change_str)
                        except:
                            change_24h = 0.0

                        prices[coin] = {
                            'price': price,
                            'change_24h': change_24h,
                            'high_24h': data.get('high_price', ''),
                            'low_24h': data.get('low_price', ''),
                            'volume_24h': data.get('volume_24h', ''),
                            'market_cap': data.get('market_cap', '')
                        }
                        break

            if len(prices) > 0:
                print(f"[INFO] Odaily成功获取 {len(prices)} 个币种价格")

            return prices

        except Exception as e:
            print(f"[ERROR] Odaily获取价格失败: {e}")
            return {}


def main():
    """测试函数"""
    print("🔍 测试Odaily数据获取器...")

    fetcher = OdailyFetcher()

    # 测试获取指定币种
    test_coins = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'DOGE']
    prices = fetcher.get_prices_for_coins(test_coins)

    print(f"\n获取到 {len(prices)} 个币种价格:")
    for coin, data in prices.items():
        print(f"  {coin}: ${data['price']} ({data['change_24h']:+.2f}%)")


if __name__ == "__main__":
    main()

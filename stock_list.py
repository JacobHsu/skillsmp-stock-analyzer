"""
台股清單載入模組
從 data/stocks.json 讀取股票清單
"""
import json
import os
from typing import List, Dict

# 取得專案根目錄
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STOCKS_JSON_PATH = os.path.join(ROOT_DIR, 'data', 'stocks.json')


def load_stocks() -> tuple[List[str], Dict[str, str]]:
    """
    從 JSON 檔案載入股票清單

    Returns:
        tuple: (股票代碼列表, 股票名稱對照字典)
    """
    with open(STOCKS_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tickers = [stock['ticker'] for stock in data['stocks']]
    names = {stock['ticker']: stock['name'] for stock in data['stocks']}

    return tickers, names


# 載入股票資料
GIFT_STOCKS, STOCK_NAMES = load_stocks()

# 便利的子集
TOP_20 = GIFT_STOCKS[:20]
TOP_10 = GIFT_STOCKS[:10]


def get_stock_name(ticker: str) -> str:
    """取得股票名稱"""
    return STOCK_NAMES.get(ticker, "未知")


def get_stock_count() -> int:
    """取得股票總數"""
    return len(GIFT_STOCKS)


# 使用範例
if __name__ == "__main__":
    print("=" * 60)
    print("台股清單資訊")
    print("=" * 60)
    print(f"\n資料來源: {STOCKS_JSON_PATH}")
    print(f"總股票數: {get_stock_count()} 支")
    print(f"資料狀態: 全部可用")

    print(f"\n前 10 支股票:")
    for i, ticker in enumerate(TOP_10, 1):
        print(f"  {i:2d}. {ticker:<12} {get_stock_name(ticker)}")

    print(f"\n使用範例:")
    print("  from stock_list import GIFT_STOCKS, STOCK_NAMES")
    print("  from stock_list import TOP_20, TOP_10")
    print("  from stock_list import get_stock_name")
    print("\n" + "=" * 60)

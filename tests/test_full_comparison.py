"""
完整測試：50 支台股比較排名
顯示股票名稱和詳細分析結果
"""
import sys
import os
import time
from datetime import datetime

if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

sys.path.append('scripts')
sys.path.append('.')
from main import StockAnalyzer
from stock_list import GIFT_STOCKS, STOCK_NAMES

print("=" * 80)
print("台股技術分析 - 完整股票比較測試")
print("=" * 80)
print(f"\n開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"股票數量: {len(GIFT_STOCKS)} 支")
print("\n" + "-" * 80)

analyzer = StockAnalyzer()

# 記錄開始時間
start_time = time.time()

print("\n正在分析中...")
print("(這可能需要 2-3 分鐘，請稍候)")

try:
    result = analyzer.compare(
        GIFT_STOCKS,
        rank_by="momentum",
        indicators=["RSI", "MACD"]
    )

    # 計算執行時間
    elapsed_time = time.time() - start_time

    print("\n" + "=" * 80)
    print("分析完成！")
    print("=" * 80)
    print(f"\n執行時間: {elapsed_time:.2f} 秒 ({elapsed_time/60:.2f} 分鐘)")
    print(f"平均每支: {elapsed_time/len(GIFT_STOCKS):.2f} 秒")
    print(f"分析股票: {len(result['ranked_stocks'])}/{result['total_analyzed']} 支")

    # 統計訊號
    buy_count = sum(1 for s in result['ranked_stocks'] if s['analysis']['signal']['action'] == 'BUY')
    sell_count = sum(1 for s in result['ranked_stocks'] if s['analysis']['signal']['action'] == 'SELL')
    hold_count = sum(1 for s in result['ranked_stocks'] if s['analysis']['signal']['action'] == 'HOLD')

    print("\n" + "=" * 80)
    print("市場概況")
    print("=" * 80)
    print(f"買入訊號: {buy_count} 支 ({buy_count/len(result['ranked_stocks'])*100:.1f}%)")
    print(f"賣出訊號: {sell_count} 支 ({sell_count/len(result['ranked_stocks'])*100:.1f}%)")
    print(f"持有訊號: {hold_count} 支 ({hold_count/len(result['ranked_stocks'])*100:.1f}%)")

    # 顯示 Top 20 排名
    print("\n" + "=" * 80)
    print("技術面排名 Top 20")
    print("=" * 80)
    print(f"{'排名':<6} {'代碼':<12} {'名稱':<10} {'分數':<8} {'RSI':<7} {'MACD':<12} {'建議':<6}")
    print("-" * 80)

    for i, stock in enumerate(result['ranked_stocks'][:20], 1):
        ticker = stock['ticker']
        name = STOCK_NAMES.get(ticker, "未知")
        analysis = stock['analysis']
        score = stock['score']
        rsi = analysis['indicators']['RSI']['value']
        macd = analysis['indicators']['MACD']['signal']
        action = analysis['signal']['action']

        # MACD 訊號中文化
        macd_cn = {
            'buy': '黃金交叉',
            'sell': '死亡交叉',
            'bullish': '多頭',
            'bearish': '空頭',
            'neutral': '中性'
        }.get(macd, macd)

        print(f"#{i:<5} {ticker:<12} {name:<10} {score:>6.1f}  {rsi:>5.1f}  {macd_cn:<12} {action:<6}")

    # 買入訊號詳細列表
    buy_signals = [s for s in result['ranked_stocks'] if s['analysis']['signal']['action'] == 'BUY']

    if buy_signals:
        print("\n" + "=" * 80)
        print(f"買入訊號詳細 (共 {len(buy_signals)} 支)")
        print("=" * 80)

        for i, stock in enumerate(buy_signals, 1):
            ticker = stock['ticker']
            name = STOCK_NAMES.get(ticker, "未知")
            analysis = stock['analysis']

            print(f"\n{i}. {ticker} - {name}")
            print(f"   價格: NT$ {analysis['current_price']:.2f}")
            print(f"   技術分數: {stock['score']:.1f}")
            print(f"   RSI: {analysis['indicators']['RSI']['value']:.2f} - {analysis['indicators']['RSI']['interpretation']}")
            print(f"   MACD: {analysis['indicators']['MACD']['interpretation']}")
            print(f"   信心度: {analysis['signal']['confidence']}")
            print(f"   理由: {', '.join(analysis['signal']['reasoning'])}")

    # 高信心度買入訊號
    high_confidence_buy = [s for s in buy_signals if s['analysis']['signal']['confidence'] == 'high']

    if high_confidence_buy:
        print("\n" + "=" * 80)
        print(f"高信心度買入訊號 (共 {len(high_confidence_buy)} 支)")
        print("=" * 80)

        for i, stock in enumerate(high_confidence_buy, 1):
            ticker = stock['ticker']
            name = STOCK_NAMES.get(ticker, "未知")
            analysis = stock['analysis']
            print(f"{i}. {ticker} - {name} (NT$ {analysis['current_price']:.2f})")

    # 賣出警示
    sell_signals = [s for s in result['ranked_stocks'] if s['analysis']['signal']['action'] == 'SELL']

    if sell_signals:
        print("\n" + "=" * 80)
        print(f"賣出訊號警示 (共 {len(sell_signals)} 支)")
        print("=" * 80)

        for i, stock in enumerate(sell_signals[:10], 1):  # 只顯示前 10 支
            ticker = stock['ticker']
            name = STOCK_NAMES.get(ticker, "未知")
            analysis = stock['analysis']
            print(f"{i}. {ticker} - {name}")
            print(f"   RSI: {analysis['indicators']['RSI']['value']:.2f}")
            print(f"   理由: {', '.join(analysis['signal']['reasoning'])}")

    print("\n" + "=" * 80)
    print("測試完成!")
    print("=" * 80)
    print(f"結束時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

except Exception as e:
    print(f"\n錯誤: {str(e)}")
    import traceback
    traceback.print_exc()

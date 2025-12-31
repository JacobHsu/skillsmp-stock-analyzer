"""
股票分析報告生成器
將分析結果轉換為美觀的 HTML 報告（TradingView 風格 - 雙欄布局）
"""
import sys
import os
from datetime import datetime

# 設定編碼
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

sys.path.append('scripts')
from main import StockAnalyzer
from stock_list import GIFT_STOCKS, STOCK_NAMES

def generate_html_report(analysis_result, output_path='docs/index.html'):
    """生成 HTML 報告 - 雙欄布局（SELL | BUY）"""

    # 提取數據
    ranked_stocks = analysis_result['ranked_stocks']

    # 分組：SELL 和 BUY
    sell_stocks = [s for s in ranked_stocks if s['analysis']['signal']['action'] == 'SELL']
    buy_stocks = [s for s in ranked_stocks if s['analysis']['signal']['action'] == 'BUY']

    # 更新時間
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 生成 SELL 股票列表
    sell_rows = []
    for i, stock in enumerate(sell_stocks, 1):
        ticker = stock['ticker'].replace('.TW', '')
        name = STOCK_NAMES.get(stock['ticker'], '未知')
        analysis = stock['analysis']
        score = stock['score']
        price = analysis['current_price']
        rsi = analysis['indicators']['RSI']['value']
        macd_signal = analysis['indicators']['MACD']['signal']

        # MACD 中文
        macd_map = {'buy': '黃金交叉', 'sell': '死亡交叉', 'bullish': '多頭', 'bearish': '空頭', 'neutral': '中性'}
        macd_cn = macd_map.get(macd_signal, macd_signal)

        row = f"""
                        <tr>
                            <td class="rank">{i}</td>
                            <td class="stock"><span class="ticker">{ticker}</span> <span class="name">{name}</span></td>
                            <td class="price">{price:.2f}</td>
                            <td class="score negative" title="計分：RSI-50 + MACD加分(-25~+25)">{score:.1f}</td>
                            <td>{rsi:.1f}</td>
                            <td>{macd_cn}</td>
                            <td class="signal-sell">SELL</td>
                        </tr>"""
        sell_rows.append(row)

    # 生成 BUY 股票列表
    buy_rows = []
    for i, stock in enumerate(buy_stocks, 1):
        ticker = stock['ticker'].replace('.TW', '')
        name = STOCK_NAMES.get(stock['ticker'], '未知')
        analysis = stock['analysis']
        score = stock['score']
        price = analysis['current_price']
        rsi = analysis['indicators']['RSI']['value']
        macd_signal = analysis['indicators']['MACD']['signal']

        # MACD 中文
        macd_map = {'buy': '黃金交叉', 'sell': '死亡交叉', 'bullish': '多頭', 'bearish': '空頭', 'neutral': '中性'}
        macd_cn = macd_map.get(macd_signal, macd_signal)

        row = f"""
                        <tr>
                            <td class="rank">{i}</td>
                            <td class="stock"><span class="ticker">{ticker}</span> <span class="name">{name}</span></td>
                            <td class="price">{price:.2f}</td>
                            <td class="score positive" title="計分：RSI-50 + MACD加分(-25~+25)">{score:.1f}</td>
                            <td>{rsi:.1f}</td>
                            <td>{macd_cn}</td>
                            <td class="signal-buy">BUY</td>
                        </tr>"""
        buy_rows.append(row)

    # 完整 HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>台股技術分析 - {update_time}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Trebuchet MS', Arial, 'Microsoft JhengHei', sans-serif;
            background: #f5f5f5;
            color: #131722;
            line-height: 1.5;
            padding: 20px;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
        }}

        header {{
            background: #ffffff;
            border-bottom: 1px solid #e0e3eb;
            padding: 20px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        h1 {{
            font-size: 18px;
            font-weight: 500;
            color: #131722;
        }}

        .update-time {{
            font-size: 13px;
            color: #787b86;
        }}

        .two-column {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1px;
            background: #e0e3eb;
        }}

        .column {{
            background: #ffffff;
        }}

        .column-header {{
            background: #f7f8fa;
            padding: 16px 24px;
            border-bottom: 1px solid #e0e3eb;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .column-title {{
            font-size: 14px;
            font-weight: 600;
            color: #131722;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}

        .badge.sell {{
            background: #fee;
            color: #f23645;
        }}

        .badge.buy {{
            background: #e8f5e9;
            color: #089981;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        thead {{
            background: #fafafa;
            position: sticky;
            top: 0;
        }}

        th {{
            color: #787b86;
            padding: 10px 24px;
            text-align: left;
            font-weight: 500;
            font-size: 11px;
            border-bottom: 1px solid #e0e3eb;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        tbody tr {{
            border-bottom: 1px solid #f5f5f5;
        }}

        tbody tr:nth-child(even) {{
            background: #fafafa;
        }}

        tbody tr:hover {{
            background: #f0f3fa;
        }}

        td {{
            padding: 12px 24px;
            color: #131722;
        }}

        .rank {{
            color: #787b86;
            width: 50px;
        }}

        .stock {{
            min-width: 200px;
        }}

        .ticker {{
            color: #787b86;
            font-size: 12px;
            margin-right: 6px;
        }}

        .name {{
            color: #131722;
            font-weight: 500;
            font-size: 14px;
        }}

        .price {{
            color: #131722;
            font-weight: 500;
        }}

        .score {{
            font-weight: 600;
            width: 80px;
            cursor: help;
        }}

        .score.positive {{
            color: #089981;
        }}

        .score.negative {{
            color: #f23645;
        }}

        .signal-buy {{
            color: #089981;
            font-weight: 600;
        }}

        .signal-sell {{
            color: #f23645;
            font-weight: 600;
        }}

        footer {{
            background: #fafafa;
            border-top: 1px solid #e0e3eb;
            padding: 16px 24px;
            text-align: center;
            color: #787b86;
            font-size: 11px;
        }}

        @media (max-width: 1024px) {{
            .two-column {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>台股技術分析篩選器</h1>
            <div class="update-time">更新時間：{update_time}</div>
        </header>

        <div class="two-column">
            <!-- SELL 欄位 -->
            <div class="column">
                <div class="column-header">
                    <span class="column-title">賣出訊號</span>
                    <span class="badge sell">{len(sell_stocks)} 支</span>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>商品</th>
                            <th>股價</th>
                            <th>分數</th>
                            <th>RSI</th>
                            <th>MACD</th>
                            <th>建議</th>
                        </tr>
                    </thead>
                    <tbody>
{''.join(sell_rows) if sell_rows else '<tr><td colspan="7" style="text-align:center;padding:40px;color:#787b86;">無賣出訊號</td></tr>'}
                    </tbody>
                </table>
            </div>

            <!-- BUY 欄位 -->
            <div class="column">
                <div class="column-header">
                    <span class="column-title">買入訊號</span>
                    <span class="badge buy">{len(buy_stocks)} 支</span>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>商品</th>
                            <th>股價</th>
                            <th>分數</th>
                            <th>RSI</th>
                            <th>MACD</th>
                            <th>建議</th>
                        </tr>
                    </thead>
                    <tbody>
{''.join(buy_rows) if buy_rows else '<tr><td colspan="7" style="text-align:center;padding:40px;color:#787b86;">無買入訊號</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>

        <footer>
            本報告由 GitHub Actions 自動生成 | 僅供參考，不構成投資建議 | 資料來源：Yahoo Finance
        </footer>
    </div>
</body>
</html>"""

    # 寫入檔案
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[OK] 報告已生成：{output_path}")
    return output_path


def main():
    """主程序"""
    print("=" * 70)
    print("開始生成股票分析報告（雙欄布局）")
    print("=" * 70)

    # 建立分析器
    analyzer = StockAnalyzer()

    print(f"\n正在分析 {len(GIFT_STOCKS)} 支股票...")
    print("這可能需要 10-15 秒，請稍候...\n")

    # 執行分析
    result = analyzer.compare(
        GIFT_STOCKS,
        rank_by="momentum",
        indicators=["RSI", "MACD"]
    )

    print(f"[OK] 分析完成！成功分析 {len(result['ranked_stocks'])} 支股票")

    # 生成報告
    print("\n正在生成 HTML 報告...")
    output_path = generate_html_report(result)

    print("\n" + "=" * 70)
    print("報告生成完成！")
    print("=" * 70)
    print(f"\n[OK] 報告位置：{output_path}")
    print("\n在瀏覽器中查看：")
    print("  file:///" + os.path.abspath(output_path).replace('\\', '/'))
    print("\n或執行：")
    print(f"  start {output_path}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

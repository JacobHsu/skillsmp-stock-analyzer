# 台股技術分析工具 - Taiwan Stock Technical Analyzer

自動化台股技術分析工具，使用 RSI、MACD、布林通道等指標進行股票分析與排名。

## 專案概述

本專案提供：
- **技術指標分析**: RSI、MACD、布林通道、移動平均線
- **股票比較排名**: 根據動能指標對多支股票進行排名
- **買賣訊號生成**: 基於技術指標提供交易建議
- **自動化報告**: 計劃整合 GitHub Actions 每日自動分析

**目前狀態**:
- ✅ 50 支台股清單（已驗證可用）
- ✅ 核心分析引擎完成
- ✅ 專案結構整理完畢
- 🚧 開發中: GitHub Actions 自動化工作流程

---

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 執行股票分析測試

```bash
# 完整 50 支股票比較測試
python tests/test_full_comparison.py
```

### 3. 使用分析器

```python
import sys
sys.path.append('scripts')
from main import StockAnalyzer
from stock_list import GIFT_STOCKS, STOCK_NAMES

# 建立分析器
analyzer = StockAnalyzer()

# 分析單支股票
result = analyzer.analyze("2330.TW", indicators=["RSI", "MACD"])
print(f"{STOCK_NAMES['2330.TW']}: {result['signal']['action']}")

# 比較多支股票並排名
comparison = analyzer.compare(
    GIFT_STOCKS[:10],  # 前 10 支股票
    rank_by="momentum",
    indicators=["RSI", "MACD"]
)

# 顯示排名結果
for stock in comparison['ranked_stocks']:
    ticker = stock['ticker']
    name = STOCK_NAMES[ticker]
    score = stock['score']
    print(f"#{stock['rank']} {ticker} {name} - 分數: {score:.2f}")
```

---

## 專案結構

```
skillsmp-stock-analyzer/
├── data/
│   ├── stocks.json                 # 股票清單配置檔 (50支台股)
│   └── gift_and_high_yield.csv     # 原始資料來源
│
├── scripts/
│   └── main.py                     # StockAnalyzer 核心分析器
│
├── tests/
│   └── test_full_comparison.py     # 完整股票比較測試
│
├── docs/                           # GitHub Pages 發布目錄
│   └── index.html                  # 每日自動更新的分析報告
│
├── archive/                        # 歷史開發檔案歸檔
│
├── SKILL.md                        # Claude Code 技能配置
├── SKILL_zh-TW.md                  # Claude Code 技能配置 (中文版)
├── stock_list.py                   # 股票清單載入模組
├── README.md                       # 專案說明文件
├── requirements.txt                # Python 依賴套件
└── .gitignore                      # Git 忽略規則
```

---

## 股票清單管理

### 當前股票清單

股票清單儲存在 `data/stocks.json`，包含 **50 支經過驗證的台股**。

查看完整清單：
```bash
python stock_list.py
```

### 修改股票清單

直接編輯 `data/stocks.json`:

```json
{
  "version": "1.0",
  "last_updated": "2025-12-31",
  "description": "台股清單 - 經過驗證的有效股票",
  "total": 50,
  "stocks": [
    {"ticker": "2330.TW", "name": "台積電"},
    {"ticker": "2454.TW", "name": "聯發科"},
    ...
  ]
}
```

**注意**:
- 台股代碼格式為 `XXXX.TW` (例如: `2330.TW`)
- 修改後重新執行程式即可自動載入新清單
- 建議使用 `stock_list.py` 驗證修改是否正確

### 股票清單模組使用

```python
from stock_list import (
    GIFT_STOCKS,      # 所有股票代碼列表
    STOCK_NAMES,      # 股票名稱對照字典
    TOP_20,           # 前 20 支股票
    TOP_10,           # 前 10 支股票
    get_stock_name,   # 取得股票名稱函數
    get_stock_count   # 取得股票總數函數
)

# 範例
print(f"總共 {get_stock_count()} 支股票")
print(f"台積電: {get_stock_name('2330.TW')}")
```

---

## 核心功能

### StockAnalyzer 類別

位於 `scripts/main.py`，提供以下主要方法：

#### 1. 分析單支股票
```python
analyzer = StockAnalyzer()
result = analyzer.analyze(
    ticker="2330.TW",
    indicators=["RSI", "MACD", "Bollinger"],
    period="3mo"
)

print(f"當前價格: {result['current_price']}")
print(f"RSI: {result['indicators']['RSI']['value']:.2f}")
print(f"建議: {result['signal']['action']}")
```

#### 2. 比較多支股票
```python
result = analyzer.compare(
    tickers=["2330.TW", "2454.TW", "2317.TW"],
    rank_by="momentum",
    indicators=["RSI", "MACD"]
)

for stock in result['ranked_stocks']:
    print(f"#{stock['rank']}: {stock['ticker']} - 分數 {stock['score']:.2f}")
```

### 技術指標

- **RSI (相對強弱指標)**: 判斷超買/超賣狀態
- **MACD (指數平滑異同移動平均線)**: 捕捉趨勢變化與買賣點
- **Bollinger Bands (布林通道)**: 判斷價格波動範圍
- **Moving Averages (移動平均線)**: 趨勢判斷

### 評分系統

技術分析評分規則：
- 基礎分數 = RSI - 50 (範圍: -50 ~ +50)
- MACD 黃金交叉: +25 分
- MACD 死亡交叉: -25 分
- MACD 多頭排列: +10 分
- MACD 空頭排列: -10 分

---

## 測試

### 完整股票比較測試

```bash
python tests/test_full_comparison.py
```

測試內容：
- 分析所有 50 支股票
- 按技術分數排名
- 顯示 Top 20 排名
- 列出買入/賣出訊號
- 統計市場概況

預期執行時間: 約 9-10 秒

---

## 🤖 GitHub Actions 自動化

### ✅ 已完成設定

專案已設定 GitHub Actions，每個**交易日上午 9:30**（台灣時間）自動執行股票分析。

#### 工作流程檔案
- `.github/workflows/daily-analysis.yml`

#### 執行時間
- **定時執行**: 週一至週五 9:30 (台灣時間)
- **手動觸發**: 可在 GitHub Actions 頁面手動執行

#### 自動化流程
1. 安裝 Python 環境與依賴套件
2. 執行股票分析 (`generate_report.py`)
3. 生成 HTML 報告到 `docs/index.html`
4. 自動提交並推送到 GitHub

---

## 🌐 GitHub Pages 部署

### 設定步驟

1. **前往 GitHub Repository 設定**
   ```
   Settings → Pages
   ```

2. **配置發布來源**
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **`/docs`**

3. **儲存設定**

   GitHub 會自動部署 `docs/index.html`

4. **訪問報告**
   ```
   https://<你的用戶名>.github.io/<repo-name>/
   ```

### 手動觸發 Workflow

在 GitHub 上：
```
Actions → 台股每日技術分析 → Run workflow
```

---

## 開發規劃

### ✅ 已完成

- [x] 報告生成器（HTML 雙欄布局）
- [x] GitHub Actions 自動化
- [x] 定時執行設定
- [x] GitHub Pages 準備

### 🚀 未來改進

- [ ] 加入更多技術指標（布林通道數值）
- [ ] 歷史報告保存
- [ ] 股價走勢圖表
- [ ] 行動裝置優化

---

## 技術棧

- **Python 3.8+**
- **yfinance**: 股票資料獲取
- **pandas**: 資料處理
- **numpy**: 數值計算
- **ta-lib** (可選): 進階技術指標

---

## 參考

[stock-analyzer](https://skillsmp.com/zh/skills/francyjglisboa-agent-skill-creator-references-examples-stock-analyzer-cskill-skill-md)

---

## 授權

MIT License

---

## 貢獻

歡迎提交 Issue 或 Pull Request！

如需協助或有任何問題，請在 GitHub Issues 中提出。

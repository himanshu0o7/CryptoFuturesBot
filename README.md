# 🪙 CryptoFuturesBot (Advanced Personal Trading Bot)

> ⚠️ **DISCLAIMER**  
> This bot is built for **personal use only**.  
> It is strictly prohibited to use this software for resale, public deployment, or any form of commercial activity.  
> Crypto trading carries financial risk. The author assumes **no responsibility** for any losses, misuse, or exchange policy violations.

---

## 📌 Overview

**CryptoFuturesBot** is a modular, automated **cryptocurrency futures trading bot** built for CoinSwitch users.  
Designed for private use, it supports real-time market analysis, SL/TP logic, portfolio management, and multi-asset rotation. A Streamlit dashboard and Telegram alerts provide full monitoring.

Advanced tools include optional OpenAI/Codeium assistant modules, a visual backtester, capital rebalancer, and live WebSocket integration.

---

## 🚀 Key Features

| Category                 | Description |
|--------------------------|-------------|
| ✅ Signal Engine         | Modular strategies using pandas-ta |
| ✅ SL/TP                 | Risk-based Stop Loss & Take Profit per trade |
| ✅ Multi-Timeframe Logic | Analyze 5m + 15m or 1h + 4h combos |
| ✅ Multi-Pair Rotation   | Trades across BTC/USDT, ETH/USDT, etc. |
| ✅ Leverage Config       | Customize leverage per pair |
| ✅ Capital Management    | Max % capital use per trade |
| ✅ Capital Rebalancer    | Reallocates unused or profit capital |
| ✅ PnL Tracking          | Per-trade profit/loss tracking |
| ✅ SL Hit % Tracker      | Measures strategy stop-loss rate |
| ✅ Portfolio Tracker     | Tracks balance, margin, exposure |
| ✅ Trade Logger          | Saves logs to SQLite and CSV |
| ✅ Telegram Alerts       | Entry, exit, SL/TP, PnL messages |
| ✅ Visual Dashboard      | Streamlit UI to view everything live |
| ✅ Visual Backtester     | Historical testing module with charts |
| ✅ WebSocket Feed        | Real-time CoinSwitch data (via SmartFeed) |
| ✅ AI Assistants         | GPT & Codeium for code and strategy help |

---

## 📁 Directory Structure

```bash
CryptoFuturesBot/
├── main.py                    # Core bot loop
├── main_runner.py             # Orchestration logic
├── streamlit_app.py           # Live dashboard
├── strategy/                  # Strategy modules
│   ├── ema_crossover.py
│   └── rsi_macd_combo.py
├── database/                  # Trade data storage
│   └── trades.db
├── backtester/                # Visual backtest UI
│   └── backtest_runner.py
├── websocket/                 # CoinSwitch live feed
│   └── coinswitch_ws.py
├── utils/
│   ├── capital_tracker.py
│   ├── capital_rebalancer.py
│   ├── pnl_logger.py
│   ├── portfolio_manager.py
│   └── risk_config.py
├── .env.sample                # Env vars template
├── run.sh / run_all.sh        # Execution scripts
├── openai_knowledge_tool.py   # Optional LLM Q&A
├── codeium_explain_module.py  # Optional code explainer
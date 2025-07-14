# CryptoFuturesBot - Advanced Cryptocurrency Trading Bot 🤖

A comprehensive, production-ready cryptocurrency futures trading bot with advanced risk management, real-time monitoring, and modular architecture.

> ⚠️ **DISCLAIMER**  
> This bot is built for **educational and personal use only**.  
> It is strictly prohibited to use this software for resale, public deployment, or any form of commercial activity.  
> Crypto trading carries financial risk. The author assumes **no responsibility** for any losses, misuse, or exchange policy violations.

---

## 🚀 Features

### Core Trading Features
- **Advanced Risk Management**: Stop-loss, take-profit, position sizing, drawdown limits
- **Multiple Trading Strategies**: Momentum-based and mean reversion strategies
- **Real-time Data Feeds**: WebSocket and REST API integration with Coinswitch
- **Portfolio Management**: Position tracking, PnL calculation, trade history
- **Order Management**: Market and limit orders with comprehensive status tracking

### Monitoring & Control
- **Web Dashboard**: Real-time Streamlit-based monitoring interface
- **Telegram Alerts**: Trade notifications, error alerts, status updates
- **Comprehensive Logging**: Structured logging with file rotation
- **Environment Validation**: Automated configuration and dependency checks

### Security & Safety
- **Dry Run Mode**: Complete simulation for testing without real funds
- **Environment Variables**: Secure API key management
- **Input Validation**: Comprehensive parameter validation and sanitization
- **Error Handling**: Robust error handling with automatic retry mechanisms

## 📁 Project Structure

```
CryptoFuturesBot/
├── utils/                          # Core utilities
│   ├── error_handler.py           # Retry mechanism & exception handling
│   ├── logging_setup.py           # Centralized logging system
│   ├── telegram_alert.py          # Notification system
│   ├── risk_management.py         # Advanced risk controls
│   ├── config_manager.py          # Configuration management
│   └── core_integration.py        # Legacy code integration
├── services/                       # Business logic services
│   ├── trade_executor.py          # Order placement & management
│   ├── data_feed.py               # Live data & WebSocket feeds
│   └── portfolio_manager.py       # Position tracking & PnL
├── strategies/                     # Trading strategies
│   ├── base_strategy.py           # Strategy framework
│   ├── simple_momentum.py         # Momentum-based trading
│   └── mean_reversion.py          # Mean reversion strategy
├── dashboard/                      # Web interface
│   └── streamlit_dashboard.py     # Real-time monitoring dashboard
├── part1_core/                     # Legacy Coinswitch utilities
├── main.py                         # Simple bot runner
├── enhanced_main.py                # Advanced bot runner with CLI
├── validate_environment.py        # Environment validation
└── .env.sample                     # Environment template
```

## 🛠️ Installation

### Prerequisites
- Python 3.12+
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/himanshu0o7/CryptoFuturesBot.git
   cd CryptoFuturesBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.sample .env
   # Edit .env with your API keys and configuration
   ```

4. **Validate setup**
   ```bash
   python validate_environment.py
   ```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Coinswitch API Configuration
COINSWITCH_API_KEY=your_coinswitch_api_key_here
COINSWITCH_API_SECRET=your_coinswitch_api_secret_here

# Telegram Bot Configuration (Optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Trading Configuration
DEFAULT_SYMBOL=BTCUSDT
DEFAULT_QUANTITY=10
RISK_PER_TRADE=0.01           # 1% risk per trade
STOP_LOSS_PERCENTAGE=0.02     # 2% stop loss
TAKE_PROFIT_PERCENTAGE=0.04   # 4% take profit

# Bot Configuration
DRY_RUN=true                  # Set to false for live trading
LOG_LEVEL=INFO
```

### Trading Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DEFAULT_SYMBOL` | BTCUSDT | Primary trading symbol |
| `DEFAULT_QUANTITY` | 10 | Default trade quantity |
| `RISK_PER_TRADE` | 0.01 | Risk percentage per trade (1%) |
| `STOP_LOSS_PERCENTAGE` | 0.02 | Stop loss percentage (2%) |
| `TAKE_PROFIT_PERCENTAGE` | 0.04 | Take profit percentage (4%) |
| `MAX_POSITION_SIZE` | 1000 | Maximum position size |

## 🚀 Usage

### Basic Usage

1. **Dry Run Mode (Recommended for testing)**
   ```bash
   python main.py
   ```

2. **Single Trading Cycle**
   ```bash
   python enhanced_main.py single
   ```

3. **Continuous Trading**
   ```bash
   python enhanced_main.py continuous --interval 30
   ```

### Advanced Usage

4. **Start Web Dashboard**
   ```bash
   python enhanced_main.py dashboard
   # Or directly:
   streamlit run dashboard/streamlit_dashboard.py
   ```

5. **Check Bot Status**
   ```bash
   python enhanced_main.py status
   ```

6. **Validate Environment**
   ```bash
   python enhanced_main.py validate
   ```

### Command Line Options

```bash
python enhanced_main.py <mode> [options]

Modes:
  single       Run one trading cycle
  continuous   Run continuously with intervals
  dashboard    Start web dashboard
  status       Show bot status
  validate     Validate environment setup

Options:
  --config, -c     Configuration file path
  --interval, -i   Interval in seconds for continuous mode (default: 30)
  --symbol, -s     Trading symbol (default: BTCUSDT)
  --dry-run        Force dry run mode
  --verbose, -v    Enable verbose logging
```

## 📊 Dashboard

The bot includes a comprehensive web dashboard built with Streamlit:

- **Real-time Portfolio Overview**: Value, PnL, positions
- **Trading Controls**: Start/stop bot, manual trading
- **Price Charts**: Interactive price charts with indicators
- **Position Management**: View and manage active positions
- **Trade History**: Complete trade log
- **Configuration**: Modify bot parameters
- **Live Logs**: Real-time bot logging

Access the dashboard at: `http://localhost:8501`

## 🔧 Trading Strategies

### 1. Simple Momentum Strategy
- **Logic**: Trades based on moving average crossovers and momentum
- **Parameters**:
  - Fast MA Period: 10
  - Slow MA Period: 30
  - Momentum Threshold: 2%

### 2. Mean Reversion Strategy
- **Logic**: Trades when price deviates significantly from mean
- **Parameters**:
  - Lookback Period: 20
  - Standard Deviation Threshold: 2.0
  - Mean Reversion Period: 10

### Adding Custom Strategies

1. Create a new strategy class inheriting from `BaseStrategy`
2. Implement `generate_signal()` and `validate_signal()` methods
3. Add to strategy manager in `enhanced_main.py`

```python
from strategies.base_strategy import BaseStrategy, TradingSignal, SignalType

class CustomStrategy(BaseStrategy):
    def generate_signal(self, market_context):
        # Your trading logic here
        return TradingSignal(...)
    
    def validate_signal(self, signal, market_context):
        # Validation logic
        return True
```

## 🛡️ Risk Management

The bot includes comprehensive risk management features:

- **Position Sizing**: Automatic calculation based on account balance and risk tolerance
- **Stop Loss**: Configurable percentage-based stop losses
- **Take Profit**: Automatic profit-taking at target levels
- **Daily Loss Limits**: Maximum daily loss protection
- **Drawdown Protection**: Maximum portfolio drawdown limits
- **Volatility Adjustment**: Dynamic stop losses based on market volatility

## 📱 Notifications

Configure Telegram alerts to receive:
- Trade execution notifications
- Error alerts and warnings
- Bot status updates
- PnL updates
- System health notifications

## 🔍 Monitoring & Logging

### Logging Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General information and trade executions
- **WARNING**: Warning messages and potential issues
- **ERROR**: Error conditions and failures

### Log Files
- Location: `logs/cryptobot.log`
- Rotation: 10MB files, 5 backups
- Format: Timestamp, module, level, message

## 🧪 Testing

### Environment Validation
```bash
python validate_environment.py
```

This comprehensive validation checks:
- Environment variables configuration
- Module imports and dependencies
- Basic functionality testing
- Numeric parameter validation

### Dry Run Testing
Always test new configurations in dry run mode:
```bash
DRY_RUN=true python main.py
```

## ⚠️ Safety & Disclaimer

### Important Safety Notes
1. **Always test in dry run mode first**
2. **Start with small position sizes**
3. **Monitor the bot regularly**
4. **Keep API keys secure**
5. **Understand the risks of automated trading**

### Risk Disclaimer
Cryptocurrency trading involves significant risk. This bot is provided for educational purposes. Users are responsible for:
- Understanding the trading strategies
- Setting appropriate risk parameters
- Monitoring bot performance
- Compliance with local regulations

**Never invest more than you can afford to lose.**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Review the validation output for configuration problems
- Check logs for error details

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Coinswitch API for trading functionality
- Streamlit for the dashboard framework
- Python trading community for inspiration

---

**Happy Trading! 🚀📈**

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
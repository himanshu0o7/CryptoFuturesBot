import os
import time
from dotenv import load_dotenv

from utils.risk_management import RiskManager
from utils.telegram_alert import send_telegram_alert
from utils.error_handler import retry
from utils.logging_setup import setup_logger
from services.data_feed import LiveDataFeed, MockDataFeed
from services.trade_executor import TradeExecutor, MockTradeExecutor
from services.portfolio_manager import PortfolioManager

# ==== Load Environment ====
load_dotenv()

# Setup logging
logger = setup_logger("CryptoFuturesBot", level=os.getenv("LOG_LEVEL", "INFO"))

# Configuration
API_KEY = os.getenv("COINSWITCH_API_KEY")
API_SECRET = os.getenv("COINSWITCH_API_SECRET")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTCUSDT")
DEFAULT_QUANTITY = float(os.getenv("DEFAULT_QUANTITY", "10"))

# ==== Initialize Services ====
def initialize_services():
    """Initialize all bot services"""
    try:
        # Initialize data feed
        if DRY_RUN:
            data_feed = MockDataFeed()
            logger.info("Using mock data feed (DRY RUN mode)")
        else:
            data_feed = LiveDataFeed()
            logger.info("Using live data feed")
        
        # Initialize trade executor
        if DRY_RUN:
            trade_executor = MockTradeExecutor()
            logger.info("Using mock trade executor (DRY RUN mode)")
        else:
            trade_executor = TradeExecutor(dry_run=False)
            logger.info("Using live trade executor")
        
        # Initialize portfolio manager
        portfolio_manager = PortfolioManager()
        
        # Initialize risk manager
        risk_manager = RiskManager(
            sl_pct=float(os.getenv("STOP_LOSS_PERCENTAGE", "0.02")),
            tp_pct=float(os.getenv("TAKE_PROFIT_PERCENTAGE", "0.04")),
            max_position_size=float(os.getenv("MAX_POSITION_SIZE", "1000"))
        )
        
        return {
            'data_feed': data_feed,
            'trade_executor': trade_executor,
            'portfolio_manager': portfolio_manager,
            'risk_manager': risk_manager
        }
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

# ==== Price Fetch ====
def get_live_price(data_feed, symbol=DEFAULT_SYMBOL):
    """Get live price using data feed service"""
    try:
        price = data_feed.get_live_price(symbol)
        if price:
            return float(price)
        else:
            logger.error(f"Failed to get price for {symbol}")
            return None
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return None

# ==== Order Placement ====
def place_order(trade_executor, symbol, qty, side="BUY"):
    """Place order using trade executor service"""
    try:
        from services.trade_executor import OrderRequest, OrderType
        
        order_request = OrderRequest(
            symbol=symbol,
            side=side,
            quantity=qty,
            order_type=OrderType.MARKET
        )
        
        response = trade_executor.place_order(order_request)
        if response:
            logger.info(f"Order placed: {response.order_id}")
            return {"status": "success", "order_id": response.order_id}
        else:
            logger.error("Order placement failed")
            return {"status": "error", "order_id": None}
            
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        return {"status": "error", "order_id": None}

# ==== Main Bot Logic ====
def run_bot():
    """Main bot execution function"""
    try:
        logger.info("🚀 CryptoFuturesBot Starting...")
        
        # Check environment variables
        if not API_KEY or API_KEY == "your_coinswitch_api_key_here":
            logger.warning("⚠️  Coinswitch API key not configured. Running in simulation mode.")
        
        # Send startup alert
        send_telegram_alert("🟢 CryptoFuturesBot started.")
        
        # Initialize services
        services = initialize_services()
        data_feed = services['data_feed']
        trade_executor = services['trade_executor']
        portfolio_manager = services['portfolio_manager']
        risk_manager = services['risk_manager']
        
        symbol = DEFAULT_SYMBOL
        qty = DEFAULT_QUANTITY
        
        # Fetch entry price
        logger.info(f"Fetching entry price for {symbol}")
        entry_price = retry(lambda: get_live_price(data_feed, symbol), label="Fetch Entry Price")
        
        if not entry_price:
            logger.error("Failed to fetch entry price")
            return
        
        logger.info(f"✅ Entry price: ₹{entry_price:,.2f}")
        
        # Calculate position size using risk management
        account_balance = 10000.0  # This should come from actual account balance
        position_size = risk_manager.calculate_position_size(
            account_balance=account_balance,
            risk_per_trade=float(os.getenv("RISK_PER_TRADE", "0.01")),
            entry_price=entry_price
        )
        
        logger.info(f"Calculated position size: {position_size:.2f}")
        
        # Place order
        order = retry(lambda: place_order(trade_executor, symbol, qty, "BUY"), label="Place Order")
        
        if order["status"] == "success":
            logger.info(f"📦 Order Placed: {order['order_id']}")
            
            # Add trade to portfolio
            portfolio_manager.add_trade(
                symbol=symbol,
                side="BUY",
                quantity=qty,
                price=entry_price,
                order_id=order['order_id']
            )
        else:
            logger.error("Order placement failed")
            return
        
        # Simulate holding period
        time.sleep(5)
        
        # Check current price and risk management
        current_price = retry(lambda: get_live_price(data_feed, symbol), label="Fetch Exit Price")
        
        if current_price:
            logger.info(f"📈 Current price: ₹{current_price:,.2f}")
            
            # Update portfolio with current price
            portfolio_manager.update_position(symbol, current_price)
            
            # Check risk management
            decision = risk_manager.should_exit(entry_price, current_price)
            
            if decision:
                msg = f"🔔 {decision} Triggered!\n{symbol} moved ₹{entry_price:,.2f} → ₹{current_price:,.2f}"
                logger.info(msg)
                send_telegram_alert(msg)
                
                # Close position
                close_order = place_order(trade_executor, symbol, qty, "SELL")
                if close_order["status"] == "success":
                    logger.info(f"Position closed: {close_order['order_id']}")
                    portfolio_manager.close_position(symbol, current_price)
            else:
                logger.info("🟡 HOLD — SL/TP not yet triggered.")
                send_telegram_alert(f"ℹ️ {symbol} HOLD — ₹{entry_price:,.2f} → ₹{current_price:,.2f}")
        
        # Send portfolio update
        portfolio_manager.send_portfolio_update()
        
        # Get portfolio stats
        stats = portfolio_manager.calculate_portfolio_stats()
        logger.info(f"Portfolio Value: ₹{stats.total_value:,.2f}, Total PnL: ₹{stats.total_pnl:,.2f}")
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        error_msg = f"Bot terminated: {e}"
        logger.error(error_msg)
        send_telegram_alert(f"❌ CryptoFuturesBot crashed:\n{e}")

if __name__ == "__main__":
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        print(f"❌ Critical error: {e}")
        print("Check logs for more details.")

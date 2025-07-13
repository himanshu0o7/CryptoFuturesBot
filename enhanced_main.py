"""
Enhanced main runner for CryptoFuturesBot
Provides multiple execution modes and comprehensive bot management
"""

import sys
import argparse
import asyncio
from typing import Dict, Any, Optional

from utils.config_manager import get_config
from utils.logging_setup import setup_logger
from utils.telegram_alert import send_bot_status
from utils.error_handler import handle_exceptions
from utils.core_integration import get_core_integrator

from services.trade_executor import TradeExecutor, MockTradeExecutor
from services.data_feed import LiveDataFeed, MockDataFeed
from services.portfolio_manager import PortfolioManager
from strategies.base_strategy import StrategyManager
from strategies.simple_momentum import SimpleMomentumStrategy
from strategies.mean_reversion import MeanReversionStrategy


class CryptoFuturesBot:
    """Main bot class with comprehensive functionality"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize the bot with configuration"""
        self.config = get_config()
        self.logger = setup_logger("CryptoFuturesBot", level=self.config.system_config.log_level)
        
        # Bot state
        self.running = False
        self.services = {}
        self.strategy_manager = None
        
        # Initialize components
        self._initialize_services()
        self._initialize_strategies()
    
    @handle_exceptions()
    def _initialize_services(self):
        """Initialize all bot services"""
        try:
            # Data feed service
            if self.config.trading_config.dry_run:
                self.services['data_feed'] = MockDataFeed()
                self.logger.info("Initialized mock data feed (dry run mode)")
            else:
                self.services['data_feed'] = LiveDataFeed(
                    api_base_url=self.config.api_config.coinswitch_base_url
                )
                self.logger.info("Initialized live data feed")
            
            # Trade executor service
            if self.config.trading_config.dry_run:
                self.services['trade_executor'] = MockTradeExecutor()
                self.logger.info("Initialized mock trade executor (dry run mode)")
            else:
                self.services['trade_executor'] = TradeExecutor(dry_run=False)
                self.logger.info("Initialized live trade executor")
            
            # Portfolio manager
            self.services['portfolio_manager'] = PortfolioManager()
            self.logger.info("Initialized portfolio manager")
            
            # Core integration
            core_integrator = get_core_integrator()
            self.services['core_integrator'] = core_integrator
            self.logger.info("Initialized core module integration")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize services: {e}")
            raise
    
    @handle_exceptions()
    def _initialize_strategies(self):
        """Initialize trading strategies"""
        try:
            self.strategy_manager = StrategyManager()
            
            # Add momentum strategy
            momentum_strategy = SimpleMomentumStrategy({
                'stop_loss_pct': self.config.trading_config.stop_loss_pct,
                'take_profit_pct': self.config.trading_config.take_profit_pct
            })
            self.strategy_manager.add_strategy(momentum_strategy)
            
            # Add mean reversion strategy  
            mean_reversion_strategy = MeanReversionStrategy({
                'stop_loss_pct': self.config.trading_config.stop_loss_pct,
                'take_profit_pct': self.config.trading_config.take_profit_pct
            })
            self.strategy_manager.add_strategy(mean_reversion_strategy)
            
            self.logger.info("Initialized trading strategies")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize strategies: {e}")
            raise
    
    @handle_exceptions()
    async def start(self):
        """Start the bot"""
        try:
            self.logger.info("🚀 Starting CryptoFuturesBot...")
            
            # Validate configuration
            validation = self.config.validate_config()
            if not validation['valid']:
                self.logger.error("Configuration validation failed:")
                for error in validation['errors']:
                    self.logger.error(f"  - {error}")
                return False
            
            # Send startup notification
            send_bot_status("STARTED", "CryptoFuturesBot is starting up")
            
            self.running = True
            
            # Start data feed if using WebSocket
            data_feed = self.services['data_feed']
            if hasattr(data_feed, 'start_websocket') and not self.config.trading_config.dry_run:
                data_feed.start_websocket()
            
            self.logger.info("✅ Bot started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            return False
    
    @handle_exceptions()
    async def stop(self):
        """Stop the bot"""
        try:
            self.logger.info("⏹️ Stopping CryptoFuturesBot...")
            
            self.running = False
            
            # Stop data feed
            data_feed = self.services['data_feed']
            if hasattr(data_feed, 'stop_websocket'):
                data_feed.stop_websocket()
            
            # Send shutdown notification
            send_bot_status("STOPPED", "CryptoFuturesBot has been stopped")
            
            self.logger.info("✅ Bot stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")
    
    @handle_exceptions()
    async def run_single_cycle(self) -> bool:
        """Run a single trading cycle"""
        try:
            symbol = self.config.trading_config.default_symbol
            
            # Get market data
            data_feed = self.services['data_feed']
            market_data = data_feed.get_market_data(symbol)
            
            if not market_data:
                self.logger.warning(f"Could not get market data for {symbol}")
                return False
            
            # Update portfolio positions
            portfolio_manager = self.services['portfolio_manager']
            portfolio_manager.update_position(symbol, market_data.price)
            
            # Generate trading signals (if strategies are enabled)
            from strategies.base_strategy import MarketContext
            
            market_context = MarketContext(
                symbol=symbol,
                current_price=market_data.price,
                volume=market_data.volume,
                price_history=[market_data.price],  # In real implementation, maintain history
                indicators={},
                timestamp=str(market_data.timestamp)
            )
            
            signals = self.strategy_manager.generate_signals(market_context)
            
            if signals:
                self.logger.info(f"Generated {len(signals)} trading signals")
                
                # Execute signals
                trade_executor = self.services['trade_executor']
                for signal in signals:
                    # Execute the signal
                    from services.trade_executor import OrderRequest, OrderType
                    
                    order_request = OrderRequest(
                        symbol=signal.symbol,
                        side=signal.signal_type.value,
                        quantity=self.config.trading_config.default_quantity,
                        order_type=OrderType.MARKET,
                        price=signal.price
                    )
                    
                    response = trade_executor.place_order(order_request)
                    if response:
                        self.logger.info(f"Executed signal: {signal.signal_type.value} {signal.symbol}")
                        
                        # Add to portfolio
                        portfolio_manager.add_trade(
                            symbol=signal.symbol,
                            side=signal.signal_type.value,
                            quantity=self.config.trading_config.default_quantity,
                            price=signal.price or market_data.price,
                            order_id=response.order_id
                        )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in trading cycle: {e}")
            return False
    
    @handle_exceptions()
    async def run_continuous(self, cycle_interval: int = 30):
        """Run bot continuously with specified interval"""
        try:
            self.logger.info(f"Running continuously with {cycle_interval}s intervals")
            
            while self.running:
                cycle_success = await self.run_single_cycle()
                
                if not cycle_success:
                    self.logger.warning("Trading cycle failed, continuing...")
                
                # Wait for next cycle
                await asyncio.sleep(cycle_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
        except Exception as e:
            self.logger.error(f"Error in continuous run: {e}")
        finally:
            await self.stop()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bot status"""
        try:
            portfolio_manager = self.services['portfolio_manager']
            stats = portfolio_manager.calculate_portfolio_stats()
            
            return {
                'running': self.running,
                'config': self.config.get_config_summary(),
                'portfolio': {
                    'total_value': stats.total_value,
                    'total_pnl': stats.total_pnl,
                    'positions_count': stats.positions_count,
                    'win_rate': stats.win_rate
                },
                'strategies': self.strategy_manager.get_strategy_performance() if self.strategy_manager else {}
            }
            
        except Exception as e:
            self.logger.error(f"Error getting bot status: {e}")
            return {'running': self.running, 'error': str(e)}


# Command-line interface
@handle_exceptions()
def main():
    """Main entry point with command-line interface"""
    parser = argparse.ArgumentParser(description='CryptoFuturesBot - Advanced Cryptocurrency Trading Bot')
    
    parser.add_argument('mode', choices=['single', 'continuous', 'validate', 'dashboard', 'status'],
                       help='Bot execution mode')
    parser.add_argument('--config', '-c', type=str, help='Configuration file path')
    parser.add_argument('--interval', '-i', type=int, default=30, 
                       help='Interval in seconds for continuous mode (default: 30)')
    parser.add_argument('--symbol', '-s', type=str, default='BTCUSDT',
                       help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Force dry run mode')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = setup_logger("CryptoFuturesBot", level=log_level)
    
    try:
        if args.mode == 'validate':
            # Run validation
            from validate_environment import main as validate_main
            success = validate_main()
            sys.exit(0 if success else 1)
            
        elif args.mode == 'dashboard':
            # Start dashboard
            import subprocess
            import os
            
            dashboard_path = os.path.join("dashboard", "streamlit_dashboard.py")
            logger.info("Starting Streamlit dashboard...")
            subprocess.run(["streamlit", "run", dashboard_path])
            
        elif args.mode == 'status':
            # Show bot status
            bot = CryptoFuturesBot(args.config)
            status = bot.get_status()
            
            print("\n🤖 CryptoFuturesBot Status")
            print("=" * 40)
            print(f"Running: {'✅' if status['running'] else '❌'}")
            print(f"Mode: {'Live' if not status['config']['trading']['dry_run'] else 'Dry Run'}")
            print(f"Portfolio Value: ₹{status['portfolio']['total_value']:,.2f}")
            print(f"Total P&L: ₹{status['portfolio']['total_pnl']:,.2f}")
            print(f"Active Positions: {status['portfolio']['positions_count']}")
            print(f"Win Rate: {status['portfolio']['win_rate']:.1f}%")
            
        else:
            # Initialize bot
            bot = CryptoFuturesBot(args.config)
            
            # Override config if needed
            if args.dry_run:
                bot.config.trading_config.dry_run = True
            
            # Run the bot
            if args.mode == 'single':
                async def run_single():
                    await bot.start()
                    success = await bot.run_single_cycle()
                    await bot.stop()
                    return success
                
                success = asyncio.run(run_single())
                logger.info(f"Single cycle {'completed successfully' if success else 'failed'}")
                
            elif args.mode == 'continuous':
                async def run_continuous():
                    await bot.start()
                    await bot.run_continuous(args.interval)
                
                asyncio.run(run_continuous())
    
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
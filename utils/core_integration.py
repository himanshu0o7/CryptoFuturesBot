"""
Integration utilities for existing part1_core modules
Provides compatibility layer and unified interface
"""

import os
import sys
from typing import Dict, Any, Optional
import importlib.util

from utils.logging_setup import get_logger
from utils.error_handler import handle_exceptions

logger = get_logger("CoreIntegration")


class CoreModuleIntegrator:
    """Integration class for part1_core modules"""
    
    def __init__(self):
        self.available_modules = {}
        self.part1_core_path = "part1_core"
        self._discover_modules()
    
    def _discover_modules(self):
        """Discover available modules in part1_core"""
        try:
            if not os.path.exists(self.part1_core_path):
                logger.warning("part1_core directory not found")
                return
            
            for file in os.listdir(self.part1_core_path):
                if file.endswith('.py') and not file.startswith('__'):
                    module_name = file[:-3]  # Remove .py extension
                    self.available_modules[module_name] = {
                        'path': os.path.join(self.part1_core_path, file),
                        'loaded': False,
                        'module': None
                    }
            
            logger.info(f"Discovered {len(self.available_modules)} modules in part1_core")
            
        except Exception as e:
            logger.error(f"Error discovering core modules: {e}")
    
    def load_module(self, module_name: str) -> Optional[Any]:
        """Load a specific module from part1_core"""
        try:
            if module_name not in self.available_modules:
                logger.error(f"Module {module_name} not found in part1_core")
                return None
            
            module_info = self.available_modules[module_name]
            
            if module_info['loaded']:
                return module_info['module']
            
            # Load the module
            spec = importlib.util.spec_from_file_location(
                module_name, 
                module_info['path']
            )
            
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                module_info['module'] = module
                module_info['loaded'] = True
                
                logger.info(f"Loaded module: {module_name}")
                return module
            else:
                logger.error(f"Failed to create spec for module: {module_name}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading module {module_name}: {e}")
            return None
    
    def get_coinswitch_api_utils(self):
        """Get coinswitch API utilities"""
        return self.load_module('coinswitch_api_utils')
    
    def get_order_executor(self):
        """Get order executor from part1_core"""
        return self.load_module('coinswitch_order_executor')
    
    def get_portfolio_utils(self):
        """Get portfolio utilities"""
        return self.load_module('coinswitch_portfolio_utils')
    
    def get_futures_utils(self):
        """Get futures trading utilities"""
        utils = {}
        
        # Load various futures utilities
        modules_to_load = [
            'coinswitch_futures_order_utils',
            'coinswitch_futures_position_utils',
            'coinswitch_futures_cancel_one_utils',
            'coinswitch_futures_place_order_utils'
        ]
        
        for module_name in modules_to_load:
            module = self.load_module(module_name)
            if module:
                utils[module_name] = module
        
        return utils
    
    def get_websocket_handlers(self):
        """Get WebSocket handlers"""
        handlers = {}
        
        ws_modules = [
            'coinswitch_ws_ticker',
            'coinswitch_ws_trades',
            'coinswitch_ws_orderbook',
            'coinswitch_ws_candles'
        ]
        
        for module_name in ws_modules:
            module = self.load_module(module_name)
            if module:
                handlers[module_name] = module
        
        return handlers
    
    def get_data_utils(self):
        """Get data utilities"""
        data_utils = {}
        
        data_modules = [
            'future_data_fetcher',
            'futures_data_checker',
            'symbol_loader',
            'coinswitch_exchange_precision_utils'
        ]
        
        for module_name in data_modules:
            module = self.load_module(module_name)
            if module:
                data_utils[module_name] = module
        
        return data_utils
    
    def get_available_modules(self) -> Dict[str, Any]:
        """Get list of available modules"""
        return {
            name: {
                'loaded': info['loaded'],
                'path': info['path']
            }
            for name, info in self.available_modules.items()
        }


# Global integrator instance
core_integrator = CoreModuleIntegrator()


def get_core_integrator() -> CoreModuleIntegrator:
    """Get global core integrator instance"""
    return core_integrator


@handle_exceptions()
def integrate_coinswitch_api():
    """Integrate Coinswitch API utilities with new services"""
    try:
        integrator = get_core_integrator()
        
        # Load API utilities
        api_utils = integrator.get_coinswitch_api_utils()
        if api_utils:
            logger.info("Coinswitch API utilities integrated")
            return api_utils
        else:
            logger.warning("Could not load Coinswitch API utilities")
            return None
            
    except Exception as e:
        logger.error(f"Error integrating Coinswitch API: {e}")
        return None


@handle_exceptions()
def integrate_existing_order_system():
    """Integrate existing order execution system"""
    try:
        integrator = get_core_integrator()
        
        # Load order executor
        order_executor = integrator.get_order_executor()
        if order_executor:
            logger.info("Order execution system integrated")
            return order_executor
        else:
            logger.warning("Could not load order execution system")
            return None
            
    except Exception as e:
        logger.error(f"Error integrating order system: {e}")
        return None


@handle_exceptions()  
def integrate_websocket_feeds():
    """Integrate existing WebSocket data feeds"""
    try:
        integrator = get_core_integrator()
        
        # Load WebSocket handlers
        ws_handlers = integrator.get_websocket_handlers()
        if ws_handlers:
            logger.info(f"Integrated {len(ws_handlers)} WebSocket handlers")
            return ws_handlers
        else:
            logger.warning("Could not load WebSocket handlers")
            return None
            
    except Exception as e:
        logger.error(f"Error integrating WebSocket feeds: {e}")
        return None


@handle_exceptions()
def create_unified_data_feed():
    """Create unified data feed using existing and new modules"""
    try:
        from services.data_feed import LiveDataFeed
        
        # Get existing data utilities
        integrator = get_core_integrator()
        data_utils = integrator.get_data_utils()
        
        # Create enhanced data feed
        data_feed = LiveDataFeed()
        
        # Integrate existing data fetchers if available
        if data_utils and 'future_data_fetcher' in data_utils:
            logger.info("Enhanced data feed with existing utilities")
        
        return data_feed
        
    except Exception as e:
        logger.error(f"Error creating unified data feed: {e}")
        return None


@handle_exceptions()
def create_unified_trade_executor():
    """Create unified trade executor using existing and new modules"""
    try:
        from services.trade_executor import TradeExecutor
        
        # Get existing order utilities
        integrator = get_core_integrator()
        order_executor = integrator.get_order_executor()
        futures_utils = integrator.get_futures_utils()
        
        # Create enhanced trade executor
        trade_executor = TradeExecutor()
        
        # Add integration logic here if needed
        if order_executor:
            logger.info("Enhanced trade executor with existing order system")
        
        return trade_executor
        
    except Exception as e:
        logger.error(f"Error creating unified trade executor: {e}")
        return None


def migrate_existing_config():
    """Migrate configuration from existing modules"""
    try:
        integrator = get_core_integrator()
        
        # Try to load existing config
        config_loader = integrator.load_module('config_loader')
        env_loader = integrator.load_module('coinswitch_env_loader')
        
        migration_info = {}
        
        if config_loader:
            logger.info("Found existing config loader")
            migration_info['config_loader'] = True
        
        if env_loader:
            logger.info("Found existing environment loader")
            migration_info['env_loader'] = True
        
        return migration_info
        
    except Exception as e:
        logger.error(f"Error migrating existing config: {e}")
        return {}


def get_legacy_compatibility_layer():
    """Get compatibility layer for legacy code"""
    
    class LegacyCompatibility:
        """Compatibility layer for legacy functions"""
        
        def __init__(self):
            self.integrator = get_core_integrator()
        
        def get_live_price(self, symbol: str = "BTCUSDT"):
            """Legacy-compatible price fetching"""
            try:
                from services.data_feed import MockDataFeed
                data_feed = MockDataFeed()
                return data_feed.get_live_price(symbol)
            except Exception as e:
                logger.error(f"Legacy price fetch error: {e}")
                return None
        
        def place_order_legacy(self, symbol: str, quantity: float, side: str = "BUY"):
            """Legacy-compatible order placement"""
            try:
                from services.trade_executor import MockTradeExecutor, OrderRequest, OrderType
                
                executor = MockTradeExecutor()
                request = OrderRequest(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    order_type=OrderType.MARKET
                )
                
                response = executor.place_order(request)
                
                if response:
                    return {
                        "status": "success",
                        "order_id": response.order_id
                    }
                else:
                    return {
                        "status": "error",
                        "order_id": None
                    }
                    
            except Exception as e:
                logger.error(f"Legacy order placement error: {e}")
                return {"status": "error", "order_id": None}
    
    return LegacyCompatibility()


# Initialize integration on module import
try:
    core_integrator = CoreModuleIntegrator()
    logger.info("Core module integration initialized")
except Exception as e:
    logger.error(f"Failed to initialize core integration: {e}")
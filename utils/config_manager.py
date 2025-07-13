"""
Configuration management utility for CryptoFuturesBot
Handles environment configuration and validation
"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

from utils.logging_setup import get_logger

logger = get_logger("ConfigManager")


@dataclass
class TradingConfig:
    """Trading configuration parameters"""
    default_symbol: str = "BTCUSDT"
    default_quantity: float = 10.0
    risk_per_trade: float = 0.01
    stop_loss_pct: float = 0.02
    take_profit_pct: float = 0.04
    max_position_size: float = 1000.0
    dry_run: bool = True


@dataclass
class APIConfig:
    """API configuration parameters"""
    coinswitch_api_key: str = ""
    coinswitch_api_secret: str = ""
    coinswitch_base_url: str = "https://api.coinswitch.co"
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    google_api_key: str = ""


@dataclass
class SystemConfig:
    """System configuration parameters"""
    log_level: str = "INFO"
    log_file_path: str = "logs/cryptobot.log"
    timezone: str = "UTC"
    enable_telegram_alerts: bool = True
    enable_logging: bool = True
    database_url: str = "sqlite:///cryptobot.db"


class ConfigManager:
    """Configuration management class"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_file: Optional config file path
        """
        self.config_file = config_file
        self.trading_config = TradingConfig()
        self.api_config = APIConfig()
        self.system_config = SystemConfig()
        
        # Load configuration
        self._load_environment()
        if config_file and os.path.exists(config_file):
            self._load_config_file(config_file)
    
    def _load_environment(self):
        """Load configuration from environment variables"""
        try:
            load_dotenv()
            
            # API Configuration
            self.api_config.coinswitch_api_key = os.getenv("COINSWITCH_API_KEY", "")
            self.api_config.coinswitch_api_secret = os.getenv("COINSWITCH_API_SECRET", "")
            self.api_config.coinswitch_base_url = os.getenv("COINSWITCH_BASE_URL", "https://api.coinswitch.co")
            self.api_config.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
            self.api_config.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
            self.api_config.google_api_key = os.getenv("GOOGLE_API_KEY", "")
            
            # Trading Configuration
            self.trading_config.default_symbol = os.getenv("DEFAULT_SYMBOL", "BTCUSDT")
            self.trading_config.default_quantity = float(os.getenv("DEFAULT_QUANTITY", "10.0"))
            self.trading_config.risk_per_trade = float(os.getenv("RISK_PER_TRADE", "0.01"))
            self.trading_config.stop_loss_pct = float(os.getenv("STOP_LOSS_PERCENTAGE", "0.02"))
            self.trading_config.take_profit_pct = float(os.getenv("TAKE_PROFIT_PERCENTAGE", "0.04"))
            self.trading_config.max_position_size = float(os.getenv("MAX_POSITION_SIZE", "1000.0"))
            self.trading_config.dry_run = os.getenv("DRY_RUN", "true").lower() == "true"
            
            # System Configuration
            self.system_config.log_level = os.getenv("LOG_LEVEL", "INFO")
            self.system_config.log_file_path = os.getenv("LOG_FILE_PATH", "logs/cryptobot.log")
            self.system_config.timezone = os.getenv("TIMEZONE", "UTC")
            self.system_config.enable_telegram_alerts = os.getenv("ENABLE_TELEGRAM_ALERTS", "true").lower() == "true"
            self.system_config.enable_logging = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
            self.system_config.database_url = os.getenv("DATABASE_URL", "sqlite:///cryptobot.db")
            
            logger.info("Configuration loaded from environment variables")
            
        except Exception as e:
            logger.error(f"Error loading environment configuration: {e}")
    
    def _load_config_file(self, config_file: str):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            # Update configurations from file
            if 'trading' in config_data:
                trading_data = config_data['trading']
                for key, value in trading_data.items():
                    if hasattr(self.trading_config, key):
                        setattr(self.trading_config, key, value)
            
            if 'api' in config_data:
                api_data = config_data['api']
                for key, value in api_data.items():
                    if hasattr(self.api_config, key):
                        setattr(self.api_config, key, value)
            
            if 'system' in config_data:
                system_data = config_data['system']
                for key, value in system_data.items():
                    if hasattr(self.system_config, key):
                        setattr(self.system_config, key, value)
            
            logger.info(f"Configuration loaded from file: {config_file}")
            
        except Exception as e:
            logger.error(f"Error loading config file {config_file}: {e}")
    
    def save_config_file(self, config_file: Optional[str] = None) -> bool:
        """Save current configuration to JSON file"""
        try:
            file_path = config_file or self.config_file or "config.json"
            
            config_data = {
                'trading': {
                    'default_symbol': self.trading_config.default_symbol,
                    'default_quantity': self.trading_config.default_quantity,
                    'risk_per_trade': self.trading_config.risk_per_trade,
                    'stop_loss_pct': self.trading_config.stop_loss_pct,
                    'take_profit_pct': self.trading_config.take_profit_pct,
                    'max_position_size': self.trading_config.max_position_size,
                    'dry_run': self.trading_config.dry_run
                },
                'system': {
                    'log_level': self.system_config.log_level,
                    'log_file_path': self.system_config.log_file_path,
                    'timezone': self.system_config.timezone,
                    'enable_telegram_alerts': self.system_config.enable_telegram_alerts,
                    'enable_logging': self.system_config.enable_logging,
                    'database_url': self.system_config.database_url
                }
                # Note: API config not saved for security reasons
            }
            
            with open(file_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info(f"Configuration saved to: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving config file: {e}")
            return False
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate current configuration and return validation results"""
        validation = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validate API configuration
        if not self.api_config.coinswitch_api_key and not self.trading_config.dry_run:
            validation['errors'].append("Coinswitch API key required for live trading")
            validation['valid'] = False
        
        if not self.api_config.coinswitch_api_secret and not self.trading_config.dry_run:
            validation['errors'].append("Coinswitch API secret required for live trading")
            validation['valid'] = False
        
        if not self.api_config.telegram_bot_token:
            validation['warnings'].append("Telegram bot token not configured - alerts disabled")
        
        # Validate trading configuration
        if self.trading_config.default_quantity <= 0:
            validation['errors'].append("Default quantity must be positive")
            validation['valid'] = False
        
        if not (0 < self.trading_config.risk_per_trade <= 0.1):
            validation['errors'].append("Risk per trade should be between 0% and 10%")
            validation['valid'] = False
        
        if not (0 < self.trading_config.stop_loss_pct <= 0.2):
            validation['errors'].append("Stop loss percentage should be between 0% and 20%")
            validation['valid'] = False
        
        if not (0 < self.trading_config.take_profit_pct <= 0.5):
            validation['errors'].append("Take profit percentage should be between 0% and 50%")
            validation['valid'] = False
        
        # Validate system configuration
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.system_config.log_level not in valid_log_levels:
            validation['warnings'].append(f"Invalid log level: {self.system_config.log_level}")
        
        return validation
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration"""
        return {
            'trading': {
                'symbol': self.trading_config.default_symbol,
                'quantity': self.trading_config.default_quantity,
                'dry_run': self.trading_config.dry_run,
                'risk_per_trade': f"{self.trading_config.risk_per_trade * 100:.1f}%",
                'stop_loss': f"{self.trading_config.stop_loss_pct * 100:.1f}%",
                'take_profit': f"{self.trading_config.take_profit_pct * 100:.1f}%"
            },
            'api': {
                'coinswitch_configured': bool(self.api_config.coinswitch_api_key),
                'telegram_configured': bool(self.api_config.telegram_bot_token),
                'google_configured': bool(self.api_config.google_api_key)
            },
            'system': {
                'log_level': self.system_config.log_level,
                'alerts_enabled': self.system_config.enable_telegram_alerts,
                'logging_enabled': self.system_config.enable_logging
            }
        }
    
    def update_trading_config(self, **kwargs):
        """Update trading configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.trading_config, key):
                setattr(self.trading_config, key, value)
                logger.info(f"Updated trading config: {key} = {value}")
    
    def update_system_config(self, **kwargs):
        """Update system configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.system_config, key):
                setattr(self.system_config, key, value)
                logger.info(f"Updated system config: {key} = {value}")
    
    def is_live_trading_enabled(self) -> bool:
        """Check if live trading is enabled and properly configured"""
        return (not self.trading_config.dry_run and 
                bool(self.api_config.coinswitch_api_key) and 
                bool(self.api_config.coinswitch_api_secret))
    
    def is_telegram_enabled(self) -> bool:
        """Check if Telegram alerts are enabled and configured"""
        return (self.system_config.enable_telegram_alerts and
                bool(self.api_config.telegram_bot_token) and 
                bool(self.api_config.telegram_chat_id))


# Global configuration instance
config_manager = ConfigManager()


def get_config() -> ConfigManager:
    """Get global configuration manager instance"""
    return config_manager


def reload_config():
    """Reload configuration from environment"""
    global config_manager
    config_manager._load_environment()
    logger.info("Configuration reloaded")
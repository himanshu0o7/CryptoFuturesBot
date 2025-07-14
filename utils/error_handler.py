"""
Error handling utilities for CryptoFuturesBot
Provides retry mechanism and centralized error handling
"""

import logging
import time
import functools
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)


def retry(func: Callable, max_attempts: int = 3, delay: float = 1.0, 
          backoff: float = 2.0, label: str = "Operation") -> Any:
    """
    Retry mechanism for functions that might fail
    
    Args:
        func: Function to retry
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts
        backoff: Backoff multiplier
        label: Label for logging
        
    Returns:
        Result of function execution
        
    Raises:
        Exception: Last exception if all attempts fail
    """
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                logger.error(f"{label} failed after {max_attempts} attempts: {e}")
                raise e
            
            logger.warning(f"{label} attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= backoff
    
    return None


class ErrorHandler:
    """Centralized error handling class"""
    
    def __init__(self, telegram_alerts: bool = True):
        self.telegram_alerts = telegram_alerts
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error: Exception, context: str = "Unknown") -> None:
        """Handle errors with logging and optional Telegram alerts"""
        error_msg = f"Error in {context}: {str(error)}"
        self.logger.error(error_msg)
        
        if self.telegram_alerts:
            try:
                from .telegram_alert import send_telegram_alert
                send_telegram_alert(f"🚨 {error_msg}")
            except Exception as telegram_error:
                self.logger.error(f"Failed to send Telegram alert: {telegram_error}")
    
    def safe_execute(self, func: Callable, context: str = "Function") -> Optional[Any]:
        """Safely execute function with error handling"""
        try:
            return func()
        except Exception as e:
            self.handle_error(e, context)
            return None


def handle_exceptions(telegram_alert: bool = True):
    """Decorator for automatic exception handling"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            error_handler = ErrorHandler(telegram_alerts=telegram_alert)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler.handle_error(e, func.__name__)
                return None
        return wrapper
    return decorator
"""
Telegram alert utilities for CryptoFuturesBot
Sends notifications and alerts via Telegram
"""

import os
import requests
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_alert(message: str, parse_mode: str = "HTML") -> bool:
    """
    Send a message to Telegram
    
    Args:
        message: Message to send
        parse_mode: Message formatting mode (HTML, Markdown, or None)
        
    Returns:
        True if successful, False otherwise
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram credentials not configured. Alert not sent.")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": parse_mode
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info("Telegram alert sent successfully")
        return True
        
    except requests.RequestException as e:
        logger.error(f"Failed to send Telegram alert: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending Telegram alert: {e}")
        return False


def send_trade_alert(symbol: str, action: str, quantity: float, price: float, 
                    order_id: Optional[str] = None) -> bool:
    """
    Send formatted trade alert to Telegram
    
    Args:
        symbol: Trading symbol
        action: Trade action (BUY/SELL)
        quantity: Trade quantity
        price: Trade price
        order_id: Order ID if available
        
    Returns:
        True if successful, False otherwise
    """
    emoji = "🟢" if action.upper() == "BUY" else "🔴"
    order_info = f"\n📄 Order ID: {order_id}" if order_id else ""
    
    message = f"""
{emoji} <b>Trade Executed</b>

📊 Symbol: {symbol}
🔄 Action: {action.upper()}
📈 Quantity: {quantity}
💰 Price: ₹{price:,.2f}
🕐 Time: {os.environ.get('TZ', 'UTC')}{order_info}
    """.strip()
    
    return send_telegram_alert(message)


def send_error_alert(error_msg: str, context: str = "Bot Operation") -> bool:
    """
    Send error alert to Telegram
    
    Args:
        error_msg: Error message
        context: Error context
        
    Returns:
        True if successful, False otherwise
    """
    message = f"""
🚨 <b>Error Alert</b>

🔧 Context: {context}
❌ Error: {error_msg}
🕐 Time: {os.environ.get('TZ', 'UTC')}

Please check the bot logs for more details.
    """.strip()
    
    return send_telegram_alert(message)


def send_bot_status(status: str, details: Optional[str] = None) -> bool:
    """
    Send bot status update to Telegram
    
    Args:
        status: Bot status (STARTED, STOPPED, ERROR, etc.)
        details: Additional details
        
    Returns:
        True if successful, False otherwise
    """
    emoji = {
        "STARTED": "🟢",
        "STOPPED": "🔴", 
        "ERROR": "🚨",
        "WARNING": "🟡",
        "INFO": "ℹ️"
    }.get(status.upper(), "📊")
    
    details_text = f"\n\n📋 Details: {details}" if details else ""
    
    message = f"""
{emoji} <b>Bot Status: {status.upper()}</b>

🤖 CryptoFuturesBot
🕐 Time: {os.environ.get('TZ', 'UTC')}{details_text}
    """.strip()
    
    return send_telegram_alert(message)


def send_pnl_update(symbol: str, pnl: float, percentage: float, 
                   entry_price: float, current_price: float) -> bool:
    """
    Send PnL update to Telegram
    
    Args:
        symbol: Trading symbol
        pnl: Profit/Loss amount
        percentage: PnL percentage
        entry_price: Entry price
        current_price: Current price
        
    Returns:
        True if successful, False otherwise
    """
    emoji = "💰" if pnl >= 0 else "📉"
    pnl_color = "green" if pnl >= 0 else "red"
    
    message = f"""
{emoji} <b>PnL Update</b>

📊 Symbol: {symbol}
💹 PnL: <span style="color:{pnl_color}">₹{pnl:,.2f} ({percentage:+.2f}%)</span>
📈 Entry: ₹{entry_price:,.2f}
📊 Current: ₹{current_price:,.2f}
🕐 Time: {os.environ.get('TZ', 'UTC')}
    """.strip()
    
    return send_telegram_alert(message)


class TelegramNotifier:
    """Telegram notification manager"""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.logger = logging.getLogger(__name__)
    
    def is_configured(self) -> bool:
        """Check if Telegram is properly configured"""
        return bool(self.bot_token and self.chat_id)
    
    def send_message(self, message: str, **kwargs) -> bool:
        """Send a message using this notifier instance"""
        if not self.is_configured():
            self.logger.warning("Telegram not configured for this notifier instance")
            return False
        
        # Temporarily set environment variables for the function
        original_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        original_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        
        os.environ["TELEGRAM_BOT_TOKEN"] = self.bot_token
        os.environ["TELEGRAM_CHAT_ID"] = self.chat_id
        
        try:
            return send_telegram_alert(message, **kwargs)
        finally:
            # Restore original values
            if original_token:
                os.environ["TELEGRAM_BOT_TOKEN"] = original_token
            if original_chat_id:
                os.environ["TELEGRAM_CHAT_ID"] = original_chat_id
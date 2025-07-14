"""
Streamlit-based dashboard for CryptoFuturesBot monitoring
Provides real-time monitoring, portfolio tracking, and bot control
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
from typing import Dict, Any

# Import bot services
try:
    from services.portfolio_manager import PortfolioManager
    from services.data_feed import LiveDataFeed, MockDataFeed
    from utils.logging_setup import get_logger
    from utils.telegram_alert import send_bot_status
except ImportError as e:
    st.error(f"Failed to import bot services: {e}")
    st.stop()

logger = get_logger("Dashboard")

# Page configuration
st.set_page_config(
    page_title="CryptoFuturesBot Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1e88e5;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
    }
    .status-green {
        color: #28a745;
        font-weight: bold;
    }
    .status-red {
        color: #dc3545;
        font-weight: bold;
    }
    .status-yellow {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'portfolio_manager' not in st.session_state:
        st.session_state.portfolio_manager = PortfolioManager()
    
    if 'data_feed' not in st.session_state:
        # Use mock data feed for dashboard demo
        st.session_state.data_feed = MockDataFeed()
    
    if 'bot_status' not in st.session_state:
        st.session_state.bot_status = "STOPPED"
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()

def get_portfolio_overview():
    """Get portfolio overview data"""
    try:
        portfolio_manager = st.session_state.portfolio_manager
        stats = portfolio_manager.calculate_portfolio_stats()
        
        return {
            'total_value': stats.total_value,
            'available_balance': stats.available_balance,
            'unrealized_pnl': stats.unrealized_pnl,
            'realized_pnl': stats.realized_pnl,
            'total_pnl': stats.total_pnl,
            'positions_count': stats.positions_count,
            'daily_pnl': stats.daily_pnl,
            'win_rate': stats.win_rate,
            'total_trades': stats.total_trades
        }
    except Exception as e:
        logger.error(f"Error getting portfolio overview: {e}")
        return {}

def display_portfolio_metrics():
    """Display portfolio metrics cards"""
    overview = get_portfolio_overview()
    
    if not overview:
        st.error("Failed to load portfolio data")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Portfolio Value",
            value=f"₹{overview.get('total_value', 0):,.2f}",
            delta=f"₹{overview.get('daily_pnl', 0):,.2f}"
        )
    
    with col2:
        st.metric(
            label="Available Balance",
            value=f"₹{overview.get('available_balance', 0):,.2f}"
        )
    
    with col3:
        pnl = overview.get('total_pnl', 0)
        st.metric(
            label="Total P&L",
            value=f"₹{pnl:,.2f}",
            delta=f"{'+' if pnl >= 0 else ''}{pnl:,.2f}"
        )
    
    with col4:
        st.metric(
            label="Active Positions",
            value=overview.get('positions_count', 0)
        )

def display_current_positions():
    """Display current positions table"""
    try:
        portfolio_manager = st.session_state.portfolio_manager
        positions = portfolio_manager.get_all_positions()
        
        if not positions:
            st.info("No active positions")
            return
        
        # Convert positions to DataFrame
        position_data = []
        for pos in positions:
            pnl_pct = (pos.unrealized_pnl / (pos.quantity * pos.entry_price)) * 100 if pos.quantity * pos.entry_price > 0 else 0
            position_data.append({
                'Symbol': pos.symbol,
                'Side': pos.side,
                'Quantity': pos.quantity,
                'Entry Price': f"₹{pos.entry_price:,.2f}",
                'Current Price': f"₹{pos.current_price:,.2f}",
                'Unrealized P&L': f"₹{pos.unrealized_pnl:,.2f}",
                'P&L %': f"{pnl_pct:+.2f}%"
            })
        
        df = pd.DataFrame(position_data)
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error displaying positions: {e}")

def display_price_chart(symbol: str = "BTCUSDT"):
    """Display price chart for a symbol"""
    try:
        data_feed = st.session_state.data_feed
        
        # Generate mock price data for chart
        import numpy as np
        base_price = data_feed.get_live_price(symbol) or 50000
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='H')
        
        # Simulate price movement
        returns = np.random.normal(0, 0.02, len(dates))
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        # Create DataFrame
        df = pd.DataFrame({
            'Date': dates,
            'Price': prices[:len(dates)]
        })
        
        # Create plotly chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Price'],
            mode='lines',
            name=symbol,
            line=dict(color='#1e88e5', width=2)
        ))
        
        fig.update_layout(
            title=f"{symbol} Price Chart (7 Days)",
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error displaying chart: {e}")

def display_trading_controls():
    """Display bot trading controls"""
    st.subheader("🎛️ Bot Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Start Bot", type="primary"):
            st.session_state.bot_status = "RUNNING"
            send_bot_status("STARTED", "Bot started from dashboard")
            st.success("Bot started!")
            st.rerun()
    
    with col2:
        if st.button("⏸️ Stop Bot", type="secondary"):
            st.session_state.bot_status = "STOPPED"
            send_bot_status("STOPPED", "Bot stopped from dashboard")
            st.warning("Bot stopped!")
            st.rerun()
    
    with col3:
        if st.button("🔄 Restart Bot"):
            st.session_state.bot_status = "RESTARTING"
            st.info("Bot restarting...")
            # Simulate restart
            import time
            time.sleep(1)
            st.session_state.bot_status = "RUNNING"
            st.rerun()

def display_bot_status():
    """Display current bot status"""
    status = st.session_state.bot_status
    
    if status == "RUNNING":
        st.markdown('<p class="status-green">🟢 Bot Status: RUNNING</p>', unsafe_allow_html=True)
    elif status == "STOPPED":
        st.markdown('<p class="status-red">🔴 Bot Status: STOPPED</p>', unsafe_allow_html=True)
    elif status == "RESTARTING":
        st.markdown('<p class="status-yellow">🟡 Bot Status: RESTARTING</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-yellow">🟡 Bot Status: UNKNOWN</p>', unsafe_allow_html=True)

def display_recent_trades():
    """Display recent trades table"""
    try:
        portfolio_manager = st.session_state.portfolio_manager
        trades = portfolio_manager.trade_history[-10:]  # Last 10 trades
        
        if not trades:
            st.info("No recent trades")
            return
        
        # Convert trades to DataFrame
        trade_data = []
        for trade in trades:
            trade_data.append({
                'Time': trade.timestamp[:19],  # Remove microseconds
                'Symbol': trade.symbol,
                'Side': trade.side,
                'Quantity': trade.quantity,
                'Price': f"₹{trade.price:,.2f}",
                'Fee': f"₹{trade.fee:.2f}",
                'P&L': f"₹{trade.pnl:,.2f}" if trade.pnl else "-"
            })
        
        df = pd.DataFrame(trade_data)
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error displaying trades: {e}")

def display_configuration():
    """Display bot configuration settings"""
    st.subheader("⚙️ Configuration")
    
    with st.expander("Trading Parameters"):
        col1, col2 = st.columns(2)
        
        with col1:
            default_symbol = st.text_input("Default Symbol", value="BTCUSDT")
            stop_loss_pct = st.number_input("Stop Loss %", value=2.0, min_value=0.1, max_value=10.0, step=0.1)
            take_profit_pct = st.number_input("Take Profit %", value=4.0, min_value=0.1, max_value=20.0, step=0.1)
        
        with col2:
            risk_per_trade = st.number_input("Risk per Trade %", value=1.0, min_value=0.1, max_value=5.0, step=0.1)
            max_positions = st.number_input("Max Positions", value=5, min_value=1, max_value=20)
            dry_run = st.checkbox("Dry Run Mode", value=True)
        
        if st.button("Save Configuration"):
            # Here you would save the configuration
            st.success("Configuration saved!")

def run_dashboard():
    """Main dashboard function"""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 CryptoFuturesBot Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Navigation")
        
        page = st.selectbox(
            "Select Page",
            ["Overview", "Positions", "Trading", "Charts", "Configuration", "Logs"]
        )
        
        st.divider()
        
        # Bot status in sidebar
        display_bot_status()
        
        st.divider()
        
        # Quick stats
        st.subheader("Quick Stats")
        overview = get_portfolio_overview()
        if overview:
            st.metric("Portfolio", f"₹{overview.get('total_value', 0):,.0f}")
            st.metric("P&L", f"₹{overview.get('total_pnl', 0):,.0f}")
            st.metric("Positions", overview.get('positions_count', 0))
        
        # Auto-refresh
        if st.checkbox("Auto-refresh (30s)"):
            import time
            time.sleep(30)
            st.rerun()
    
    # Main content based on selected page
    if page == "Overview":
        st.header("📈 Portfolio Overview")
        display_portfolio_metrics()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💼 Current Positions")
            display_current_positions()
        
        with col2:
            st.subheader("📋 Recent Trades")
            display_recent_trades()
    
    elif page == "Positions":
        st.header("💼 Position Management")
        display_current_positions()
        
        # Add position management controls here
        with st.expander("Manual Position Control"):
            st.warning("⚠️ Manual position control is for advanced users only!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                symbol = st.text_input("Symbol", value="BTCUSDT")
            with col2:
                action = st.selectbox("Action", ["Close Position", "Modify Stop Loss"])
            with col3:
                if st.button("Execute"):
                    st.info(f"Would execute {action} for {symbol}")
    
    elif page == "Trading":
        st.header("🎯 Trading Controls")
        display_trading_controls()
        
        st.divider()
        
        # Manual trading section
        st.subheader("📝 Manual Trade Entry")
        with st.expander("Place Manual Trade"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                trade_symbol = st.text_input("Symbol", value="BTCUSDT", key="trade_symbol")
            with col2:
                trade_side = st.selectbox("Side", ["BUY", "SELL"])
            with col3:
                trade_quantity = st.number_input("Quantity", value=10.0, min_value=0.1)
            with col4:
                trade_type = st.selectbox("Type", ["MARKET", "LIMIT"])
            
            if st.button("Place Trade", type="primary"):
                st.warning("Manual trading disabled in demo mode")
    
    elif page == "Charts":
        st.header("📊 Price Charts")
        
        # Symbol selector
        chart_symbol = st.selectbox("Select Symbol", ["BTCUSDT", "ETHUSDT", "ADAUSDT"])
        
        display_price_chart(chart_symbol)
        
        # Additional chart controls
        col1, col2, col3 = st.columns(3)
        with col1:
            timeframe = st.selectbox("Timeframe", ["1H", "4H", "1D", "1W"])
        with col2:
            indicators = st.multiselect("Indicators", ["MA", "RSI", "MACD", "Bollinger Bands"])
        with col3:
            if st.button("Update Chart"):
                st.info("Chart updated!")
    
    elif page == "Configuration":
        display_configuration()
    
    elif page == "Logs":
        st.header("📜 Bot Logs")
        
        # Log level filter
        log_level = st.selectbox("Log Level", ["ALL", "INFO", "WARNING", "ERROR"])
        
        # Mock log entries
        log_entries = [
            "2024-01-15 10:30:15 - INFO - Bot started successfully",
            "2024-01-15 10:30:20 - INFO - Fetching price for BTCUSDT: ₹45,230.50",
            "2024-01-15 10:30:25 - INFO - Generated BUY signal for BTCUSDT",
            "2024-01-15 10:30:30 - INFO - Order placed successfully: ORDER_123456",
            "2024-01-15 10:35:15 - WARNING - High volatility detected",
            "2024-01-15 10:40:00 - INFO - Position closed with profit: ₹125.50"
        ]
        
        # Display logs in a code block
        log_text = "\n".join(log_entries)
        st.code(log_text, language="text")
        
        if st.button("Refresh Logs"):
            st.rerun()
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"Last Updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        st.caption("CryptoFuturesBot v1.0")
    with col3:
        if st.button("🔄 Refresh Data"):
            st.session_state.last_update = datetime.now()
            st.rerun()

if __name__ == "__main__":
    run_dashboard()
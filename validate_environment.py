"""
Environment validation utility for CryptoFuturesBot
Validates environment variables and configuration
"""

import os
import sys
from typing import Dict, List, Tuple
from dotenv import load_dotenv

def load_environment() -> bool:
    """Load environment variables from .env file"""
    try:
        load_dotenv()
        return True
    except Exception as e:
        print(f"Error loading .env file: {e}")
        return False

def check_required_variables() -> Tuple[bool, List[str]]:
    """Check if all required environment variables are set"""
    required_vars = [
        'COINSWITCH_API_KEY',
        'COINSWITCH_API_SECRET',
    ]
    
    optional_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID',
        'GOOGLE_API_KEY',
    ]
    
    missing_required = []
    missing_optional = []
    
    print("🔍 Checking environment variables...")
    print("\n📋 Required Variables:")
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == f"your_{var.lower()}_here":
            missing_required.append(var)
            print(f"❌ {var}: Not set or using placeholder")
        else:
            # Mask sensitive values
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {var}: {masked_value}")
    
    print("\n📋 Optional Variables:")
    
    for var in optional_vars:
        value = os.getenv(var)
        if not value or value == f"your_{var.lower()}_here":
            missing_optional.append(var)
            print(f"⚠️  {var}: Not set (optional)")
        else:
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {var}: {masked_value}")
    
    return len(missing_required) == 0, missing_required + missing_optional

def check_configuration_variables() -> Dict[str, str]:
    """Check configuration variables and their values"""
    config_vars = {
        'DEFAULT_SYMBOL': os.getenv('DEFAULT_SYMBOL', 'BTCUSDT'),
        'DEFAULT_QUANTITY': os.getenv('DEFAULT_QUANTITY', '10'),
        'DRY_RUN': os.getenv('DRY_RUN', 'true'),
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'RISK_PER_TRADE': os.getenv('RISK_PER_TRADE', '0.01'),
        'STOP_LOSS_PERCENTAGE': os.getenv('STOP_LOSS_PERCENTAGE', '0.02'),
        'TAKE_PROFIT_PERCENTAGE': os.getenv('TAKE_PROFIT_PERCENTAGE', '0.04'),
        'MAX_POSITION_SIZE': os.getenv('MAX_POSITION_SIZE', '1000'),
    }
    
    print("\n⚙️  Configuration Variables:")
    for var, value in config_vars.items():
        print(f"🔧 {var}: {value}")
    
    return config_vars

def validate_numeric_configs() -> bool:
    """Validate numeric configuration values"""
    print("\n🔢 Validating numeric configurations...")
    
    validations = []
    
    try:
        quantity = float(os.getenv('DEFAULT_QUANTITY', '10'))
        if quantity <= 0:
            print(f"❌ DEFAULT_QUANTITY must be positive: {quantity}")
            validations.append(False)
        else:
            print(f"✅ DEFAULT_QUANTITY: {quantity}")
            validations.append(True)
    except ValueError:
        print(f"❌ DEFAULT_QUANTITY must be a number: {os.getenv('DEFAULT_QUANTITY')}")
        validations.append(False)
    
    try:
        risk = float(os.getenv('RISK_PER_TRADE', '0.01'))
        if not 0 < risk <= 0.1:  # 0.1% to 10%
            print(f"❌ RISK_PER_TRADE should be between 0 and 0.1: {risk}")
            validations.append(False)
        else:
            print(f"✅ RISK_PER_TRADE: {risk * 100:.1f}%")
            validations.append(True)
    except ValueError:
        print(f"❌ RISK_PER_TRADE must be a number: {os.getenv('RISK_PER_TRADE')}")
        validations.append(False)
    
    try:
        sl_pct = float(os.getenv('STOP_LOSS_PERCENTAGE', '0.02'))
        if not 0 < sl_pct <= 0.2:  # 0.1% to 20%
            print(f"❌ STOP_LOSS_PERCENTAGE should be between 0 and 0.2: {sl_pct}")
            validations.append(False)
        else:
            print(f"✅ STOP_LOSS_PERCENTAGE: {sl_pct * 100:.1f}%")
            validations.append(True)
    except ValueError:
        print(f"❌ STOP_LOSS_PERCENTAGE must be a number: {os.getenv('STOP_LOSS_PERCENTAGE')}")
        validations.append(False)
    
    try:
        tp_pct = float(os.getenv('TAKE_PROFIT_PERCENTAGE', '0.04'))
        if not 0 < tp_pct <= 0.5:  # 0.1% to 50%
            print(f"❌ TAKE_PROFIT_PERCENTAGE should be between 0 and 0.5: {tp_pct}")
            validations.append(False)
        else:
            print(f"✅ TAKE_PROFIT_PERCENTAGE: {tp_pct * 100:.1f}%")
            validations.append(True)
    except ValueError:
        print(f"❌ TAKE_PROFIT_PERCENTAGE must be a number: {os.getenv('TAKE_PROFIT_PERCENTAGE')}")
        validations.append(False)
    
    return all(validations)

def test_imports() -> bool:
    """Test if all required modules can be imported"""
    print("\n📦 Testing module imports...")
    
    imports_ok = True
    
    try:
        from utils import error_handler, logging_setup, telegram_alert, risk_management
        print("✅ Utils modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import utils modules: {e}")
        imports_ok = False
    
    try:
        from services import trade_executor, data_feed, portfolio_manager
        print("✅ Services modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import services modules: {e}")
        imports_ok = False
    
    try:
        from strategies import base_strategy, simple_momentum
        print("✅ Strategies modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import strategies modules: {e}")
        imports_ok = False
    
    try:
        from dashboard import streamlit_dashboard
        print("✅ Dashboard modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import dashboard modules: {e}")
        imports_ok = False
    
    return imports_ok

def test_basic_functionality() -> bool:
    """Test basic bot functionality"""
    print("\n🧪 Testing basic functionality...")
    
    tests_passed = True
    
    try:
        # Test logging setup
        from utils.logging_setup import setup_logger
        logger = setup_logger("ValidationTest")
        logger.info("Logging test successful")
        print("✅ Logging system working")
    except Exception as e:
        print(f"❌ Logging system failed: {e}")
        tests_passed = False
    
    try:
        # Test risk manager
        from utils.risk_management import RiskManager
        rm = RiskManager()
        decision = rm.should_exit(100, 102)  # Should return TAKE_PROFIT
        print("✅ Risk management system working")
    except Exception as e:
        print(f"❌ Risk management system failed: {e}")
        tests_passed = False
    
    try:
        # Test data feed
        from services.data_feed import MockDataFeed
        data_feed = MockDataFeed()
        price = data_feed.get_live_price("BTCUSDT")
        if price and price > 0:
            print(f"✅ Data feed working (Mock price: ₹{price:,.2f})")
        else:
            print("❌ Data feed returned invalid price")
            tests_passed = False
    except Exception as e:
        print(f"❌ Data feed failed: {e}")
        tests_passed = False
    
    try:
        # Test trade executor
        from services.trade_executor import MockTradeExecutor
        from services.trade_executor import OrderRequest, OrderType
        
        executor = MockTradeExecutor()
        order_request = OrderRequest(
            symbol="BTCUSDT",
            side="BUY",
            quantity=10,
            order_type=OrderType.MARKET
        )
        
        response = executor.place_order(order_request)
        if response and response.order_id:
            print(f"✅ Trade executor working (Mock order: {response.order_id})")
        else:
            print("❌ Trade executor failed to return valid response")
            tests_passed = False
    except Exception as e:
        print(f"❌ Trade executor failed: {e}")
        tests_passed = False
    
    return tests_passed

def create_sample_env():
    """Create a sample .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("\n📝 Creating sample .env file...")
        try:
            with open('.env.sample', 'r') as sample_file:
                sample_content = sample_file.read()
            
            with open('.env', 'w') as env_file:
                env_file.write(sample_content)
            
            print("✅ Sample .env file created. Please edit it with your actual values.")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True

def main():
    """Main validation function"""
    print("🚀 CryptoFuturesBot Environment Validation")
    print("=" * 50)
    
    # Check if .env file exists, create if not
    create_sample_env()
    
    # Load environment
    if not load_environment():
        print("❌ Failed to load environment variables")
        return False
    
    # Check required variables
    vars_ok, missing_vars = check_required_variables()
    
    # Check configuration
    config = check_configuration_variables()
    
    # Validate numeric configs
    numeric_ok = validate_numeric_configs()
    
    # Test imports
    imports_ok = test_imports()
    
    # Test basic functionality
    functionality_ok = test_basic_functionality()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    if vars_ok:
        print("✅ Required environment variables: OK")
    else:
        print("❌ Required environment variables: MISSING")
        print(f"   Missing: {', '.join(missing_vars[:2])}")  # Show first 2 missing required vars
    
    print(f"{'✅' if numeric_ok else '❌'} Numeric configurations: {'OK' if numeric_ok else 'INVALID'}")
    print(f"{'✅' if imports_ok else '❌'} Module imports: {'OK' if imports_ok else 'FAILED'}")
    print(f"{'✅' if functionality_ok else '❌'} Basic functionality: {'OK' if functionality_ok else 'FAILED'}")
    
    overall_ok = vars_ok and numeric_ok and imports_ok and functionality_ok
    
    print("\n" + "=" * 50)
    if overall_ok:
        print("🎉 VALIDATION PASSED - Bot is ready to run!")
        print("\nNext steps:")
        print("1. Run the bot: python main.py")
        print("2. Start dashboard: streamlit run dashboard/streamlit_dashboard.py")
    else:
        print("⚠️  VALIDATION FAILED - Please fix the issues above")
        print("\nRequired actions:")
        if not vars_ok:
            print("1. Set required environment variables in .env file")
        if not numeric_ok:
            print("2. Fix invalid numeric configuration values")
        if not imports_ok:
            print("3. Install missing dependencies: pip install -r requirements.txt")
        if not functionality_ok:
            print("4. Check error logs and fix functionality issues")
    
    print("=" * 50)
    
    return overall_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
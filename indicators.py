import pandas as pd

def calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index (RSI)."""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - 100 / (1 + rs)
    return rsi

def calculate_macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """Calculate MACD indicator."""
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - macd_signal
    return pd.DataFrame({'macd': macd, 'signal': macd_signal, 'hist': histogram})

def calculate_supertrend(df: pd.DataFrame, period: int = 10, multiplier: int = 3) -> pd.Series:
    """Calculate Supertrend indicator."""
    high = df['high']
    low = df['low']
    close = df['close']
    tr = pd.concat([(high - low), (high - close.shift()), (close.shift() - low)], axis=1)
    tr = tr.abs().max(axis=1)
    atr = tr.rolling(window=period).mean()
    hl2 = (high + low) / 2
    upper_band = hl2 + multiplier * atr
    lower_band = hl2 - multiplier * atr
    supertrend = pd.Series(index=df.index, dtype='float64')
    direction = pd.Series(index=df.index, dtype='int')

    for i in range(len(df)):
        if i == 0:
            supertrend.iloc[i] = upper_band.iloc[i]
            direction.iloc[i] = 1
            continue
        if close.iloc[i] > supertrend.iloc[i-1]:
            direction.iloc[i] = 1
        elif close.iloc[i] < supertrend.iloc[i-1]:
            direction.iloc[i] = -1
        else:
            direction.iloc[i] = direction.iloc[i-1]

        if direction.iloc[i] == 1:
            supertrend.iloc[i] = max(lower_band.iloc[i], supertrend.iloc[i-1])
        else:
            supertrend.iloc[i] = min(upper_band.iloc[i], supertrend.iloc[i-1])

    return supertrend

def detect_breakout(df: pd.DataFrame, lookback: int = 20, volume_multiplier: float = 2.0,
                     price_col: str = 'close', volume_col: str = 'volume') -> bool:
    """Detect breakout with volume spike."""
    if len(df) < lookback + 1:
        return False
    recent = df.iloc[-lookback-1:-1]
    last_price = df[price_col].iloc[-1]
    last_volume = df[volume_col].iloc[-1]
    price_threshold = recent[price_col].max()
    volume_threshold = recent[volume_col].mean() * volume_multiplier
    return last_price > price_threshold and last_volume > volume_threshold

def detect_breakdown(df: pd.DataFrame, lookback: int = 20, volume_multiplier: float = 2.0,
                      price_col: str = 'close', volume_col: str = 'volume') -> bool:
    """Detect breakdown with volume spike."""
    if len(df) < lookback + 1:
        return False
    recent = df.iloc[-lookback-1:-1]
    last_price = df[price_col].iloc[-1]
    last_volume = df[volume_col].iloc[-1]
    price_threshold = recent[price_col].min()
    volume_threshold = recent[volume_col].mean() * volume_multiplier
    return last_price < price_threshold and last_volume > volume_threshold

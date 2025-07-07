from typing import List, Dict, Optional


def sma(values: List[float], period: int) -> Optional[float]:
    """Simple moving average."""
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def detect_breakout(
    candles: List[Dict[str, float]], lookback: int = 20
) -> Optional[str]:
    """Return 'up' if breakout above range, 'down' if below range, else None."""
    if len(candles) < lookback + 1:
        return None
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    close = candles[-1]["close"]
    recent_high = max(highs[-lookback - 1 : -1])
    recent_low = min(lows[-lookback - 1 : -1])
    if close > recent_high:
        return "up"
    if close < recent_low:
        return "down"
    return None

# 4. SL/TP/TSL Logic
class RiskManager:
    def __init__(self, sl_pct=0.02, tp_pct=0.04):
        self.sl_pct = sl_pct
        self.tp_pct = tp_pct

    def should_exit(self, entry_price, current_price):
        change_pct = (current_price - entry_price) / entry_price
        if change_pct <= -self.sl_pct:
            return "SL"
        elif change_pct >= self.tp_pct:
            return "TP"
        return None

import numpy as np

def predict(h):
    if len(h) < 10:
        return None

    last = h[-30:]

    avg = np.mean(last)
    std = np.std(last)

    low = sum(x < 1.5 for x in last)
    high = sum(x > 3 for x in last)

    risk = min(95, int(std * 45))
    confidence = max(5, 100 - risk)

    return {
        "avg": avg,
        "risk": risk,
        "confidence": confidence,
        "low": low,
        "high": high
    }


def format_prediction(p):
    if not p:
        return "⏳ недостаточно данных"

    if p["low"] >= 6:
        return f"""
💎 ELITE SIGNAL

🔥 накопление низких
🎯 шанс: {p['confidence']}%
📈 2x–5x
📊 риск: {p['risk']}%
"""

    if p["high"] >= 5:
        return f"""
⚠️ RISK ZONE

🚫 пропуск
📊 риск: {p['risk']}%
"""

    if p["avg"] < 2:
        return f"""
📊 PRO SIGNAL

📈 рост возможен
📊 риск: {p['risk']}%
"""

    return f"""
⚖️ WAIT ZONE

📊 риск: {p['risk']}%
"""

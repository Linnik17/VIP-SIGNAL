import numpy as np

def analyze(history):
    if len(history) < 10:
        return "⏳ Нужно минимум 10 значений"

    last = history[-20:]

    avg = np.mean(last)
    std = np.std(last)

    low = sum(x < 1.5 for x in last)
    high = sum(x > 3 for x in last)

    risk = min(95, int(std * 40))
    chance = max(5, 100 - risk)

    if low >= 6:
        return f"""
💎 VIP SIGNAL

🔥 серия низких
🎯 шанс роста: {chance}%
📈 цель: 2x–5x
📊 риск: {risk}%
"""

    if high >= 5:
        return f"""
⚠️ VIP ALERT

📉 перегрев рынка
🚫 вход опасен
📊 риск: {risk}%
"""

    if avg < 2:
        return f"""
📊 VIP MODE

📈 спокойный рынок
🎯 рост 2x–3x возможен
📊 риск: {risk}%
"""

    return f"""
⚖️ NEUTRAL

⏳ нет сигнала
📊 риск: {risk}%
"""


def stats(history):
    last = history[-30:]
    total = len(last)

    return {
        "low": round(sum(x < 1.5 for x in last)/total*100, 1),
        "mid": round(sum(1.5 <= x <= 3 for x in last)/total*100, 1),
        "high": round(sum(x > 3 for x in last)/total*100, 1),
    }

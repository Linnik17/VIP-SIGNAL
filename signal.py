import numpy as np
from db import get

def generate_signal():
    h = get()

    if len(h) < 15:
        return "⏳ мало данных"

    last = h[-20:]

    avg = np.mean(last)
    std = np.std(last)

    low = sum(x < 1.5 for x in last)
    high = sum(x > 3 for x in last)

    risk = min(95, int(std * 45))
    chance = max(5, 100 - risk)

    if low >= 6:
        return f"""
🚨 AUTO SIGNAL

🔥 низкие серии
🎯 шанс: {chance}%
📈 2x–5x
📊 риск: {risk}%
"""

    if high >= 5:
        return f"""
⚠️ AUTO WARNING

📉 перегрев
🚫 пропуск
📊 риск: {risk}%
"""

    return f"""
📊 AUTO MODE

⏳ нет сильного сигнала
📊 риск: {risk}%
"""

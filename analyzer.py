import numpy as np

def smart_analysis(history):
    if len(history) < 10:
        return "⏳ Нужно минимум 10 раундов для анализа"

    last = history[-10:]

    avg = np.mean(last)
    std = np.std(last)

    low_streak = 0
    for x in reversed(last):
        if x < 1.5:
            low_streak += 1
        else:
            break

    high_streak = 0
    for x in reversed(last):
        if x > 3:
            high_streak += 1
        else:
            break

    # 🧠 логика уровней риска
    risk = min(100, int(std * 35))

    if low_streak >= 4:
        return f"""
🔥 СЕРИЯ НИЗКИХ

📊 риск: {risk}%
🎯 шанс роста: HIGH
📈 цель: 2x–5x
"""

    if high_streak >= 3:
        return f"""
⚠️ ПЕРЕГРЕВ

📊 риск: {risk}%
🚫 вход опасен
📉 ожидается откат
"""

    if avg < 2:
        return f"""
📈 СПОКОЙНЫЙ РЫНОК

📊 риск: {risk}%
🎯 умеренный рост 2x–3x
"""

    return f"""
⚖️ НЕЙТРАЛЬНО

📊 риск: {risk}%
⏳ лучше наблюдать
"""


def probability_score(history):
    last = history[-20:]

    low = sum(1 for x in last if x < 1.5)
    mid = sum(1 for x in last if 1.5 <= x <= 3)
    high = sum(1 for x in last if x > 3)

    total = len(last)

    return {
        "low": round(low/total*100, 1),
        "mid": round(mid/total*100, 1),
        "high": round(high/total*100, 1),
    }

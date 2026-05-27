history = []

def add(v):
    history.append(v)
    if len(history) > 500:
        history.pop(0)

def get():
    return history

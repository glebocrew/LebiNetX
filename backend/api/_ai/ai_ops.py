import re
from collections import Counter

def ai_hashtags(text, top_n=3):
    stop_words = {
        "и", "в", "во", "на", "с", "со", "а", "но", "что", "это",
        "как", "к", "по", "за", "из", "у", "от", "для", "о",
        "the", "and", "or", "to", "of", "in", "on", "is", "are"
    }

    words = re.findall(r"\b[a-zа-яё]{4,}\b", text.lower())
    words = [w for w in words if w not in stop_words]

    most_common = Counter(words).most_common(top_n)

    return [f"#{word}" for word, _ in most_common]

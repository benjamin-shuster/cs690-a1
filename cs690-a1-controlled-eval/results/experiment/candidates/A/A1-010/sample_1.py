def word_counts(text):
    import string

    punctuation = string.punctuation.replace("_", "").replace("-", "").replace("/", "").replace("\\", "").replace("<", "").replace(">", "").replace("@", "").replace("#", "").replace("$", "").replace("%", "").replace("^", "").replace("&", "").replace("*", "").replace("+", "").replace("=", "").replace("|", "").replace("~", "").replace("`", "")
    punctuation = ".,;:!?\"'()[]{}"
    counts = {}
    for token in text.split():
        normalized = token.lower().strip(punctuation)
        if normalized:
            counts[normalized] = counts.get(normalized, 0) + 1
    return counts

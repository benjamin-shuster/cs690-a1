def word_counts(text):
    import string

    punctuation = string.punctuation
    return {
        token: count
        for token, count in __import__("collections").Counter(
            normalized
            for token in text.split()
            if (normalized := token.lower().strip(punctuation))
        ).items()
    }

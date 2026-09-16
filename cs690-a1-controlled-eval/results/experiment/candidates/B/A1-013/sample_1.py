from collections import Counter

def top_k_frequent(items, k):
    if k == 0:
        return []

    counts = Counter()
    first_seen = {}

    for index, item in enumerate(items):
        if item not in counts:
            first_seen[item] = index
        counts[item] += 1

    return [
        item
        for item, _ in sorted(
            counts.items(),
            key=lambda pair: (-pair[1], first_seen[pair[0]])
        )[:k]
    ]

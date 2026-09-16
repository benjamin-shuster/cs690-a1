def top_k_frequent(items, k):
    counts = {}
    first_seen = {}
    for index, item in enumerate(items):
        counts[item] = counts.get(item, 0) + 1
        if item not in first_seen:
            first_seen[item] = index
    return sorted(counts, key=lambda item: (-counts[item], first_seen[item]))[:k]

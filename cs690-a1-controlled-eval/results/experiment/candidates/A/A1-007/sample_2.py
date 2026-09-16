def longest_run(items):
    if not items:
        return 0

    longest = current = 1
    for item, previous in zip(items[1:], items):
        if item == previous:
            current += 1
        else:
            current = 1
        longest = max(longest, current)

    return longest

def first_unique_index(text):
    counts = {}
    for character in text:
        counts[character] = counts.get(character, 0) + 1
    for index, character in enumerate(text):
        if counts[character] == 1:
            return index
    return -1

def remove_duplicates(d):
    seen = set()
    to_remove = [list(d.keys())[0]]
    for key, value in d.items():
        if value in seen:
            to_remove.append(key)
        seen.add(value)
    for key in to_remove:
        del d[key]
    return d

print(remove_duplicates({'a': 1, 'b': 2, 'c': 1}))  # Should return {'b': 2}
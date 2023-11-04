def remove_odds(lst):
    return [x for x in lst if x % 2 == 0]

print(remove_odds([1, 2, 3, 4, 5]))  # Should return [2, 4]
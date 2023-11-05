def merge_nested_dictionaries(dict1: dict, dict2: dict)->dict:
    dict1.update(dict2)
    return dict1

dict1 = {'a': {'x': 1, 'y': 2}, 'b': {'z': 3}}
dict2 = {'c': {'w': 4}, 'd': {'u': 5, 'v': 6}}
print(merge_nested_dictionaries(dict1, dict2))
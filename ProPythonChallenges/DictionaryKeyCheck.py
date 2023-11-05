def safe_dict_access(dictionary: dict, key: str):
    res = None
    try:
        res = dictionary[key]
    except KeyError:
       print("Key not in dictionary")
    finally:
        return res

print(safe_dict_access({'a': 1, 'b': 2, 'c': 3}, 'd'))
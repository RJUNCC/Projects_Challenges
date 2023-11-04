def swap_dict(dictionary):
    new_dict = {value: key for key, value in dictionary.items()}
    return new_dict

my_dict = {1: 'a', 2: 'b', 3: 'c'}
print(swap_dict(my_dict)) # Expected: {'a': 1, 'b': 2, 'c': 3}
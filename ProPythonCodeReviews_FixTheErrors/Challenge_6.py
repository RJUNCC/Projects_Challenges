def flatten_list(nested_list):
    for i in nested_list:
        if isinstance(i, list):
            yield from flatten_list(i)
        else:
            yield i

def loopGenerator(generator: list):
    ls = [i for i in generator]
    return ls

print(loopGenerator(flatten_list([1, 2, [3, 4, 5], 6]))) # Expected: [1, 2, 3, 4, 5, 6]
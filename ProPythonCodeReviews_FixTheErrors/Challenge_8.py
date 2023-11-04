def extract_numbers(input_list):
    return [i for i in input_list if isinstance(i, int)]

print(extract_numbers([1, '2', 3, 'four', 5.0, 6]))


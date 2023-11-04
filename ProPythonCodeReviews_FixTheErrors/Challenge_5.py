def convert_to_int(input_list):
    return [int(i) for i in input_list if i.isdigit()]

print(convert_to_int(['1', '2', 'three']))
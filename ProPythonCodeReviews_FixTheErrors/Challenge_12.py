def find_max(lst):
    max_value = 0
    for num in lst:
        if num > max_value:
            max_value = num
    return max_value

print(find_max([3, 2, 8, 5, 10]))  # Should return 10
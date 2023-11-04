def second_largest(numbers):
    largest = max(numbers)
    second_largest = None
    for num in numbers:
        if num < largest and (second_largest is None or num > second_largest):
            second_largest = num
    return second_largest

numbers = [1, 2, 3, 4, 5]
print(second_largest(numbers)) # Expected: 4
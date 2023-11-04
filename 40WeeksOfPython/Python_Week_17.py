def number_length(number):
    count = 0;
    if number == 0:
        return 1
    while number > 0:
        number //= 10
        count += 1
    return count

print(number_length(10))
print(number_length(5000))
print(number_length(0))
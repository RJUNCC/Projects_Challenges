# Problem 1
def min_to_sec(minutes: int) -> int:
    return minutes*60

print(min_to_sec(60))
print(min_to_sec(30))

# Problem 2
def summation(num1, num2):
    return num1 + num2

print(summation(1,2))

# Problem 3
def count_vowels(str: str) -> int:
    vowels = ['a', 'e', 'i', 'o', 'u']
    new_str = str.lower()
    count = 0
    for i in new_str:
        if i in vowels:
            count += 1
    return count

print(count_vowels('aeiouy'))
print(count_vowels('AEIOUY'))

# Bonus
def fizzBuzz(num):
    if num % 3 == 0:
        if num % 5 == 0:
            return "FizzBuzz"
        return "Fizz"
    elif num % 5 == 0:
        return "Buzz"

print(fizzBuzz(5))
print(fizzBuzz(6))
print(fizzBuzz(15))
def divide_numbers(num1, num2):
    result = None
    try:
        result = num1 / num2
    except ZeroDivisionError:
        print('Cannot divide by zero')
    finally:
        return result

print(divide_numbers(4, 0))
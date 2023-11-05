def safe_division(num1: int, num2: int):
    try:
        return num1 / num2
    except ZeroDivisionError:
        print("Cannot divide by 0.")
    except TypeError:
        print("Wrong data type for one or both paramaters.")
    
print(safe_division(10, 2))
# Problem 1
def discount(origPrice: float, discPerc: float) -> float:
    return origPrice - origPrice * (discPerc/100)

print(discount(65, 25)) # if 25% off than it would be original price * (1-percentage)

# Problem 2
def year_to_day(ageYears: int) -> int:
    return ageYears * 365

print(year_to_day(3))

# Problem 3
def rad_to_deg(angle: float) -> float:
    import numpy as np
    return angle * np.pi/180

print(rad_to_deg(60))

# # Bonus
# def get_days(date1: str, date2: str):
#     # assuming format: mm/dd/yyyy
#     d1list = date1.split('/')
#     d2list = date2.split('/')
#     numYears = abs(int(d1list[-1]) - int(d2list[-1]))
#     numMonths = int(d1list[0]) - int(d2list[0])
#     # return int(d1list[1]) - int(d2list[1])

# print(get_days("07/15/2022", "04/26/1994"))
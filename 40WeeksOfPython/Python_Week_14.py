def firstLetter(ls: list) -> list:
    return [i[0] for i in ls]

answer = firstLetter(['Ellie', 'Tim', 'Matt'])
print(answer)

def evenVals(ls: list) -> list:
    return [i for i in ls if i%2==0]

answer2 = evenVals([1, 2, 3, 4, 5, 6])
print(answer2)

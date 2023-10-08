def index_of_caps(word: str) -> list:
    indexList = []
    for i in range(len(word)):
        if word[i].isupper():
            indexList.append(i)
    return indexList

print(index_of_caps('eDaBiT')) # [1, 3, 5]
print(index_of_caps('SSAABB')) # [1, 2, 3, 4, 5, 6]
print(index_of_caps('eQuINoX'))
print(index_of_caps('determine'))
print(index_of_caps('STRIKE'))
print(index_of_caps('sUn'))
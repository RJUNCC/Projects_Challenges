from typing import List

# easy: odd or even sum
def odd_or_even_sum(numbers):
  return "odd" if sum(numbers) % 2 == 1 else "even"

print(odd_or_even_sum([1,2,3,4,5,6,7])) # even
print(odd_or_even_sum([1,2,3,4,5,6])) # odd

# medium: merge sorted lists
def merge_sorted_lists(list1, list2):
  return sorted(list1+list2)

l1 = [1, 3, 5]
l2 = [2, 4, 6]
print(merge_sorted_lists(l1, l2))

# hard: longest substring without repeating characters
def longest_substring(s):
  x = s[0]
  for i in range(1, len(s)):
    if s[i] == s[i-1]:
      break
    else:
      x += s[i]

  return len(x)

print(longest_substring("abcabcbb"))

# easy: tupe reverse
def reverse_tuple(t: tuple) -> tuple:
  return t[::-1]

tuple1 = (1, 2, 3, 4, 5)
tuple2 = ("a", "b", "c")
tuple3 = (True, False, True)
print(reverse_tuple(tuple1))
print(reverse_tuple(tuple2))
print(reverse_tuple(tuple3))

# medium: student grade manager
def add_grade(student_grades: dict[str, List[int]], student: str, grade: List[int]):
  student_grades[student] = grade # key is student value is a list of grades
  return student_grades # return dictionary

student_grades = {
"Alice": [90, 85],
"Bob": [80, 85],
"Charlie": [70, 75],
}

print(add_grade(student_grades, "Ryan", [100, 99]))

# hard: Longest Consecutive Sequence
def longest_consecutive_sequence(nums):
  if not nums:
      return 0
  
  nums = list(set(nums))
  nums.sort()

  longest_streak = 1
  current_streak = 1

  for i in range(1, len(nums)):
    if nums[i] == nums[i-1] + 1:
      current_streak += 1
    else:
      longest_streak = max(longest_streak, current_streak)
      current_streak = 1
  return max(longest_streak, current_streak)
  
list1 = [1, 2, 3, 4, 5]
list2 = [5, 4, 7, 8, 9, 1, 2, 3]
list3 = [1, 3, 2, 4, 5, 7, 6, 9]

print(longest_consecutive_sequence(list1))
print(longest_consecutive_sequence(list2))
print(longest_consecutive_sequence(list3))

# Bonus: OOP

'''Will raise an exception if not the right dtype'''
class InvalidTypeError(Exception):
  pass

class Library(object):
  
  # constructor
  def __init__(self, temp="Harry Potter"):
    self.lst: List[str] = [temp]

  # methods
  def add_book(self, book_name: str) -> None:
    if not isinstance(book_name, str):
      raise InvalidTypeError("Only strings allowed.")
    self.lst.append(book_name)

  def remove_book(self, book_name: str) -> None:
    for i in self.lst:
      
        if i == book_name:
            self.lst.remove(i)
        else:
            print("Book not found!")
    
  def list_books(self) -> List[str]:
    return self.lst

a = Library()
print(a.list_books())
a.add_book("Chronicles of Narnia")
print(a.list_books())
a.remove_book("Harry Potter")
print(a.list_books())
a.remove_book("MrPoopyButthole")
print(a.list_books())
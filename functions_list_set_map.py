def vol(rad):
    import math
    return (4/3) * math.pi * (rad**3)

print(vol(2))

def ran_check(num,low,high):
    return num in range(low,high+1)
    #if num in range(low,high+1):
        #return print(f'{num} is in range between {low} and {high}')
print(ran_check(3,1,10))

def up_low(s):
    upper = 0
    lower = 0
    for letter in s:
        if letter.isupper():
            upper += 1
        elif letter.islower():
            lower += 1

    print(f'Original String :  Hello Mr. Rogers, how are you this fine Tuesday?')
    print(f'No. of Upper case characters :  {upper}')
    print(f'No. of Lower case Characters :  {lower}')

s = 'Hello Mr. Rogers, how are you this fine Tuesday?'
up_low(s)

# filter
def unique_list(l):
    newl=[]
    for i in l:
        if i not in newl:
            newl.append(i)

    return newl
   # return list(filter(unique,l)

print(unique_list([1,1,1,1,2,2,3,3,3,3,4,5]))

def unique_list2(s):
    return list(set(s))

print(unique_list2([1,1,1,1,2,2,3,3,3,3,4,5]))

# map
def multiply(numbers):
     mult = 1
     for index in numbers:
         mult *= index
     return mult

result = multiply([1, 2, 3, -4])
print(result)

from functools import reduce
result = reduce(lambda x,y: x*y, [1,2,3,-4])
print(result)

def palindrome(s):
    return s == s[::-1]

print(palindrome('helleh'))

# dict to map a:1, iterate over keys and true if values > 1
#mystring = 'William'

# Given a string, return a string where for every char in the original, there are two chars.

index=0
newstring = ''
for letter in mystring:
    print (letter)
   newstring = newstring + letter + letter
    newstring[index] = letter
    newstring[index+1] = letter
    index += 1

print(type (newstring))

print (newstring)

def myfunc(name):
    print('My name is {}'.format(name))

myfunc('William')

def myfunc(a):
    if a == True:
        return 'Hello'
    elif a == False:
        return 'Goodbye'

result = myfunc(False)
print (result)

def myfunc(x,y,z):
    if z == True:
        return x
    else:
        return y

result = myfunc('Hello','Goodbye',True)
print (result)

def is_greater(arg1,arg2):
    if arg1 > arg1:
        return True
    else:
        return False

def myfunc(a,b):
    # a, b are positional arguements
    # have to pass in a tuple to the sum function
    return sum ((a,b)) * 0.05

result = myfunc(10,10)
print (result)


def myfunc2(*args):
    # tuple of incoming parameters
    # can handle any number of args
    return sum(args) * 0.05

result = myfunc2(10,10)
print (result)

def myfunc(**kwargs):
    print(kwargs)
    if 'fruit' in kwargs:
        print('My fruit of choice is {}'.format(kwargs['fruit']))
    else:
        print('I did not find any fruit here')

myfunc(fruit='apple',veggie='lettuce')


def myfunc(*args,**kwargs):
    print(args)
    print(kwargs)
    print('I would like {} {}'.format(args[0],kwargs['food']))

myfunc(10,20,30,fruit='oragne',food='eggs',animal='dog')

def myfunc(*args):
    return [num for num in args if num%2 == 0]

print(myfunc(5,6,7,8))

def myfunc(string):
    newstring=[]
    for index in range(0,len(string)):
        if index%2 == 1:
            newstring.append(string[index].upper())
            #print(newstring)
        else:
            newstring.append(string[index].lower())
            #print(newstring)

    return ''.join(newstring)


    # for letter in string:
    #     print (letter.upper())

result = myfunc('William')
print(result)

def spy_game(nums):
    first0 = False
    second0 = False
    seven = False
    for item in nums:
        if item == 0 and not first0:
            first0 = True
        elif item == 0 and first0:
            second0 = True
        elif item == 7 and first0 and second0:
            seven = True

    if first0 and second0 and seven:
        return True
    else:
        return False

print(spy_game([1,7,2,0,4,5,0]))

def count_primes(num):
    count_of_primes = 0
    for i in range(2,num+1):
        print(i)
        if i%2 == 0:


print(count_primes(100))

# map function
def square(num):
    return num**2

# want to apply square function to each item in list
my_nums = [1,2,3,4,5]

for item in map(square,my_nums):
    print(item)

# can cast the result to a list
result = list(map(square,my_nums))

print(result)

def splicer(mystring):
    if len(mystring)%2 == 0:
        return 'EVEN'
    else:
        return mystring[0]

names = ['William','Edward','Hargrove']
# map executes the function. You pass the function in as an argument
result = list(map(splicer,names))
print(result)

def check_even(num):
    return num%2 == 0

mynums = [1,2,3,4,5,6]

# only want even numbers from this list
# filter based on the function's condition

result = list(filter(check_even,mynums))
print(result)

# start with a function and convert to a lamdba

def square(num):
    return num**2
print(square(3))

# which is same as

def square(num): return num**2
print(square(4))

# and can be converted into a lambda expression
# remove name, return and def keyword, replace with lambda

lambda_square = lambda num: num **2
print(lambda_square(5))

# usually lambda expressions are not named and assigned to as in above
# usually used as function calls in other expressions (eg map/filter)
# lambda syntax arg:return

mynums = [1,2,3,4,5]
# map the lambda expression to the list of nums
result = list(map(lambda num:num**2,mynums))
print(result)

result = list(filter(lambda num:num%2 == 0,mynums))
print(result)

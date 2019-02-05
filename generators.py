# standard function to return cubes
def create_cubes(n):
    result = []
    for x in range(n):
        result.append(x**3)
    return result


print(create_cubes(10))

# can just yield the cubed numbers
# generate the values if needed

def gen_create_cubes(n):
    for x in range(n):
        yield x**3

# returns an object that cannot be directly printed
'''
eg 
print(gen_create_cubes(10))
returns <generator object gen_create_cubes at 0x00000259205F7B88>
'''

# have to iterate through the list of numbers
for num in gen_create_cubes(10):
    print(num)
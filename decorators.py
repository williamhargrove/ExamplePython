@new_decorator
# specifying @new_decorator above will pass function func_needs_decorator to the new_decorator function
def func_needs_decorator():
    print('I want to be decorated')


func_needs_decorator()
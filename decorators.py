def new_decorator(original_function):

    def wrap_function():
        print('Some extra code, before the original function')
        original_function() # note we execute the original function
        print('Some extra code, after the original function')

    # notice that we are returning a function
    return wrap_function

@new_decorator
# specifying @new_decorator above will pass function func_needs_decorator to the new_decorator function
def func_needs_decorator():
    print('I want to be decorated')


func_needs_decorator()
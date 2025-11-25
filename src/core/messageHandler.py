


# @on decorator
def on(f: callable, *args, **kwargs):
    l = f.__name__.split("_")
    print(l)
    
    f(*args, **kwargs)


on(on, lambda : 0)
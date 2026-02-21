import time
import functools
import traceback
def cache(func):
    memo = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in memo:
            memo[key] = func(*args, **kwargs)
        return memo[key]
    return wrapper


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ {func.__name__} took {end - start:.5f}s")
        return result
    return wrapper

import sys
import time
from types import NoneType
from functools import wraps


def data_size(obj, *, precision=2):
    for u in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]:
        if n := sys.getsizeof(obj) < (k := 1000):
            return f"{round(n, precision)} {u}"
        n /= k


# decorator to time a function
def time_it(func):
    @wraps(func)
    def timed(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds")
        return result

    return timed


# decorator to size_it of the data being returned by a function
def size_it(func):
    @wraps(func)
    def size_of(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, NoneType):
            return
        print(f"{func.__name__} returned datatype {type(result)} size {data_size(result)}")
        return result

    return size_of


# a decorator that will log the function call
def log_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} called with args: {args} and kwargs: {kwargs}")
        return func(*args, **kwargs)

    return wrapper


# decorator to time, size and log a function
def inspect_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} called with args: {args} and kwargs: {kwargs}")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds")
        if not isinstance(result, NoneType):
            print(f"{func.__name__} returned datatype {type(result)} size {data_size(result)}")
            return result

    return wrapper


# decorator to wrap try except
def attempt_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{func.__name__} failed with error: {e}")

    return wrapper


# decorator to break function
def break_it(_func):
    @wraps(_func)
    def wrapper(*_, **__):
        raise Exception("This function has been broken")

    return wrapper


# decorator that raises an exception
def raise_it(_func, exception=Exception, message=None):
    @wraps(_func)
    def wrapper(*_, **__):
        raise exception(message)

    return wrapper


# a decorator that will never run the function, but return a predefined return value
def fake_it(_func, return_value=None):
    @wraps(_func)
    def wrapper(*_, **__):
        return return_value

    return wrapper


# decorator to delay a call
def delay_it(func, time_to_delay):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(time_to_delay)
        return func(*args, **kwargs)

    return wrapper


# decorator to play an alert sound
def alert_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("\a\r")
        return func(*args, **kwargs)

    return wrapper


# decorator that plays several alerts
def jingle_it(func, jingles=3, delay=1.0):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for _ in range(jingles):
            print("\a\r", sep="", end="")
            time.sleep(delay)
        return func(*args, **kwargs)

    return wrapper


# decorator to take you to a webpage
def web_it(func, url):
    import webbrowser

    @wraps(func)
    def wrapper(*args, **kwargs):
        webbrowser.open_new_tab(url)
        return func(*args, **kwargs)

    return wrapper


# decorator that asserts that a function returns a specific value
def assert_it(predicate, message=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            val = func(*args, **kwargs)
            if message is not None:
                assert predicate(val), message
            else:
                assert predicate(val)
            return val

        return wrapper

    return decorator

import functools
import time

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()   # 1
        value = func(*args, **kwargs)
        end_time = time.time()     # 2
        run_time = end_time - start_time    # 3
        print("Finished in ", run_time, " secs")
        return value
    return wrapper_timer
    


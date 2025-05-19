import time
from functools import wraps, lru_cache


def log_execution_time(func):
    wraps(func)

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter() - start_time
        arg_lst = [repr(arg) for arg in args]
        arg_lst.extend(f"{k}={v!r}" for k, v in kwargs.items())
        arg_str = ", ".join(arg_lst)
        print(
            f"Execution time for {func.__name__}({arg_str}): {end_time:.6f} seconds -> {result}"
        )
        return result

    return wrapper


@log_execution_time
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


@lru_cache
@log_execution_time
def fibonacci(n):
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(20))

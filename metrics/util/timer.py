from time import perf_counter

class Timer:
    "Simple timer class for reporting the time taken by a block of code."

    def __init__(self, name):
        self.name = name
        self.start_time = None

    def __enter__(self):
        "Starts the timer upon entering a with-block."
        self.start_time = perf_counter()

    def __exit__(self, exc_type, exc_val, tb):
        "Ends the timer and reports time taken upon exiting a with-block."
        end_time = perf_counter()
        execution_time = end_time - self.start_time
        print(f'{self.name} took {execution_time:.8f}s to execute')

# timer decorator
def timer(fn):
    "Decorator for wrapping function calls with a Timer."
    def inner(*args, **kwargs):
        with Timer(fn.__name__):
            return fn(*args, **kwargs)

    return inner
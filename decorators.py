import logging
from datetime import datetime
import time

# Set up logging
logging.basicConfig(filename='task_manager.log', level=logging.INFO,)

def log_action(func):
    def wrapper(*args, **kwargs):
        current_datetime = datetime.now()
        # STEP 2.2: YOUR CODE HERE
        logging.info(f"{current_datetime}: Executing function: {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        return result
    return wrapper

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        # STEP 2.3: YOUR CODE HERE
        logging.info(f"Function {func.__name__} executed in {total_time:.4f} seconds")
        return result
    return wrapper
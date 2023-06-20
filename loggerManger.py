import logging
import os
import inspect

# Create the log file directory if it doesn't exist
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Create an empty log file if it doesn't exist
log_file_path = os.path.join(log_directory, "logs_file.log")
if not os.path.isfile(log_file_path):
    open(log_file_path, 'a').close()

logforamt = '''
====== %(asctime)s ====== %(levelname)s ======
 %(message)s
 =================== end log ======================
'''
logging.basicConfig(filename="logs/logs_file.log",
                    level=logging.INFO,
                    format=logforamt)


def logger(func):
    """
    Decorator function to log the function name and its arguments
    """

    def sync_wrapper(*args, **kwargs):
        logging.info(f"Running {func.__name__}.\nWith arguments {args} {kwargs}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")

    async def async_wrapper(*args, **kwargs):
        logging.info(f"Running {func.__name__} with arguments {args} {kwargs}")
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.info(f"Error in {func.__name__}: {e}")

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

from .Logger import Logger

def errorHandler(func):

    def wrapper(*args, **kwargs):
        logger = Logger()
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e.__traceback__.tb_lineno}: {e}")

    return wrapper
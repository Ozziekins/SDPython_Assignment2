from contextlib import redirect_stdout
from io import StringIO


def logger(func):
    """
    A decorator for logging output of a file we do
    not want to see in the output.
    :param func: The function to be decorated
    :return wrapper: the reference to the wrapped function
    """

    def wrapper(*args, **kwargs):
        """
        A decorated function.
        Redirects the output of the function to a file
        :param args: list of positional arguments
        required by the decorated function
        :param kwargs: list of keyword arguments
        required by the decorated function
        :return: None
        """
        with redirect_stdout(StringIO()):
            result = func(*args, **kwargs)
        return result

    return wrapper

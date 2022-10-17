import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
import traceback
from io import StringIO
from pathlib import Path

_Path = (Path(__file__).parent / '../../assets/error_log.txt').resolve()


def handle_indent(value_to_indent):
    """
    Indents every subsequent line of a multiline string by 11 spaces
    :param value_to_indent: The value that needs to be indented, has to be convertible to a string
    :return: The indented multiline string
    """
    return ('\n' + (' ' * 11)).join(str(value_to_indent).splitlines())


def error_logger(func):
    """
    Serves as an exception catcher.
    It catches all the exceptions that occur while running
    a decorated function. It pipes the error to a log file.
    :param func: The decorator function to be wrapped.
    :return wrapper: The newly wrapped function
    """

    def wrapper(*args, **kwargs):
        """
        The decorated function.
        It saves the following to the error_log.txt file
            1) The timestamp of the error
            2) The type of the error
            3) The error message of any
            4) The trace
        :param args: list of positional arguments
        required by the decorated function
        :param kwargs: list of keyword arguments
        required by the decorated function
        :return: None
        """
        try:
            result = func(*args, **kwargs)
            return result
        except BaseException as error:
            with open(_Path, 'a') as file:
                with redirect_stderr(file):
                    print(handle_indent('{:10} {}'.format("Date:", datetime.now())), file=sys.stderr)
                    print(handle_indent('{:10} {}'.format("Type:", type(error))), file=sys.stderr)
                    print(handle_indent('{:10} {}'.format("Message:", error)), file=sys.stderr)
                    print(handle_indent('{:10} {}'.format("Trace:", traceback.format_exc())), file=sys.stderr)
                    print(file=sys.stderr)

    return wrapper

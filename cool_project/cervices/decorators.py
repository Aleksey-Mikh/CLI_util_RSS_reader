from requests import exceptions
import shutil
from math import ceil

from cool_project.cervices.print_functions import (
    info_print, warning_print, error_print
)


def check_limit_type_value(func):
    """
    Decorator which check type of limit value.
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            if result.limit is not None:
                result.limit = int(result.limit)
        except ValueError:
            warning_print("You must enter the number in --limit params.")
        return result

    return wrapper


def intercept_errors(func):
    """Decorator which intercept a errors"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.ConnectionError:
            error_print("Connection error. Please check your URL")
        except exceptions.MissingSchema as exc:
            error_print(exc)
        except Exception as exc:
            error_print("Unknown error")

    return wrapper


def verbose_information_about_start_scrapping(func):
    """
    Decorator which print information about start and end scrapping
    """

    def wrapper(*args, **kwargs):
        if args[0].verbose:
            info_print("Start Scrapping")
            result = func(*args, **kwargs)
            info_print("Stop Scrapping")
        else:
            result = func(*args, **kwargs)

        return result

    return wrapper


def get_data_for_print_delimiter(word):
    """
    Get data for print separator for function

    :param word: a word which will be printed in center of a separator
    :return: left_columns_count, right_columns_count, word
    """
    columns = shutil.get_terminal_size().columns

    if word is None:
        word = ""
    else:
        word = f" {word} "

    columns_count = columns - len(word)
    left_columns_count = ceil(columns_count / 2)
    right_columns_count = columns_count - left_columns_count

    return left_columns_count, right_columns_count, word


def decorator_delimiter(start_word=None, end_word=None, calls_stat=False):
    """
    Decorator which print separate line with
    start_word and end_word value,
    if calls_stat is True also print how much times function was called,
    if start_word or end_word value is None value will not be print.

    :param start_word: a word which will be printed
    in center of a start separator
    :param end_word: a word which will be printed
    in center of a end separator
    :param calls_stat: print or not how much times function was called
    """
    count_of_calls = 1

    def decorator(func):

        def wrapper(*args, **kwargs):
            nonlocal count_of_calls, start_word
            word = start_word

            if calls_stat:
                if start_word is not None:
                    word = f"{start_word} {count_of_calls}"
                    count_of_calls += 1

            left_columns_count, right_columns_count, word = get_data_for_print_delimiter(word)
            print(
                f"{'-' * left_columns_count}{word}{'-' * right_columns_count}"
            )
            result = func(*args, **kwargs)
            left_columns_count, right_columns_count, word = get_data_for_print_delimiter(end_word)
            print(
                f"{'-' * left_columns_count}{word}{'-' * right_columns_count}"
            )

            return result

        return wrapper

    return decorator

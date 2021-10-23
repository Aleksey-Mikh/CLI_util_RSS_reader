import shutil
from math import ceil

from requests import exceptions
import pytest

from cool_project.cervices.decorators import (
    check_limit_type_value,
    intercept_errors,
    verbose_information_about_start_scrapping,
    get_data_for_print_delimiter,
    decorator_delimiter,
)


class Limit:

    def __init__(self, limit):
        self.limit = limit


def function_for_test(value):
    limit = Limit(value)
    return limit


def test_check_limit_type_value(capsys):
    dec_func = check_limit_type_value(function_for_test)
    assert dec_func(5).limit == 5

    dec_func = check_limit_type_value(function_for_test)
    assert dec_func("5").limit == 5

    dec_func = check_limit_type_value(function_for_test)
    dec_func("five")
    captured = capsys.readouterr()
    assert captured.out == "[WARNING] You must enter the number in --limit params.\n\n"

    dec_func = check_limit_type_value(function_for_test)
    assert dec_func(None).limit is None


def raise_exc(exc):
    if exc is None:
        return True
    raise exc


tasks_to_try = (
    (exceptions.ConnectionError, "[ERROR] Connection error. Please check your URL\n\n"),
    (exceptions.MissingSchema("Invalid URL 'httpslenta.r/rs': No schema supplied."),
     "[ERROR] Invalid URL 'httpslenta.r/rs': No schema supplied.\n\n"),
    (Exception, "[ERROR] Unknown error\n\n")
)


@pytest.mark.parametrize("exc, value", tasks_to_try)
def test_intercept_errors(capsys, exc, value):
    dec_func = intercept_errors(raise_exc)
    assert dec_func(None)

    dec_func = intercept_errors(raise_exc)
    dec_func(exc)
    captured = capsys.readouterr()
    assert captured.out == value


class Verbose:

    def __init__(self, verbose):
        self.verbose = verbose


def function_for_test_2(value):
    return value


def test_verbose_information_about_start_scrapping(capsys):
    dec_func = verbose_information_about_start_scrapping(function_for_test_2)
    res = dec_func(Verbose(True))
    captured = capsys.readouterr()
    assert captured.out == "[INFO] Start Scrapping\n\n[INFO] Stop Scrapping\n\n"
    assert res.verbose and isinstance(res.verbose, bool)

    dec_func = verbose_information_about_start_scrapping(function_for_test_2)
    res = dec_func(Verbose(False))
    assert not res.verbose and isinstance(res.verbose, bool)


def calculate_terminal_size(word):
    columns = shutil.get_terminal_size().columns

    if word is None:
        word = ""
    else:
        word = f" {word} "

    columns_count = columns - len(word)
    left_columns_count = ceil(columns_count / 2)
    right_columns_count = columns_count - left_columns_count
    return left_columns_count, right_columns_count, word


def test_get_data_for_print_delimiter():
    word = "FINISH HIM!"
    res = get_data_for_print_delimiter(word)
    assert res == calculate_terminal_size(word)

    word = None
    res = get_data_for_print_delimiter(word)
    assert res == calculate_terminal_size(word)


def test_decorator_delimiter(capsys):
    dec_func = decorator_delimiter("Fight")
    dec_func = dec_func(function_for_test_2)
    dec_func("POP")
    captured = capsys.readouterr()

    first_line = calculate_terminal_size("Fight")
    last_line = calculate_terminal_size(None)
    assert captured.out == f"{'-' * first_line[0]}{first_line[2]}{'-' * first_line[1]}\n" \
                           f"{'-' * last_line[0]}{last_line[2]}{'-' * last_line[1]}\n"

    dec_func = decorator_delimiter("Fight", "END", True)
    dec_func = dec_func(function_for_test_2)
    dec_func("POP")
    captured = capsys.readouterr()

    first_line = calculate_terminal_size("Fight 1")
    last_line = calculate_terminal_size("END")
    assert captured.out == f"{'-' * first_line[0]}{first_line[2]}{'-' * first_line[1]}\n" \
                           f"{'-' * last_line[0]}{last_line[2]}{'-' * last_line[1]}\n"

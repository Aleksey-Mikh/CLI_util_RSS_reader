from requests import exceptions

from print_functions import info_print, warning_print, error_print


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


def start_decorator(func):
    """
    Decorator which print information about start and end program
    """

    def wrapper(*args, **kwargs):
        number_of_separators = 20
        print(
            "---" * number_of_separators,
            "Start Program",
            "---" * number_of_separators,
            "\n\n",
        )
        result = func(*args, **kwargs)
        print()
        print(
            "---" * number_of_separators,
            "Stop Program",
            "---" * number_of_separators,
        )
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
            error_print(exc)
            return None

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


def delimiter_new_news(func):
    """Decorator which print delimiter of new news"""

    def wrapper(feed):
        print("\n")  # line break
        print("---" * 30)
        result = func(feed)
        print("---" * 30, end='')
        return result

    return wrapper

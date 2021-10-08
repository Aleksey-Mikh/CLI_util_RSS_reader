from print_functions import info_print, warning_print, error_print


def check_limit_type_value(func):

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

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            error_print(exc)
            return None

    return wrapper


def verbose_information_about_start_scrapping(func):

    def wrapper(*args, **kwargs):
        if args[0].verbose:
            info_print("Start Scrapping")
            result = func(*args, **kwargs)
            info_print("Stop Scrapping")
        else:
            result = func(*args, **kwargs)

        return result

    return wrapper


def delimiter_new_feed(func):

    def wrapper(feed):
        print("\n")  # line break
        result = func(feed)
        print()  # line break
        return result

    return wrapper

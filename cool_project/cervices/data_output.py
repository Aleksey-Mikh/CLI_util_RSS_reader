import json

from colorama import init, Fore, Style, deinit

from cool_project.cervices.decorators import decorator_delimiter


def console_output_feed(news, colorize):
    """
    Function which print news in console in standard format.

    :param colorize: the flag which shows that need paint output
    :param news: list of dicts which contains news information
    """
    print('\n')  # line break for correct output

    channel_data = news[0]
    if colorize:
        init(autoreset=True, strip=False)
        print(
            Style.BRIGHT + Fore.GREEN + f"Feed source:",
            f"{channel_data['source']}"
        )
        print(
            Style.BRIGHT + Fore.GREEN + f"Feed:",
            Fore.MAGENTA + f"{channel_data['channel_title']}" + Style.DIM,
            end="\n\n"
        )
    else:
        print(f"Feed source: {channel_data['source']}")
        print(f"Feed: {channel_data['channel_title']}", end="\n\n")

    for item in news[1:]:
        output_feed(item, colorize)
        print()  # line break for correct output

    if colorize:
        deinit()


@decorator_delimiter("News", calls_stat=True)
def output_feed(news, colorize):
    """
    Function which processing dictionary and if value is None
    don't print pair - key, value in console. If value contain text
    print pair - key, value which contain information about news.

    :param colorize: the flag which shows that need paint output
    :param news: dict which contain information about news
    """
    for key, value in news.items():
        if value is None or value == []:
            line_break(key)
        else:
            if isinstance(value, list):
                value = rebuild_value(value)

            line_break(key)

            if colorize:
                if key == "description" or key == "more_description":
                    print(
                        Style.BRIGHT + Fore.GREEN +
                        f"{key.title().replace('_', ' ')}:",
                        f"{value.replace('&nbsp', ' ')}"
                    )
                elif key == "title":
                    print(
                        Style.BRIGHT + Fore.RED +
                        f"{key.title().replace('_', ' ')}:",
                        Style.BRIGHT + Fore.YELLOW +
                        f"{value.replace('&nbsp', ' ')}"
                    )
                else:
                    print(
                        Style.BRIGHT + Fore.CYAN +
                        f"{key.title().replace('_', ' ')}:",
                        f"{value.replace('&nbsp', ' ')}"
                    )
            else:
                print(
                    f"{key.title().replace('_', ' ')}: "
                    f"{value.replace('&nbsp', ' ')}"
                )


def line_break(key):
    """
    Print line breaks when key in dict equals description or comments

    :param key: key of dictionary
    """
    if key == "description" or key == "comments":
        print()  # line break for correct output


def rebuild_value(value):
    """
    Function rebuild value to string

    :param value: value which is a list
    :return: string
    """
    value = ", ".join(value)
    return value


def console_json_output(data):
    """
    function which processing python data to json format
    and print it to the console.

    :param data: list of dicts which contains news information
    :return: list of dicts which contains news information
    """
    json_formatted_text = json.dumps(data, indent=4, ensure_ascii=False)
    print(json_formatted_text)

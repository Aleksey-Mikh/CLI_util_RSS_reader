import json

from cool_project.cervices.decorators import decorator_delimiter


def console_output_feed(news):
    """
    Function which print news in console in standard format.

    :param news: list of dicts which contains news information
    """
    print('\n')  # line break for correct output

    channel_data = news[0]
    print(f"Feed source: {channel_data['source']}")
    print(f"Feed: {channel_data['channel_title']}", end="\n\n")

    for item in news[1:]:
        output_feed(item)
        print()  # line break for correct output


@decorator_delimiter("News", calls_stat=True)
def output_feed(news):
    """
    Function which processing dictionary and if value is None
    don't print pair - key, value in console. If value contain text
    print pair - key, value which contain information about news.

    :param news: dict which contain information about news
    """
    for key, value in news.items():
        if value is None or value == []:
            line_break(key)
        else:
            if isinstance(value, list):
                value = rebuild_value(value)

            line_break(key)

            print(f"{key.title().replace('_', ' ')}: {value.replace('&nbsp', ' ')}")


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

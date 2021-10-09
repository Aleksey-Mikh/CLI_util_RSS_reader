import json

from decorators import delimiter_new_news


def console_output_feed(news):
    """
    Function which print news in console in standard format.

    :param news: list of dicts which contains news information
    """
    print('\n')
    channel_title = news[0]
    print(f"Channel title: {channel_title['channel_title']}")
    for item in news[1:]:
        output_feed(item)
    print()  # line break


@delimiter_new_news
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
        print()


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
    json_dump = json.dumps(data)
    json_obj = json.loads(json_dump)
    json_formatted_text = json.dumps(json_obj, indent=4, ensure_ascii=False)
    print(json_formatted_text)

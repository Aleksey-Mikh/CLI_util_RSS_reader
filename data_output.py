import json

from decorators import delimiter_new_feed


def console_output_feeds(feeds):
    print('\n')
    channel_title = feeds[0]
    print(f"Channel title: {channel_title['channel_title']}")
    for feed in feeds[1:]:
        output_feed(feed)


@delimiter_new_feed
def output_feed(feed):
    i = 0
    for key, value in feed.items():
        if value is None or value == []:
            line_break(i)
            i += 1
        else:
            if isinstance(value, list):
                value = rebuild_value(value)

            line_break(i)

            print(f"{key.title().replace('_', ' ')}: {value.replace('&nbsp', ' ')}")
            i += 1


def line_break(i):
    if i == 5 or i == 7:
        print()


def rebuild_value(value):
    value = ", ".join(value)
    return value


def console_json_output(data):
    json_dump = json.dumps(data)
    json_obj = json.loads(json_dump)
    json_formatted_text = json.dumps(json_obj, indent=4, ensure_ascii=False)
    print(json_formatted_text)

from decorators import delimiter_new_feed


def console_output_feeds(feeds):
    print('\n')
    channel_title = feeds[0]
    print(f"Channel title: {channel_title['channel_title']}")
    for feed in feeds[1:]:
        # print('\n\n')
        output_feed(feed)


@delimiter_new_feed
def output_feed(feed):
    i = 0
    for key, value in feed.items():
        if value is None:
            i += 1
            line_break(i)
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
    temp_str = ''

    for val in value:
        temp_str += val
    value = temp_str

    return value

#
# "title": title,
# "date": pub_date,
# "link": link,
# "author": author,
# "category": list_categories,
# "description": description,
# "more_description": content_encoded,
# "comments": comments,
# "media_object": enclosure,
# "extra_links": guid,
# "source_feed": list_source,
##JSON structure:

    [
        {
            "channel_title": channel_title
        },
        {
            "title": title,
            "date": pub_date,
            "link": link,
            "author": author,
            "category": list_categories,
            "description": description,
            "more_description": content_encoded,
            "comments": comments,
            "media_object": enclosure,
            "extra_links": guid,
            "source_feed": list_source,
        },
    ]

<b>channel_title*</b> - The title of the news channel from which the data was parsed.

<b>title*</b> - News title.

<b>date*</b> - Date of publication of the news.

<b>link*</b> - Link to the news.

<b>author*</b> - The author of the news.

<b>category*</b> - List of categories to which the news relates.

<b>description*</b> - Short description of the news.

<b>more_description*</b> - More complete description of the news.

<b>comments*</b> - Link to comments.

<b>media_object*</b> - Link to media objects.

<b>extra_links*</b> - Extra links.

<b>source_feed*</b> - Link to the news source.

*May contain null value if the element was not detected during news parsing.
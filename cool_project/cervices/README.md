Package description
===
This package contains modules which implement some services functions.

##data_output.py
The Module contains functions for output news in different format, for example: 
JSON or simple print in console.

###JSON structure:

    [
        {
        "channel_title": channel_title,
        "source": source,
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

<b>media_object*</b> - Links to media objects.

<b>extra_links*</b> - Extra links.

<b>source_feed*</b> - Link to the news source.

>*May contain null value if the element was not detected during news parsing.

###simple print:

    Channel source: https://people.onliner.by/feed
    Channel title: Люди Onlíner

    -------------------- News № --------------------
    title: title
    date: pub_date
    link: link
    author: author
    category: list_categories

    description: description
    more_description: content_encoded

    comments: comments
    media_object: enclosure
    extra_links: guid
    source_feed: list_source
    ------------------------------------------------

##print_functions.py
The Module contains print functions for print different messages, for example:
1. error messages print
2. warning messages print
3. info messages print

>those functions are calling during parsing process 

##decorators.py
The Module contains decorators functions for different use, for example:
+ decorators which print separators for output data
+ decorators which intercept exceptions
+ decorators which check input data

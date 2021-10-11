from bs4 import BeautifulSoup

from cool_project.cervices.print_functions import info_print, warning_print


def serialization_data(data, limit, verbose, source):
    """
    Function that processes the data with the soup class,
    gets the channel name and dictionaries with the news content
    and forms a list of it all.

    :param data: response text
    :param limit: limit of the news
    :param verbose: flag which means that program must print log information
    :param source: link that is used in parse print
    :return: list of the dicts which contains information about news
    """
    list_items = list()

    soup = BeautifulSoup(data, "xml")
    if not checking_the_source_is_the_rss(soup, verbose, source):  # finish work if get False
        return None

    channel = get_title_of_source(soup)
    list_items.append(channel)

    items = soup.find_all("item")
    count_news = len(items)
    limit = check_limit(limit, count_news)

    if verbose:
        info_print(f"Count of news: {limit}")
    gen = percent_generator(list_items, limit)

    for item in items[:limit]:
        list_items.append(serialization_item(item))

        if verbose:
            next(gen)

    return list_items


def get_title_of_source(soup):
    """
    Find channel title and return it or None.

    :param soup: BeautifulSoup object
    :return: dict which contain channel_title
    """
    try:
        channel_title = soup.find("title").get_text(strip=True)
    except AttributeError:
        channel_title = None

    channel = {"channel_title": channel_title}
    return channel


def percent_generator(list_items, limit):
    """
    Generator that prints information about the percent of program execution.

    :param list_items: list of dictionaries with received news
    :param limit: limit of the news
    """
    percent_of_one_items = 100 / limit
    percent_of_complete_program = percent_of_one_items
    while True:
        info_print(
            f"Feeds received [{len(list_items) - 1}/{limit}], "
            f"percent of execution program={int(percent_of_complete_program)}%"
        )
        yield
        percent_of_complete_program += percent_of_one_items


def checking_the_source_is_the_rss(soup, verbose, source):
    """
    Find element version in xml tree and print warning if source isn't RSS.

    :param soup: BeautifulSoup object
    :param verbose: flag which means that program must print log information
    :param source: link that is used in parse print
    :return: True if source is RSS or False if source isn't RSS
    """
    try:
        soup.find("rss").get("version")
        return True
    except AttributeError:
        warning_print(f"{source!r} isn't a RSS. Please try to enter a correct URL")
        if verbose:
            info_print("If your sure that this URL is correct, please check your URL, "
                       "maybe it use old rss version and parser don't understand it.")
        return False


def check_limit(limit, count_news):
    """
    Checked limit and if limit is None or limit > count_news
    redefined limit to count_news.

    :param limit: limit of the news
    :param count_news: the number of news on the site
    :return: updated limit
    """
    if limit is None or limit > count_news:
        limit = count_news
    return limit


def serialization_item(item):
    """
    Function that processes the news and gets the values of an element
    to build a dictionary that will contain information about the news.

    :param item: one news
    :return: dict which contain information about news
    """
    try:
        title = item.find("title").get_text(strip=True)
    except AttributeError:
        title = None

    try:
        link = item.find("link").get_text(strip=True)
    except AttributeError:
        link = None

    try:
        author = item.find("author").get_text(strip=True)
    except AttributeError:
        author = None

    try:
        description = item.find("description").get_text(strip=True)
        soup = BeautifulSoup(description, 'html.parser')
        description = soup.get_text()
    except AttributeError:
        description = None

    try:
        content_encoded = item.find("content:encoded").get_text(strip=True)
        soup = BeautifulSoup(content_encoded, 'html.parser')
        content_encoded = soup.get_text()
    except AttributeError:
        content_encoded = None

    try:
        list_categories = []
        categories = item.find_all("category")

        for category in categories:
            category_content = category.get_text(strip=True)
            list_categories.append(category_content)

    except AttributeError:
        list_categories = None

    try:
        comments = item.find("comments").get_text(strip=True)
    except AttributeError:
        comments = None

    try:
        enclosure = item.find("enclosure").get("url")
    except AttributeError:
        enclosure = None

    try:
        guid = item.find("guid").get_text(strip=True)
    except AttributeError:
        guid = None

    try:
        pub_date = item.find("pubDate").get_text(strip=True)
    except AttributeError:
        pub_date = None

    try:
        list_source = []
        source_content = item.find("source").get_text(strip=True)

        try:
            source_url = item.find("source").get("url")
        except AttributeError:
            source_url = ""

        list_source.extend([source_content + " ", source_url])
    except AttributeError:
        list_source = None

    # if description text in rss equals content_encoded text - getting rid of duplicates
    if description == content_encoded:
        content_encoded = None

    item_dict = {
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
    }

    return item_dict

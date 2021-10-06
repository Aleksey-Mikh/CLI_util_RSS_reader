from bs4 import BeautifulSoup


def serialization_data(data):
    soup = BeautifulSoup(data, 'xml')
    items = soup.find_all('item')
    list_items = list()
    for item in items[2:3]:
        list_items.append(serialization_item(item))

    return list_items


def serialization_item(item):
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
        source = item.find("source").get_text(strip=True)
    except AttributeError:
        source = None

    item_dict = {
        "title": title,
        "link": link,
        "author": author,
        "description": description,
        "category": list_categories,
        "comments": comments,
        "enclosure": enclosure,
        "guid": guid,
        "pub_date": pub_date,
        "source": source,
    }

    return item_dict

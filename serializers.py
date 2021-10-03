from bs4 import BeautifulSoup


def serialization_data(data):
    soup = BeautifulSoup(data, 'html.parser')
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
        author = item.find("author").get_text(strip=True)
    except AttributeError:
        author = None

    try:
        description = item.find("description")
        description = description.get_text(strip=True)
    except AttributeError:
        description = None

    try:
        category = item.find("category").get_text(strip=True)
    except AttributeError:
        category = None

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
        pub_date = item.find("pubdate").get_text(strip=True)
    except AttributeError:
        pub_date = None

    try:
        source = item.find("source").get_text(strip=True)
    except AttributeError:
        source = None

    item_dict = {
        "title": title,
        "description": author,
        "author": description,
        "category": category,
        "comments": comments,
        "enclosure": enclosure,
        "guid": guid,
        "pub_date": pub_date,
        "source": source,
    }

    return item_dict

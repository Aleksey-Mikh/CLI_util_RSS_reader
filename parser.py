import requests
from bs4 import BeautifulSoup


URL = "https://lenta.ru/rss"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "accept": "*/*"
}


def save_in_file(data, path):
    with open(path, "w", encoding="utf-8") as file:
        file.writelines(data)


def read_file(path):
    with open(path) as file:
        data = file.read()

    return data


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def get_data(data):
    pass


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        save_in_file(html.text, "lenta_rss.xml")
        # data = read_file("rss.xml")

    else:
        print("Error")

parse()



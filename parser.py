import requests
from bs4 import BeautifulSoup


URL = "https://news.yahoo.com/rss/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "accept": "*/*"
}


def save_in_file(data, path):
    with open(path, "w") as file:
        file.writelines(data)


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        save_in_file(html.text, "rss.xml")

parse()



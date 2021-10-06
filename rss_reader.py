import requests
import json
import argparse

from serializers import serialization_data


PROGRAM_VERSION = 0.6
URL = [
    "https://people.onliner.by/feed",
    "https://www.thecipherbrief.com/feed",
    'https://news.yahoo.com/rss/',
    'https://rss.art19.com/apology-line',
    'https://news.un.org/feed/subscribe/ru/news/region/europe/feed/rss.xml',
    'http://avangard-93.ru/news/rss',
    'http://avangard-93.ru/news/rss',
    'http://www.forbes.com/most-popular/feed/',
]
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "accept": "*/*",
    "Content-Type": "charset=UTF-8"
}


def save_in_file(data, path):
    print(data)
    with open(path, "w", encoding="utf-8") as file:
        file.writelines(data)


def read_file(path):
    with open(path, encoding='utf-8') as file:
        data = file.read()

    return data


def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    response.encoding = response.apparent_encoding
    return response


def parse():
    data_for_json = []
    for url in URL:
        print(url)
        html = get_html(url)
        if html.status_code == 200:
            # save_in_file(html.text, "lenta_rss.xml")
            # data = read_file("vedomosti_rss.xml")
            serializable_data = serialization_data(html.text)
            data_for_json.extend(serializable_data)
        else:
            print("Error")

    save_json(data_for_json, "data.json")


def main():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", type=str, help="Print version info")
    parser.add_argument("--version", action="version", version=f"Version {PROGRAM_VERSION}", help="RSS URL")
    parser.add_argument("--json", action='store_true', help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action='store_true', help="Outputs verbose status messages")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided")

    args, unknown = parser.parse_known_args()
    print(args)
    print(unknown)
    if "—version" in unknown:
        parser.parse_args(["--version"])


parse()
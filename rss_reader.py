import requests
import json
import argparse

from serializers import serialization_data


PROGRAM_VERSION = 1.2
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
    with open(path, encoding='utf-8') as file:
        data = file.read()

    return data


def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        # save_in_file(html.text, "lenta_rss.html")
        data = read_file("lenta_rss.html")
        serializable_data = serialization_data(data)
        save_json(serializable_data, "data.json")
    else:
        print("Error")


def main():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", type=str, help="Print version info")
    parser.add_argument("--version", action="version", version=f"Version {PROGRAM_VERSION}", help="RSS URL")
    parser.add_argument("--json", action='store_true', help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action='store_true', help="Outputs verbose status messages")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided")
    args = parser.parse_args()
    print(args)


main()

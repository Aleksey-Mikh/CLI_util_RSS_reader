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
    'http://www.forbes.com/most-popular/feed/',
]
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "accept": "*/*",
    "Content-Type": "charset=UTF-8"
}


def check_limit_type_value(func):

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            result.limit = int(result.limit)
        except ValueError:
            print("[WARNING] You must enter the number in --limit params.")
        return result

    return wrapper


def start_decorator(func):

    def wrapper(*args, **kwargs):
        print("---" * 20, "Start Scrapping", "---" * 20, end="\n\n")
        result = func(*args, **kwargs)
        print()
        print("---" * 20, "Stop Scrapping", "---" * 20)
        return result

    return wrapper


class RSSParser:

    def __init__(self):
        argparse_params = self._init_argparse()
        self.source = argparse_params.source
        self.limit = argparse_params.limit
        self.json = argparse_params.json
        self.verbose = argparse_params.verbose

    @staticmethod
    @check_limit_type_value
    def _init_argparse():
        parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
        parser.add_argument("source", type=str, help="Print version info")
        parser.add_argument("--version", action="version", version=f"Version {PROGRAM_VERSION}", help="RSS URL")
        parser.add_argument("--json", action='store_true', help="Print result as JSON in stdout")
        parser.add_argument("--verbose", action='store_true', help="Outputs verbose status messages")
        parser.add_argument("--limit", help="Limit news topics if this parameter provided")

        args, unknown = parser.parse_known_args()

        # If --version option is specified app should just print its version and stop.
        if "—version" in unknown:
            parser.parse_args(["--version"])
        else:
            return args

    def parsing(self):
        response = self._get_html()
        if response.status_code == 200:
            serializable_data = serialization_data(response.text, self.limit, self.verbose)
            self._save_data(serializable_data)
        else:
            self._check_error_status_code(response.status_code)

    def _get_html(self):
        response = requests.get(self.source, headers=HEADERS)

        # if site gives invalid encoding this line trying to correct encoding
        response.encoding = response.apparent_encoding
        return response

    def _check_error_status_code(self, status_code):
        if 400 <= status_code <= 499:
            if status_code == 404:
                self._print_error(f"[WARNING] {self.source} Not Found")
            else:
                self._print_error("[WARNING] Error seems to have been caused by the client. Check url which you give.")
        elif 500 <= status_code <= 599:
            self._print_error("[WARNING] The server failed to fulfil a request")
        else:
            self._print_error("[WARNING] Error which can't be processed because status code don't defined")

    @staticmethod
    def _print_error(message):
        print(message)

    @staticmethod
    def _save_data(serializable_data):
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(serializable_data, file, indent=4, ensure_ascii=False)


@start_decorator
def main():
    reader = RSSParser()
    reader.parsing()


if __name__ == '__main__':
    main()

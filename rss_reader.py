import requests
import json
import argparse

from serializers import serialization_data
from print_functions import info_print, warning_print, error_print
from data_output import console_output_feed, console_json_output
from decorators import (
    check_limit_type_value, start_decorator, intercept_errors, verbose_information_about_start_scrapping
)


PROGRAM_VERSION = 1.0
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


class RSSParser:

    def __init__(self):
        argparse_params = self._init_argparse()
        self.source = argparse_params.source
        self.limit = argparse_params.limit
        self.json = argparse_params.json
        self.verbose = argparse_params.verbose
        self.serializable_data = None

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

    @verbose_information_about_start_scrapping
    def parsing(self):
        response = self._get_html()

        if response is None:
            if self.verbose:
                info_print(f"Program stop running with error, when it try to get information from {self.source!r}")
            return False

        if response.status_code == 200:
            self.serializable_data = serialization_data(response.text, self.limit, self.verbose, self.source)

            if self.serializable_data is None:
                return False
            info_print("Receiving the news was successful")

            self._save_data(self.serializable_data)

        else:
            self._check_error_status_code(response.status_code)

    def print_data_in_console(self):
        if self.serializable_data is None:
            return False

        if self.json:
            console_json_output(self.serializable_data)
        else:
            console_output_feed(self.serializable_data)

    @intercept_errors
    def _get_html(self):
        response = requests.get(self.source, headers=HEADERS)

        # if site gives invalid encoding this line trying to correct it
        response.encoding = response.apparent_encoding
        return response

    def _check_error_status_code(self, status_code):
        if 400 <= status_code <= 499:
            if status_code == 404:
                error_print(f"{self.source!r} Not Found")
            else:
                error_print("Error seems to have been caused by the client. Check url which you give.")
        elif 500 <= status_code <= 599:
            error_print("The server failed to fulfil a request")
        else:
            error_print("Error which can't be processed because status code don't defined")

    @staticmethod
    def _save_data(serializable_data):
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(serializable_data, file, indent=4, ensure_ascii=False)


@start_decorator
@intercept_errors
def main(reader):
    reader.parsing()
    reader.print_data_in_console()


if __name__ == '__main__':
    reader = RSSParser()
    main(reader)

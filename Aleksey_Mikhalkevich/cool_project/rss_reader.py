import argparse
import requests


from cool_project.cervices.data_output import console_output_feed, console_json_output
from cool_project.cervices.decorators import (
    check_limit_type_value,
    intercept_errors,
    verbose_information_about_start_scrapping,
    decorator_delimiter,
)
from cool_project.cervices.print_functions import info_print, error_print
from cool_project.serializers.serializers import serialization_data
from cool_project.data_storage.working_with_storage import storage_control
from cool_project.project_settings import PROGRAM_VERSION, HEADERS


class RSSParser:
    """
    Class that regulates the parsing relationship between
    the user and the site that program are trying to parse.
    """

    def __init__(self):
        """
        Init class and init argparse
        """
        argparse_params = self._init_argparse()
        self.source = argparse_params.source
        self.limit = argparse_params.limit
        self.json = argparse_params.json
        self.verbose = argparse_params.verbose
        self.date = argparse_params.date
        self.to_html = argparse_params.to_html
        self.serializable_data = None

    @staticmethod
    @check_limit_type_value
    def _init_argparse():
        """
        Initialization argparse and check if --version option
        is specified app should just print its version and stop.

        :return: args of argparse
        """
        parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
        parser.add_argument("source", nargs="?", default=None, type=str, help="Print version info")
        parser.add_argument("--version", action="version", version=f"Version {PROGRAM_VERSION}", help="RSS URL")
        parser.add_argument("--json", action='store_true', help="Print result as JSON in stdout")
        parser.add_argument("--verbose", action='store_true', help="Outputs verbose status messages")
        parser.add_argument("--limit", help="Limit news topics if this parameter provided")
        parser.add_argument("--date", help="Take a date in %Y%m%d format. Example: 20191206")
        parser.add_argument("--to-html", help="This argument receives the path where new file will be saved.")

        args, unknown = parser.parse_known_args()

        # If --version option is specified app should just print its version and stop.
        if "—version" in unknown:
            parser.parse_args(["--version"])
        else:
            return args

    @verbose_information_about_start_scrapping
    def parsing(self):
        """
        Gets the response object and checks that it isvalid
        and call serialization_data to get serializable_data
        """
        response = self._get_html()

        if self._isvalid(response):
            serializable_data = serialization_data(response.text, self.limit, self.verbose, self.source)

            if serializable_data is None:
                error_print("Data wasn't received")
                return False

            info_print("Receiving the news was successful")
            self.serializable_data = serializable_data

    def _isvalid(self, response):
        """Check if response is valid"""
        if response is None:
            if self.verbose:
                info_print(f"The program stop running with error, when it try to get information from {self.source!r}")
            return False

        elif response.status_code == 200:
            return True
        else:
            self._check_error_status_code(response.status_code)

    def check_date_and_source(self):
        """
        Check date and source value and allowed standard start if
        source was enter and date is None, if source is None
        print error, if date was enter call storage_control.

        :return: True if source is enter and date is None
        """
        if self.date is None and self.source is not None:
            return True
        elif self.date is not None:
            storage_control(
                date=self.date, source=self.source, verbose=self.verbose,
                json=self.json, limit=self.limit, to_html=self.to_html
            )
        elif self.source is None:
            if self.verbose:
                info_print(f"Source is {self.source}")
            error_print("A source wasn't enter")

    def print_data_in_console(self):
        """
        Check the self.json value and
        if self.json is True - outputs json to the console
        if self.json is False - outputs news
        in a standard format to the console
        """
        if self.serializable_data is None:
            return False

        if self.json:
            if self.verbose:
                info_print("Output news in JSON format")
            console_json_output(self.serializable_data)
        else:
            if self.verbose:
                info_print("Output news in standard format")
            console_output_feed(self.serializable_data)

        storage_control(
            data=self.serializable_data, source=self.source, verbose=self.verbose, to_html=self.to_html
        )

    @intercept_errors
    def _get_html(self):
        """
        Executes a get request at the url specified by the user
        and check encoding of response data.

        :return response obj
        """
        response = requests.get(self.source, headers=HEADERS)

        # if site gives invalid encoding this line trying to correct it
        response.encoding = response.apparent_encoding
        return response

    def _check_error_status_code(self, status_code):
        """
        Check status code and print error message.

        :param status_code: http status code
        """
        if 400 <= status_code <= 499:
            if status_code == 404:
                error_print(f"{self.source!r}: 404 Page Not Found")
            else:
                error_print("Error seems to have been caused by the client. Check url which you give.")
        elif 500 <= status_code <= 599:
            error_print("The server failed to fulfil a request")
        else:
            error_print("Error which can't be processed because status code don't defined")


@decorator_delimiter("Start Program", "Stop Program")
# @intercept_errors  # TODO del #
def start_parsing(reader):
    """Load parsing and print data"""
    if reader.check_date_and_source():
        reader.parsing()
        reader.print_data_in_console()


def main():
    """Init reader"""
    reader = RSSParser()
    start_parsing(reader)


if __name__ == '__main__':
    main()

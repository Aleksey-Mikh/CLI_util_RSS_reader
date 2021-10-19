import json
import os
import re
from pathlib import Path
import datetime

from cool_project.cervices.print_functions import error_print, info_print
from cool_project.cervices.data_output import console_output_feed, console_json_output


LIST_OF_DATE_FORMATS = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y%m%d",
            "%Y-%m-%dT%H:%M:%SZ",
        ]


class StorageManager:
    """
    A base class for working with storage that implements methods
    for writing data to storage, reading from storage,
    getting paths, and converting dates.
    """

    def __init__(self, source, *, verbose, date=None, data=None):
        """
        Init StorageManager
        :param source: news source
        :param verbose: verbose mode
        :param date: the date on which you need to receive the news
        :param data: data to write to the storage
        """
        self.date = date
        self.source = source
        self.data = data
        self.verbose = verbose

    def _get_abspath_to_storage(self):
        """
        Getting the absolute path to this file.

        :return: absolute path to the file
        """
        abs_file_path = os.path.abspath(__file__)
        path, name = os.path.split(abs_file_path)
        path = self.get_path(path, "storage")
        return path

    @staticmethod
    def write_to_storage(path, data):
        """
        Writing data to the storage by the received path.

        :param path: the path where the data should be stored
        :param data: storage data
        """
        with open(path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def read_from_storage(path):
        """
        Reading data from storage by the received path.

        :param path: the path by which the data should be received
        """
        with open(path, encoding='utf-8') as File:
            data = json.load(File)
            return data

    @staticmethod
    def make_dir(path):
        """
        Creating a folder at the got path.
        If the folder already exists does nothing.

        :param path: the path where the folder should be created
        """
        if not Path(path).exists():
            p = Path(path)
            p.mkdir()

    @staticmethod
    def path_is_exists(path):
        """
        Check path exists.

        :param path: A path to check
        :return: True if a path exists, False if isn't exists
        """
        return Path(path).exists()

    @staticmethod
    def get_path(old_path, *args):
        """
        Getting a new path from the old one with the addition
        of an arbitrary number of components.

        :param old_path: old_path
        :param args: an arbitrary number of components for new path
        :return: new path
        """
        return Path(old_path, *args)

    @staticmethod
    def get_date_in_correct_format(date_str):
        """
        The method gets a string containing the date and
        converts it according to known formats.
        If the conversion failed returns None.

        :param date_str: a string containing the date
        :return: a date in format %Y-%m-%d or None
        """
        for date_format in LIST_OF_DATE_FORMATS:
            try:
                date_time_obj = datetime.datetime.strptime(date_str, date_format)
                return str(date_time_obj.date())
            except ValueError:
                # if the correct format wasn't received,
                # proceed to the next format in LIST_OF_DATE_FORMATS
                pass

        return None


class DataManagerInStorageAfterParsing(StorageManager):
    """
    A class that works with the storage when the program
    is running in the normal news parsing mode.
    Here the news is processed and added to the storage.
    """

    def __init__(self, source, *, data, verbose):
        """
        Init DataManagerInStorageAfterParsing
        :param source: news source
        :param verbose: verbose mode
        :param data: data to write to the storage
        """
        super().__init__(source, data=data, verbose=verbose)

    def get_file_name(self, date):
        """
        The method that gets the correct date of creation of the news
        and the source of the news and generates
        the file name by which the news will be saved.

        :param date: the correct date of creation of the news
        :return: file name
        """
        source = re.sub(r"\W", "_", self.source)
        file_name = f'{date}_{source}.json'
        return file_name

    def make_dir_by_key(self, data_dict):
        """
        Creating folders in which news will be stored.

        :param data_dict: dictionary with news
        """
        for key in data_dict.keys():
            path = self._get_abspath_to_storage()

            # key[:7] it is the year and the month in the format: 2021-10
            path = self.get_path(path, key[:7])
            self.make_dir(path)

            path = self.get_path(path, key)
            self.make_dir(path)

    def control_of_exist(self, data_dict, channel_data):
        """
        A method that checks if the file already exists.
        If the file exists, it runs the _write_or_update_data method
        with the `update' flag,
        if there is no file, it runs the _write_or_update_data method
        with the `write' flag.

        :param data_dict: dictionary with news
        :param channel_data: channel data
        """
        for date, list_of_news in data_dict.items():
            file_name = self.get_file_name(date)
            path = self._get_abspath_to_storage()
            path = self.get_path(path, date[:7], date, file_name)

            if self.path_is_exists(path):
                self._write_or_update_data(path, channel_data, list_of_news, "update")
            else:
                self._write_or_update_data(path, channel_data, list_of_news, "write")

    def _write_or_update_data(self, path, channel_data, list_of_news, flag):
        """
        If the flag is set to 'update', it reads data from the file
        and writes to the beginning of the file only those
        data that are not yet in the file.
        If the flag is set to 'write', it writes data to a file.

        :param path: the path to the file
        :param channel_data: channel data
        :param list_of_news: list of news
        :param flag: 'update' or 'write'
        """
        if flag == "update":
            data_from_file = self.read_from_storage(path)
            data_to_file = []

            for news in list_of_news:
                if news not in data_from_file:
                    data_to_file.append(news)

            # data_from_file[:1] - channel data
            data_to_file = data_from_file[:1] + data_to_file + data_from_file[1:]
            self.write_to_storage(path, data_to_file)
        elif flag == "write":
            data_to_file = channel_data + list_of_news
            self.write_to_storage(path, data_to_file)

    def split_data_by_news(self):
        """
        A method that splits the data received from the site by dates
        and writes it to the dictionary,
        where the key is the date and the value is a list of news.
        if the site uses dates in an unsupported format,
        it throws an error and returns None

        :return: (channel_data, dict_for_data_saving) or None
        """
        dict_for_data_saving = {}
        channel_data, data = self.data[:1], self.data[1:]

        for news in data:
            date_in_correct_format = self.get_date_in_correct_format(news["date"])

            if date_in_correct_format is None:
                error_print(f"The site {self.source} uses an unsupported date format. Storage data has failed.")
                if self.verbose is not None:
                    info_print("Supported date format:\n\t{}".format('\n\t'.join(LIST_OF_DATE_FORMATS)))
                return None

            dict_for_data_saving[date_in_correct_format] = dict_for_data_saving.get(date_in_correct_format, []) + [news]

        return channel_data, dict_for_data_saving


class FindManagerWhenEnterDate(StorageManager):
    """
    A class that implements data search by date
    """

    def __init__(self, source, *, date, verbose, json_flag, limit):
        """
        Init FindManagerWhenEnterDate

        :param source: news source
        :param verbose: verbose mode
        :param date: the date on which you need to receive the news
        :param json_flag: --json value
        :param limit: --limit value
        """
        self.json_flag = json_flag
        self.limit = limit
        super().__init__(source, date=date, verbose=verbose)

    def get_content_by_paths(self, paths):
        """
        A method that has received a list of paths corresponding
        to the date and collects news from files in this paths.

        :param paths: a list of paths
        :return: a list of dictionary with news
        """
        list_of_content = []
        for path in paths:
            data_from_file = self.read_from_storage(path)
            list_of_content.append(data_from_file)

        return list_of_content

    def slice_content_by_limit(self, list_of_content):
        """
        The method that slice the list of news
        by the limit set by the user.

        :param list_of_content: a list of dictionary with news
        :return: a list of dictionary with news
        """
        if self.limit is None:
            if self.verbose:
                list_of_sources = self.get_sources_from_data(list_of_content)
                info_print(
                    "According to the entered date, news was "
                    "received from the following sources: {}".format(
                        ", ".join(list_of_sources)
                    )
                )
            return list_of_content
        if self.limit <= 0:
            error_print("The limit is less than or equal to 0, news cannot be printed.")
            return False

        limit = self.limit
        new_list_of_content = []

        for data in list_of_content:
            channel_data, news = data[:1], data[1:]

            if limit < len(news):
                news = news[:limit]

                if news:
                    new_list_of_content.append(channel_data + news)
                break
            else:
                limit -= len(news)
                new_list_of_content.append(channel_data + news)

        if self.verbose:
            list_of_sources = self.get_sources_from_data(new_list_of_content)
            info_print(
                "According to the entered date, news was "
                "received from the following sources: {}".format(
                    ", ".join(list_of_sources)
                )
            )

        return new_list_of_content

    def check_news_by_date(self):
        """
        A method that verifies that there is news
        in the repository by the received date

        :return: False or list of paths
        """
        date_in_correct_format = self.get_date_in_correct_format(self.date)

        if date_in_correct_format is None:
            error_print(f"{self.date!r} is an incorrect date. Please try to enter the date in a correct format")
            return False

        path = self.get_path(self._get_abspath_to_storage(), date_in_correct_format[:7])

        if self.path_is_exists(path):
            path = self.get_path(path, date_in_correct_format)

            if self.path_is_exists(path):
                paths = Path(path).glob(f"{date_in_correct_format}*")
                paths = list(map(str, paths))
                return paths
            else:
                self._news_was_not_founded(date_in_correct_format)
                return False
        else:
            self._news_was_not_founded(date_in_correct_format)
            return False

    def data_output(self, data):
        """
        Output information on the terminal in JSON or standard format

        :param data: list with news
        """
        if self.json_flag:
            if len(data) == 1 and isinstance(data[0], list):
                data = data[0]
            if self.verbose:
                info_print("News will be printed in JSON format")
            console_json_output(data)
        else:
            if self.verbose:
                info_print("News will be printed in a standard format")
            for feed in data:
                console_output_feed(feed)

    @staticmethod
    def _news_was_not_founded(date):
        """
        Error output when news by date is not found.

        :param date: date entered by the user
        """
        error_print(f"No news was found for this date - {date}")

    @staticmethod
    def get_sources_from_data(list_of_data):
        """
        A method that receives a list of news and
        generates a list of sources of this news

        :param list_of_data: news list
        :return: list of news sources
        """
        list_of_sources = []
        for data in list_of_data:
            list_of_sources.append(data[0]["source"])
        return list_of_sources


class FindManagerWhenEnterDateAndSource(FindManagerWhenEnterDate):

    def __init__(self, source, *, date, verbose, json_flag, limit):
        super().__init__(source, date=date, verbose=verbose, json_flag=json_flag, limit=limit)

    def get_file_name(self):
        source = re.sub(r"\W", "_", self.source)
        file_name = f'{self.date}_{source}.json'
        return file_name

    def news_was_not_founded(self):
        error_print(f"No news was founded for this date and: {self.date}, and this source: {self.source}")

    def data_output(self, data):
        if self.json_flag:
            if self.verbose:
                info_print("News will be printed in JSON format")
            console_json_output(data)
        else:
            if self.verbose:
                info_print("News will be printed in a standard format")
            console_output_feed(data)

    def slice_content_by_limit(self, data):
        if self.verbose:
            info_print(f"The news was searched in the storage by date: {self.date}, and source: {self.source}")
        if self.limit is None:
            return data
        if self.limit <= 0:
            error_print("The limit is less than or equal to 0, news cannot be printed.")
            return False

        limit = self.limit
        channel_data, news = data[:1], data[1:]

        if limit < len(news):
            news = news[:limit]
        new_list_of_content = channel_data + news

        return new_list_of_content


def storage_control(*, date=None, source=None, data=None, verbose=None, **kwargs):
    # after parsing, writing a data to the storage
    if data is not None and source is not None:
        st_manager = DataManagerInStorageAfterParsing(source, data=data, verbose=verbose)
        response_from_split_data_by_news = st_manager.split_data_by_news()

        if response_from_split_data_by_news is None:
            return False

        channel_data, dict_for_data_saving = response_from_split_data_by_news
        st_manager.make_dir_by_key(dict_for_data_saving)
        st_manager.control_of_exist(dict_for_data_saving, channel_data)

    # if user enter only a date
    elif date is not None and source is None:
        json_flag, limit = kwargs["json"], kwargs["limit"]
        st_manager = FindManagerWhenEnterDate(source, date=date, verbose=verbose, json_flag=json_flag, limit=limit)
        paths = st_manager.check_news_by_date()

        if not paths:
            return False

        list_of_content = st_manager.get_content_by_paths(paths)
        if verbose:
            info_print("The news has been successfully extracted from the storage")
        list_of_content = st_manager.slice_content_by_limit(list_of_content)
        if not list_of_content:
            return False
        st_manager.data_output(list_of_content)

    # if user enter a date and a source
    elif date is not None and source is not None:
        json_flag, limit = kwargs["json"], kwargs["limit"]
        st_manager = FindManagerWhenEnterDateAndSource(
            source, date=date, verbose=verbose, json_flag=json_flag, limit=limit
        )
        paths = st_manager.check_news_by_date()
        st_manager.date = st_manager.get_date_in_correct_format(date)

        if not paths:
            return False
        file_name = st_manager.get_file_name()

        path = list(filter(lambda x: x[-len(file_name):] == file_name, paths))
        if not path:
            st_manager.news_was_not_founded()
            return False

        data = st_manager.read_from_storage(path[0])
        if verbose:
            info_print("The news has been successfully extracted from the storage")

        data = st_manager.slice_content_by_limit(data)
        if not data:
            return False
        st_manager.data_output(data)

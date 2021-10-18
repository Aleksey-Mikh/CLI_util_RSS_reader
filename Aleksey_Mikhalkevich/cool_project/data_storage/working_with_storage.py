import json
import os
import re
from pathlib import Path
import datetime

from cool_project.cervices.print_functions import error_print, warning_print, info_print
from cool_project.cervices.data_output import console_output_feed, console_json_output


LIST_OF_DATE_FORMATS = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y%m%d",
            "%Y-%m-%dT%H:%M:%SZ",
        ]


class StorageManager:

    def __init__(self, source, *, verbose, date=None, data=None):
        self.date = date
        self.source = source
        self.data = data
        self.verbose = verbose

    def _get_abspath_to_storage(self):
        abs_file_path = os.path.abspath(__file__)
        path, name = os.path.split(abs_file_path)
        path = self.get_path(path, "storage")
        return path

    @staticmethod
    def write_to_storage(path, data):
        with open(path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def read_from_storage(path):
        with open(path, encoding='utf-8') as File:
            data = json.load(File)
            return data

    @staticmethod
    def make_dir(path):
        if not Path(path).exists():
            p = Path(path)
            p.mkdir()

    @staticmethod
    def path_is_exists(path):
        return Path(path).exists()

    @staticmethod
    def get_path(old_path, *args):
        return Path(old_path, *args)

    @staticmethod
    def get_date_in_correct_format(date_str):
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

    def __init__(self, source, *, data, verbose):
        super().__init__(source, data=data, verbose=verbose)

    def get_file_name(self, date):
        """case when program after parsing"""
        source = re.sub(r"\W", "_", self.source)
        file_name = f'{date}_{source}.json'

        return file_name

    def make_dir_by_key(self, data_dict):
        for key in data_dict.keys():
            path = self._get_abspath_to_storage()

            # key[:7] it is the year and the month in the format: 2021-10
            path = self.get_path(path, key[:7])
            self.make_dir(path)

            path = self.get_path(path, key)
            self.make_dir(path)

    def control_of_exist(self, data_dict, channel_data):
        for date, list_of_news in data_dict.items():
            file_name = self.get_file_name(date)
            path = self._get_abspath_to_storage()
            path = self.get_path(path, date[:7], date, file_name)

            if self.path_is_exists(path):
                self._write_or_update_data(path, channel_data, list_of_news, "update")
            else:
                self._write_or_update_data(path, channel_data, list_of_news, "write")

    def _write_or_update_data(self, path, channel_data, list_of_news, flag):
        if flag == "update":
            data_from_file = self.read_from_storage(path)
            data_to_file = []

            for news in list_of_news:
                if news not in data_from_file:
                    data_to_file.append(news)
                    info_print("Data in storage was updated")

            # data_from_file[:1] - channel data
            data_to_file = data_from_file[:1] + data_to_file + data_from_file[1:]
            self.write_to_storage(path, data_to_file)
        elif flag == "write":
            data_to_file = channel_data + list_of_news
            self.write_to_storage(path, data_to_file)

    def split_data_by_news(self):
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

    def __init__(self, source, *, date, verbose, json_flag, limit):
        self.json_flag = json_flag
        self.limit = limit
        super().__init__(source, date=date, verbose=verbose)

    @staticmethod
    def _news_was_not_founded(date):
        error_print(f"No news was found for this date - {date}")

    def get_content_by_paths(self, paths):
        list_of_content = []
        for path in paths:
            data_from_file = self.read_from_storage(path)
            list_of_content.append(data_from_file)

        return list_of_content

    def slice_content_by_limit(self, list_of_content):
        if self.limit is None:
            return list_of_content

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

    @staticmethod
    def get_sources_from_data(list_of_data):
        list_of_sources = []
        for data in list_of_data:
            list_of_sources.append(data[0]["source"])
        return list_of_sources

    def check_news_by_date(self):
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
        if self.json_flag:
            if len(data) == 1:
                data = data[0]
            if self.verbose:
                info_print("News will be printed in JSON format")
            console_json_output(data)
        else:
            if self.verbose:
                info_print("News will be printed in a standard format")
            for feed in data:
                console_output_feed(feed)


def storage_control(*, date=None, source=None, data=None, verbose=None, **kwargs):
    # after parsing, writing data to the storage
    if data is not None and source is not None:
        st_manager = DataManagerInStorageAfterParsing(source, data=data, verbose=verbose)
        response_from_split_data_by_news = st_manager.split_data_by_news()

        if response_from_split_data_by_news is None:
            return False

        channel_data, dict_for_data_saving = response_from_split_data_by_news
        st_manager.make_dir_by_key(dict_for_data_saving)
        st_manager.control_of_exist(dict_for_data_saving, channel_data)

    # if user enter only date
    elif date is not None and source is None:
        json_flag, limit = kwargs["json"], kwargs["limit"]
        st_manager = FindManagerWhenEnterDate(source, date=date, verbose=verbose, json_flag=json_flag, limit=limit)
        paths = st_manager.check_news_by_date()

        if not paths:
            return False

        list_of_content = st_manager.get_content_by_paths(paths)
        if verbose:
            info_print("The news has been extracted from the storage")
        list_of_content = st_manager.slice_content_by_limit(list_of_content)
        st_manager.data_output(list_of_content)

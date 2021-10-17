import json
import os
import re
from pathlib import Path
import datetime

from cool_project.cervices.print_functions import error_print, warning_print, info_print


class StorageManager:

    def __init__(self, source, date=None, data=None):
        self.date = date
        self.source = source
        self.data = data

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
    def check_path(path):
        return Path(path).exists()

    def get_file_name(self, date):
        """case when program after parsing"""
        source = re.sub(r"\W", "_", self.source)
        file_name = f'{date}_{source}.json'

        return file_name

    @staticmethod
    def get_path(old_path, *args):
        return Path(old_path, *args)

    @staticmethod
    def get_date_in_correct_format(date_str):
        list_of_date_formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y%m%d",
            "%Y-%m-%dT%H:%M:%SZ",
        ]
        for date_format in list_of_date_formats:
            try:
                date_time_obj = datetime.datetime.strptime(date_str, date_format)
                return str(date_time_obj.date())
            except ValueError:
                # if the correct format wasn't received,
                # proceed to the next format in list_of_date_formats
                pass

        return None

    def split_data_by_news(self):
        dict_for_data_saving = {}
        channel_data, data = self.data[:1], self.data[1:]

        for news in data:
            date_in_correct_format = self.get_date_in_correct_format(news["date"])

            if date_in_correct_format is None:
                error_print(f"The site {self.source} uses an unsupported date format. Storage data has failed.")
                return None

            dict_for_data_saving[date_in_correct_format] = dict_for_data_saving.get(date_in_correct_format, []) + [news]

        return channel_data, dict_for_data_saving

    @staticmethod
    def _get_abspath():
        abs_file_path = os.path.abspath(__file__)
        path, name = os.path.split(abs_file_path)
        return path

    def make_dir_by_key(self, data_dict):
        for key in data_dict.keys():
            path = self._get_abspath()

            # key[:7] it is the year and the month in the format: 2021-10
            path = self.get_path(path, "storage", key[:7])
            self.make_dir(path)

            path = self.get_path(path, key)
            self.make_dir(path)

    def control_of_exist(self, data_dict, channel_data):
        for date, list_of_news in data_dict.items():
            file_name = self.get_file_name(date)
            path = self._get_abspath()
            path = self.get_path(path, "storage", date[:7], date, file_name)

            if self.check_path(path):
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
                    print("file was updated")

            # data_from_file[:1] - channel data
            data_to_file = data_from_file[:1] + data_to_file + data_from_file[1:]
            self.write_to_storage(path, data_to_file)
        elif flag == "write":
            data_to_file = channel_data + list_of_news
            self.write_to_storage(path, data_to_file)


def storage_control(*, date=None, source=None, data=None):
    if data is not None and source is not None:  # after parsing, writing data to the storage
        st_manager = StorageManager(source, data=data)
        response_from_split_data_by_news = st_manager.split_data_by_news()

        if response_from_split_data_by_news is None:
            return False

        channel_data, dict_for_data_saving = response_from_split_data_by_news
        st_manager.make_dir_by_key(dict_for_data_saving)
        st_manager.control_of_exist(dict_for_data_saving, channel_data)



    #     st_manager = StorageManager(source, data=data)
    #     file_name = st_manager.get_file_name()
    #
    #     abs_file_path = os.path.abspath(__file__)
    #     path, name = os.path.split(abs_file_path)
    #
    #     path = st_manager.get_path(path, "storage", file_name[:7])
    #     st_manager.make_dir(path)
    #
    #     path = st_manager.get_path(path, file_name)
    #     st_manager.write_to_storage(path)
    # elif date is not None and source is None:
    #     st_manager = StorageManager(date=date)
    #     file_name = st_manager.get_file_name()
    #
    #     abs_file_path = os.path.abspath(__file__)
    #     path, name = os.path.split(abs_file_path)
    #
    #     path = st_manager.get_path(path, "storage", file_name[:7])


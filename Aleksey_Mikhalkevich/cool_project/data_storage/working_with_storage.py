import json
import os
import re
from pathlib import Path
import datetime


class StorageManager:

    def __init__(self, source, date=None, data=None):
        self.date = date
        self.source = source
        self.data = data

    def write_to_storage(self, path):
        with open(path, "w", encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

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
            print('lol')

    @staticmethod
    def check_path(path):
        return Path(path).exists()

    def get_file_name(self):
        if self.data is None:
            date_in_correct_format = self._get_date_in_correct_format(self.date)
        else:
            date_in_correct_format = self._get_date_in_correct_format(self.data[1]["date"])

        if date_in_correct_format is None:
            return None

        source = re.sub(r"\W", "_", self.source)
        file_name = f'{date_in_correct_format}_{source}.json'

        return file_name

    @staticmethod
    def get_path(old_path, *args):
        return Path(old_path, *args)

    @staticmethod
    def _get_date_in_correct_format(date_str):
        list_of_date_formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y%m%d"
        ]
        for date_format in list_of_date_formats:
            try:
                date_time_obj = datetime.datetime.strptime(date_str, date_format)
                return date_time_obj.date()
            except ValueError:
                # if the correct format wasn't received,
                # proceed to the next format in list_of_date_formats
                pass

        return None


def storage_control(*, date=None, source=None, data=None):
    if data is not None and source is not None:  # after parsing, writing data to the storage
        st_manager = StorageManager(source, data=data)
        file_name = st_manager.get_file_name()

        abs_file_path = os.path.abspath(__file__)
        path, name = os.path.split(abs_file_path)

        path = st_manager.get_path(path, "storage", file_name[:7])
        st_manager.make_dir(path)

        path = st_manager.get_path(path, file_name)
        st_manager.write_to_storage(path)

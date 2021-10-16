import json
import re
from pathlib import Path
import datetime


class StorageManager:

    def __init__(self, date, source):
        self.date = date
        self.source = source

    def write_to_storage(self, data):
        path = self.get_path(data)

        with open(path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def read_from_storage(self, path):
        with open(path, encoding='utf-8') as File:
            data = json.load(File)
            return data

    def make_dir(self, path):
        if Path(path).exists():
            p = Path(path)
            p.mkdir()

    def check_path(self, path):
        return Path(path).exists()

    def get_path(self, data):
        source = data[0]["source"]
        pattern = r"\W"
        source = re.sub(pattern, "_", source)

        date_time = self.get_date(data[1]["date"])
        path = Path(Path.cwd(), "storage", f'{date_time}_{source}.json')

        return path

    def get_date(self, date_str):
        list_of_date_formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y%m%d"
        ]
        for date_format in list_of_date_formats:
            try:
                date_time_obj = datetime.datetime.strptime(date_str, date_format)
            except ValueError:
                date_time_obj = None

            if date_time_obj is not None:
                break

        if date_time_obj is None:
            return False

        return date_time_obj.date()


def storage_control(date, source):
    st_manager = StorageManager(date, source)
    date_time_obj = st_manager.get_date(date)
    if date_time_obj:
        ...
    else:
        return False

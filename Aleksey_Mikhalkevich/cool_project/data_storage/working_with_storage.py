import json
import re
from pathlib import Path
import datetime


def write_to_storage(data):
    path = get_path(data)

    with open(path, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def read_from_storage(path):
    with open(path, encoding='utf-8') as File:
        data = json.load(File)
        return data


def make_dir(path):
    if Path(path).exists():
        p = Path(path)
        p.mkdir()


def check_path(path):
    return Path(path).exists()


def get_path(data):
    source = data[0]["source"]
    pattern = r"\W"
    source = re.sub(pattern, "_", source)

    date_time = get_date(data[1]["date"])
    path = Path(Path.cwd(), "storage", f'{date_time}_{source}.json')

    return path


def get_date(date_str):
    format_date = "%a, %d %b %Y %H:%M:%S %z"
    date_time_obj = datetime.datetime.strptime(date_str, format_date)
    return date_time_obj.date()

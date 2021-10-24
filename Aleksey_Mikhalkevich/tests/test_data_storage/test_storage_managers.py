import shutil
from math import ceil
from pathlib import Path
from unittest import mock

import pytest

from cool_project.data_storage.storage_managers import (
    StorageManager as SM,
    DataManagerInStorageAfterParsing,
    FindManagerWhenEnterDate,
    FindManagerWhenEnterDateAndSource
)


@pytest.fixture()
def init_SM():
    data = ["data"]
    st_manager = SM("sour.ce", verbose=True, data=data)
    return st_manager


@pytest.fixture()
def init_DataManagerInStorageAfterParsing():
    data = [
        {
            "channel_title": "Люди Onlíner",
            "source": "source"
        },
        {
            "title": "Пиневич: 40% коечного фонда перепрофилировано под ковидных пациентов",
            "date": "Sat, 23 Oct 2021 17:51:11 +0300",
            "link": "https://people.onliner.by/2021/10/23/pereprofilirovano-pod-kovidnyx-pacientov",
            "author": None,
            "category": ["Здоровье"],
            "description": 'По всей стране в медицинских учреждениях '
                           'перепрофилировано чуть более 40% коечного фонда. '
                           'Такую цифру привел глава Министерства '
                           'здравоохранения Дмитрий Пиневич, '
                           'отметив, что это позволяет и '
                           'дальше оказывать плановую помощь '
                           'жителям Беларуси.Читать далее…',
            "more_description": None,
            "comments": None,
            "media_object": ["https://content.onliner.by/news/thumbnail/5a7aa9c81d307b0ddc03a0f10746bffe.jpeg"],
            "extra_links": "https://people.onliner.by/2021/10/23/pereprofilirovano-pod-kovidnyx-pacientov",
            "source_feed": None,
        }
    ]
    st_manager = DataManagerInStorageAfterParsing("sour.ce", verbose=True, data=data)
    return st_manager


@pytest.fixture()
def init_FindManagerWhenEnterDateAndSource():
    st_manager = FindManagerWhenEnterDateAndSource(
        "sour.ce", verbose=True, date="1000-10-23", json_flag=True, limit=1
    )
    return st_manager


@pytest.fixture()
def init_FindManagerWhenEnterDate():
    st_manager = FindManagerWhenEnterDate(
        "sour.ce", verbose=True, date="1000-10-23", json_flag=True, limit=1
    )
    return st_manager


@pytest.fixture()
def del_dir():
    """A fixture that deletes a directory"""
    path = Path(Path(__file__).parent, "test_dir")
    yield path
    Path.rmdir(path)


@pytest.fixture()
def path_to_storage():
    path = Path(__file__).parent.parent.parent
    path = Path(path, "cool_project", "data_storage", "storage")
    return path


@pytest.fixture()
def del_file_txt():
    """A fixture that deletes file"""
    path = Path(Path(__file__).parent, "feed.txt")
    yield
    Path.unlink(path)


def test_StorageManager_mehod_get_abspath_to_storage(init_SM, path_to_storage):
    st_manger = init_SM
    path = st_manger._get_abspath_to_storage()
    assert path == path_to_storage


def test_StoragerManager_mehod_write_to_storage(del_file_txt, init_SM):
    path = Path(Path(__file__).parent, "feed.txt")
    st_manager = init_SM
    st_manager.write_to_storage(path, 'data')
    assert Path(path).exists()


def test_StorageManager_mehod_read_from_storage(init_SM):
    path = Path(Path(__file__).parent, "test_data.json")
    st_manager = init_SM
    result = st_manager.read_from_storage(path)
    assert result == [{"test": "data"}]


def test_StorageManager_mehod_make_dir(init_SM, del_dir):
    path = del_dir
    st_manager = init_SM
    st_manager.make_dir(path)
    assert Path(path).exists()


def test_StorageManager_mehod_path_is_exists(init_SM):
    path = Path(__file__)
    st_manager = init_SM
    assert st_manager.path_is_exists(path)

    path = Path(Path(__file__), "fake")
    assert not st_manager.path_is_exists(path)


def test_StorageManager_mehod_get_path(init_SM):
    expected = Path(Path(__file__), "check")
    st_manager = init_SM
    actual = st_manager.get_path(Path(__file__), "check")
    assert actual == expected


@pytest.mark.parametrize("date_str, correct_res",
                         [("Sat, 23 Oct 2021 17:51:11 +0300", "2021-10-23"),
                          ("Sat, 23 Oct 2021 some inf", None),
                          ("20211024", "2021-10-24"),
                          ("22024", None)]
                         )
def test_StorageManager_mehod_get_date_in_correct_format(init_SM, date_str, correct_res):
    st_manager = init_SM
    actual = st_manager.get_date_in_correct_format(date_str)
    assert actual == correct_res


def test_DataManagerInStorageAfterParsing_mehod_get_file_name(init_DataManagerInStorageAfterParsing):
    st_manager = init_DataManagerInStorageAfterParsing
    actual = st_manager.get_file_name("2021-10-22")
    expected = "2021-10-22_sour_ce.json"
    assert actual == expected


def test_DataManagerInStorageAfterParsing_mehod_make_dir_by_key(
        init_DataManagerInStorageAfterParsing, path_to_storage
):
    st_manager = init_DataManagerInStorageAfterParsing
    data = {"1000-10-23": "data"}
    expected = Path(path_to_storage, "1000-10", "1000-10-23")
    st_manager.make_dir_by_key(data)
    assert Path(expected).exists()
    shutil.rmtree(Path(path_to_storage, "1000-10"))


def test_DataManagerInStorageAfterParsing_mehod_control_of_exist(
        init_DataManagerInStorageAfterParsing, path_to_storage
):
    st_manager = init_DataManagerInStorageAfterParsing
    data = {"1000-10-23": [{"data": "data"}]}
    channel_data = [{"channel_data": "data"}]
    st_manager.make_dir_by_key(data)
    st_manager.control_of_exist(data, channel_data)
    expected = Path(path_to_storage, "1000-10", "1000-10-23")
    assert Path(expected).exists()

    data = {"1000-10-23": [{"data2": "data2"}]}
    st_manager.control_of_exist(data, channel_data)
    assert Path(expected).exists()
    shutil.rmtree(Path(path_to_storage, "1000-10"))


def test_DataManagerInStorageAfterParsing_mehod_split_data_by_news(init_DataManagerInStorageAfterParsing, capsys):
    st_manager = init_DataManagerInStorageAfterParsing
    channel_data, dict_for_data_saving = st_manager.split_data_by_news()
    channel_data_correct = [{
        "channel_title": "Люди Onlíner",
        "source": "source"
    }]
    dict_for_data_saving_correct = {
        "2021-10-23": [
            {
                "title": "Пиневич: 40% коечного фонда перепрофилировано под ковидных пациентов",
                "date": "Sat, 23 Oct 2021 17:51:11 +0300",
                "link": "https://people.onliner.by/2021/10/23/pereprofilirovano-pod-kovidnyx-pacientov",
                "author": None,
                "category": ["Здоровье"],
                "description": 'По всей стране в медицинских учреждениях '
                               'перепрофилировано чуть более 40% коечного фонда. '
                               'Такую цифру привел глава Министерства '
                               'здравоохранения Дмитрий Пиневич, '
                               'отметив, что это позволяет и '
                               'дальше оказывать плановую помощь '
                               'жителям Беларуси.Читать далее…',
                "more_description": None,
                "comments": None,
                "media_object": ["https://content.onliner.by/news/thumbnail/5a7aa9c81d307b0ddc03a0f10746bffe.jpeg"],
                "extra_links": "https://people.onliner.by/2021/10/23/pereprofilirovano-pod-kovidnyx-pacientov",
                "source_feed": None,
            }
        ]
    }
    captured = capsys.readouterr()
    assert (channel_data, dict_for_data_saving) == (channel_data_correct, dict_for_data_saving_correct)
    assert captured.out == ""

    data = [
        {
            "channel_title": "Люди Onlíner",
            "source": "source"
        },
        {
            "title": "Пиневич: 40% коечного фонда перепрофилировано под ковидных пациентов",
            "date": "Sat, 23 Oct 021 17:51:11 +0300",
            "link": "https://people.onliner.by/2021/10/23/pereprofilirovano-pod-kovidnyx-pacientov",
            "author": None,
        }
    ]
    st_manager = DataManagerInStorageAfterParsing("sour.ce", verbose=True, data=data)
    actual = st_manager.split_data_by_news()
    captured = capsys.readouterr()

    # captured.out[82:] - supported dates. Supported dates may change
    assert captured.out[:82] == f"[ERROR] The site sour.ce uses an" \
                                f" unsupported date format. " \
                                f"Storage data has failed."
    assert actual is None


def test_FindManagerWhenEnterDateAndSource_mehod_get_file_name(init_FindManagerWhenEnterDateAndSource):
    st_manager = init_FindManagerWhenEnterDateAndSource
    file_name = st_manager.get_file_name()
    assert file_name == "1000-10-23_sour_ce.json"


def test_FindManagerWhenEnterDateAndSource_mehod_news_was_not_founded(init_FindManagerWhenEnterDateAndSource, capsys):
    st_manager = init_FindManagerWhenEnterDateAndSource
    st_manager.news_was_not_founded()
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] No news was founded " \
                           "for this date and: 1000-10-23," \
                           " and this source: sour.ce\n\n"


def calculate_terminal_size(word):
    """
    calculated terminal size
    :param word: a word which will be printed in center of a separator
    :return: left_columns_count, right_columns_count, word
    """
    columns = shutil.get_terminal_size().columns

    if word is None:
        word = ""
    else:
        word = f" {word} "

    columns_count = columns - len(word)
    left_columns_count = ceil(columns_count / 2)
    right_columns_count = columns_count - left_columns_count
    return left_columns_count, right_columns_count, word


def test_FindManagerWhenEnterDateAndSource_mehod_data_output(
        init_FindManagerWhenEnterDateAndSource, capsys
):
    st_manager = init_FindManagerWhenEnterDateAndSource
    data = [{"data": "LOL"}]
    st_manager.data_output(data)
    captured = capsys.readouterr()
    assert captured.out == "[INFO] News will be printed in JSON format\n\n" \
                           "[\n" \
                           "    {\n" \
                           "        \"data\": \"LOL\"\n" \
                           "    }\n" \
                           "]\n"

    st_manager = FindManagerWhenEnterDateAndSource(
        "sour.ce", verbose=True, date="1000-10-23", json_flag=None, limit=1
    )
    data = [
        {
            "channel_title": "channel_title",
            "source": "source"
        },
        {
            "title": "title",
            "date": "date",
            "link": "link",
            "author": None,
            "category": ["Здоровье"],
            "description": 'description',
            "more_description": None,
            "comments": None,
            "media_object": "media_object",
            "extra_links": "extra_links",
            "source_feed": None,
        }
    ]
    st_manager.data_output(data)
    captured = capsys.readouterr()
    first_line_1 = calculate_terminal_size("News 1")
    last_line = calculate_terminal_size(None)
    assert captured.out == f"[INFO] News will be printed in a standard format\n\n" \
                           f"\n\nFeed source: source\n" \
                           f"Feed: channel_title\n\n" \
                           f"{'-' * first_line_1[0]}{first_line_1[2]}{'-' * first_line_1[1]}\n" \
                           f"Title: title\n" \
                           f"Date: date\n" \
                           f"Link: link\n" \
                           f"Category: Здоровье\n\n" \
                           f"Description: description\n\n" \
                           f"Media Object: media_object\n" \
                           f"Extra Links: extra_links\n" \
                           f"{'-' * last_line[0]}{last_line[2]}{'-' * last_line[1]}\n\n"


def test_FindManagerWhenEnterDateAndSource_mehod_slice_content_by_limit(
        init_FindManagerWhenEnterDateAndSource, capsys
):
    st_manager = init_FindManagerWhenEnterDateAndSource
    data = [
        {"channel_title": "Люди Onlíner"},
        {"2021-10-23": {"title": "title"}},
        {"2021-10-23": {"title": "title"}}
    ]
    actual = st_manager.slice_content_by_limit(data)
    capsys.readouterr()
    assert actual == data[:-1]

    st_manager = FindManagerWhenEnterDateAndSource(
        "sour.ce", verbose=True, date="1000-10-23", json_flag=True, limit=None
    )
    actual = st_manager.slice_content_by_limit(data)
    capsys.readouterr()
    assert actual == data

    st_manager = FindManagerWhenEnterDateAndSource(
        "sour.ce", verbose=True, date="1000-10-23", json_flag=True, limit=-3
    )
    st_manager.slice_content_by_limit(data)
    captured = capsys.readouterr()
    assert captured.out == "[INFO] The news was searched in the " \
                           "storage by date: 1000-10-23, " \
                           "and source: sour.ce\n\n" \
                           "[ERROR] The limit is less than or equal" \
                           " to 0, news cannot be printed.\n\n"


def test_FindManagerWhenEnterDate_mehod_get_content_by_paths(init_FindManagerWhenEnterDate):
    st_manager = init_FindManagerWhenEnterDate
    path = Path(Path(__file__).parent, "test_data.json")
    list_of_content = st_manager.get_content_by_paths([path])
    assert list_of_content == [[{'test': 'data'}]]


def test_FindManagerWhenEnterDate_mehod_slice_content_by_limit(init_FindManagerWhenEnterDate, capsys):
    st_manager = init_FindManagerWhenEnterDate
    data = [
        {"source": "Люди Onlíner"},
        {"2021-10-23": {"title": "title"}},
        {"2021-10-23": {"title": "title"}}
    ]
    actual = st_manager.slice_content_by_limit([data])
    capsys.readouterr()
    assert actual == [data[:-1]]

    st_manager = FindManagerWhenEnterDate(
        "sour.ce", verbose=True, date="1000-10-23", json_flag=True, limit=None
    )
    actual = st_manager.slice_content_by_limit([data])
    capsys.readouterr()
    assert actual == [data]

    st_manager = FindManagerWhenEnterDate(
        "sour.ce", verbose=True, date="1000-10-23", json_flag=True, limit=3
    )
    actual = st_manager.slice_content_by_limit([data])
    capsys.readouterr()
    assert actual == [data]

    st_manager = FindManagerWhenEnterDate(
        "sour.ce", verbose=True, date="1000-10-23", json_flag=True, limit=-1
    )
    st_manager.slice_content_by_limit([data])
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] The limit is less than or " \
                           "equal to 0, news cannot be printed.\n\n"


def test_FindManagerWhenEnterDate_mehod_news_was_not_founded(init_FindManagerWhenEnterDate, capsys):
    st_manager = init_FindManagerWhenEnterDate
    st_manager._news_was_not_founded("1000-10-23")
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] No news was found for " \
                           "this date - 1000-10-23\n\n"


def test_FindManagerWhenEnterDate_mehod_data_output(
        init_FindManagerWhenEnterDate, capsys
):
    st_manager = init_FindManagerWhenEnterDate
    data = [{"data": "LOL"}]
    st_manager.data_output(data)
    captured = capsys.readouterr()
    assert captured.out == "[INFO] News will be printed in JSON format\n\n" \
                           "[\n" \
                           "    {\n" \
                           "        \"data\": \"LOL\"\n" \
                           "    }\n" \
                           "]\n"

    st_manager = FindManagerWhenEnterDate(
        "sour.ce", verbose=True, date="1000-10-23", json_flag=None, limit=1
    )
    data = [
        {
            "channel_title": "channel_title",
            "source": "source"
        },
        {
            "title": "title",
            "date": "date",
            "link": "link",
            "author": None,
            "category": ["Здоровье"],
            "description": 'description',
            "more_description": None,
            "comments": None,
            "media_object": "media_object",
            "extra_links": "extra_links",
            "source_feed": None,
        }
    ]
    st_manager.data_output([data])
    captured = capsys.readouterr()
    first_line_1 = calculate_terminal_size("News 2")
    last_line = calculate_terminal_size(None)
    assert captured.out == f"[INFO] News will be printed in a standard format\n\n" \
                           f"\n\nFeed source: source\n" \
                           f"Feed: channel_title\n\n" \
                           f"{'-' * first_line_1[0]}{first_line_1[2]}{'-' * first_line_1[1]}\n" \
                           f"Title: title\n" \
                           f"Date: date\n" \
                           f"Link: link\n" \
                           f"Category: Здоровье\n\n" \
                           f"Description: description\n\n" \
                           f"Media Object: media_object\n" \
                           f"Extra Links: extra_links\n" \
                           f"{'-' * last_line[0]}{last_line[2]}{'-' * last_line[1]}\n\n"


def test_FindManagerWhenEnterDate_mehod_check_news_by_date(
        init_FindManagerWhenEnterDate, capsys
):
    st_manager = init_FindManagerWhenEnterDate
    st_manager.check_news_by_date()
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] '1000-10-23' is an incorrect date. " \
                           "Please try to enter the date " \
                           "in a correct format\n\n"

    st_manager = FindManagerWhenEnterDate(
        "sour.ce", verbose=True, date="10001023", json_flag=True, limit=1
    )
    st_manager.check_news_by_date()
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] No news was found for this date" \
                           " - 1000-10-23\n\n"

    path = st_manager._get_abspath_to_storage()
    path = Path(path, "1000-10")
    st_manager.make_dir(path)

    st_manager.check_news_by_date()
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] No news was found for this date" \
                           " - 1000-10-23\n\n"

    path = Path(path, "1000-10-23")
    st_manager.make_dir(path)

    res = st_manager.check_news_by_date()
    assert res == []

    shutil.rmtree(Path(st_manager._get_abspath_to_storage(), "1000-10"))



import shutil
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

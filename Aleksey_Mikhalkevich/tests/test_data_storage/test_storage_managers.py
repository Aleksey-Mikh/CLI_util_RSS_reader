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
def prepare_SM():
    data = ["data"]
    st_manager = SM("sour.ce", verbose=True, data=data)
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


def test_StorageManager_mehod_get_abspath_to_storage(prepare_SM, path_to_storage):
    st_manger = prepare_SM
    path = st_manger._get_abspath_to_storage()
    assert path == path_to_storage


def test_StoragerManager_mehod_write_to_storage(del_file_txt, prepare_SM):
    path = Path(Path(__file__).parent, "feed.txt")
    st_manager = prepare_SM
    st_manager.write_to_storage(path, 'data')
    assert Path(path).exists()


def test_StorageManager_mehod_read_from_storage(prepare_SM):
    path = Path(Path(__file__).parent, "test_data.json")
    st_manager = prepare_SM
    result = st_manager.read_from_storage(path)
    assert result == [{"test": "data"}]


def test_StorageManager_mehod_make_dir(prepare_SM, del_dir):
    path = del_dir
    st_manager = prepare_SM
    st_manager.make_dir(path)
    assert Path(path).exists()


def test_StorageManager_mehod_path_is_exists(prepare_SM):
    path = Path(__file__)
    st_manager = prepare_SM
    assert st_manager.path_is_exists(path)

    path = Path(Path(__file__), "fake")
    assert not st_manager.path_is_exists(path)


def test_StorageManager_mehod_get_path(prepare_SM):
    expected = Path(Path(__file__), "check")
    st_manager = prepare_SM
    actual = st_manager.get_path(Path(__file__), "check")
    assert actual == expected

@pytest.mark.parametrize("date_str, correct_res",
                         [("Sat, 23 Oct 2021 17:51:11 +0300", "2021-10-23"),
                          ("Sat, 23 Oct 2021 some inf", None),
                          ("20211024", "2021-10-24"),
                          ("22024", None)]
                         )
def test_StorageManager_mehod_get_date_in_correct_format(prepare_SM, date_str, correct_res):
    st_manager = prepare_SM
    actual = st_manager.get_date_in_correct_format(date_str)
    assert actual == correct_res





from pathlib import Path

import pytest

from cool_project.conversion_to_format.conversion_to_html import (
    make_dir,
    is_list,
    get_env,
    get_content,
    convert_to_html
)


@pytest.fixture()
def del_dir():
    """A fixture that deletes a directory"""
    path = Path(Path(__file__).parent, "test_dir")
    yield path
    Path.rmdir(path)


@pytest.fixture()
def del_file_html():
    """A fixture that deletes file"""
    path = Path(Path(__file__).parent, "feed.html")
    yield
    Path.unlink(path)


def test_make_dir(del_dir):
    """test for make_dir"""
    path = del_dir
    make_dir(path)
    assert Path(path).exists()


@pytest.mark.parametrize("obj, correct_res",
                         [("soup_fix", False),
                          ([1, 2], True)]
                         )
def test_is_list(obj, correct_res):
    """test for is_list"""
    assert is_list(obj) == correct_res


def test_get_env():
    """test for get_env"""
    assert get_env()


@pytest.mark.parametrize("data, correct_res",
                         [("data", ["data"]),
                          ([["data"]], [["data"]])]
                         )
def test_get_content(data, correct_res):
    """test for get_content"""
    content = get_content(data, get_env())
    expected = {
        "title": "Feeds",
        "feeds": correct_res
    }
    assert content == expected


def test_convert_to_html(del_file_html, capsys):
    """test for convert_to_htm"""
    data = "data"
    path = Path(__file__).parent
    convert_to_html(data, path, True)
    captured = capsys.readouterr()
    assert captured.out == f"[INFO] Conversion to HTML started\n\n" \
                           f"[INFO] Conversion to HTML ended\n\n" \
                           f"[INFO] A feed in HTML format was saved on the path: " \
                           f"{Path(path, 'feed.html')}\n\n"

    data = "data"
    path = Path(Path(__file__).parent, "da:ta")
    convert_to_html(data, path, True)
    captured = capsys.readouterr()
    assert captured.out == f"[INFO] Conversion to HTML started\n\n" \
                           f"[INFO] Conversion to HTML ended\n\n" \
                           f"[ERROR] The entered path cannot be created\n\n"

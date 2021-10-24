import shutil
from pathlib import Path

import pytest

from cool_project.data_storage.working_with_storage import storage_control


@pytest.fixture()
def path_to_storage():
    """A fixture that return path to storage"""
    path = Path(__file__).parent.parent.parent
    path = Path(path, "cool_project", "data_storage", "storage")
    return path


def test_storage_control_after_parse(capsys, path_to_storage):
    """test for storage_control after parse"""
    data = [
        {
            "channel_title": "Люди Onlíner",
            "source": "source"
        },
        {
            "title": "title",
            "date": "Sat, 23 Oct 1000 17:51:11 +0300",
            "link": "link",
            "author": None,
            "category": ["Здоровье"],
            "description": "description",
            "more_description": None,
            "comments": None,
            "media_object": ["media_object"],
            "extra_links": "extra_links",
            "source_feed": None,
        }
    ]
    path = Path(__file__).parent
    storage_control(data=data, source="sour.ce", verbose=False, to_html=path, to_pdf=path)
    captured = capsys.readouterr()
    assert Path(Path(path, "feed.html")).exists()
    assert Path(Path(path, "feed.pdf")).exists()
    assert Path(Path(path_to_storage, "1000-10", "1000-10-23")).exists()
    assert captured.out == f"[INFO] A feed in HTML format was saved on the path: " \
                           f"{Path(path, 'feed.html')}\n\n" \
                           f"[INFO] A feed in PDF format was saved on the path: " \
                           f"{Path(path, 'feed.pdf')}\n\n"

    data = [
        {
            "channel_title": "Люди Onlíner",
            "source": "source"
        },
        {
            "date": "Sat, 23 Oct 10 17",
        }
    ]
    path = Path(__file__).parent
    storage_control(data=data, source="sour.ce", verbose=False, to_html=None, to_pdf=None)
    captured = capsys.readouterr()
    assert captured.out == f"[ERROR] The site sour.ce uses an " \
                           f"unsupported date format. " \
                           f"Storage data has failed.\n\n"

    Path.unlink(Path(path, "feed.html"))
    Path.unlink(Path(path, "feed.pdf"))
    shutil.rmtree(Path(path_to_storage, "1000-10"))


def test_storage_control_when_enter_date(capsys, path_to_storage):
    """test for storage_control when enter date"""
    if Path(Path(path_to_storage, "1000-10")).exists():
        shutil.rmtree(Path(path_to_storage, "1000-10"))

    data = [
        {
            "channel_title": "Люди Onlíner",
            "source": "source"
        },
        {
            "title": "title",
            "date": "Sat, 23 Oct 1000 17:51:11 +0300",
            "link": "link",
            "author": None,
            "category": ["Здоровье"],
            "description": "description",
            "more_description": None,
            "comments": None,
            "media_object": ["media_object"],
            "extra_links": "extra_links",
            "source_feed": None,
        }
    ]
    path = Path(__file__).parent
    storage_control(date="10001023", source=None, verbose=True, to_html=None, to_pdf=None, limit=1, json=True)
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] No news was found for this date - 1000-10-23\n\n"

    # make file for test
    storage_control(data=data, source="sour.ce", verbose=False, to_html=None, to_pdf=None)
    capsys.readouterr()

    path = Path(__file__).parent
    storage_control(date="10001023", source=None, verbose=True, to_html=path, to_pdf=path, limit=1, json=True)
    captured = capsys.readouterr()
    assert Path(Path(path, "feed.html")).exists()
    assert Path(Path(path, "feed.pdf")).exists()
    assert Path(Path(path_to_storage, "1000-10", "1000-10-23")).exists()
    assert captured.out == "[INFO] The news has been successfully extracted from the storage\n\n" \
                           "[INFO] According to the entered date, news " \
                           "was received from the following " \
                           "sources: source\n\n" \
                           "[INFO] News will be printed in JSON format\n\n" \
                           "[\n" \
                           "    {\n" \
                           '        "channel_title": "Люди Onlíner",\n' \
                           '        "source": "source"\n' \
                           "    },\n" \
                           "    {\n" \
                           '        "title": "title",\n' \
                           '        "date": "Sat, 23 Oct 1000 17:51:11 +0300",\n' \
                           '        "link": "link",\n' \
                           '        "author": null,\n' \
                           '        "category": [\n' \
                           '            "Здоровье"\n' \
                           '        ],\n' \
                           '        "description": "description",\n' \
                           '        "more_description": null,\n' \
                           '        "comments": null,\n' \
                           '        "media_object": [\n' \
                           '            "media_object"\n' \
                           '        ],\n' \
                           '        "extra_links": "extra_links",\n' \
                           '        "source_feed": null\n' \
                           '    }\n' \
                           ']\n' \
                           "[INFO] Conversion to HTML started\n\n" \
                           "[INFO] Conversion to HTML ended\n\n" \
                           "[INFO] A feed in HTML format was saved on the path: " \
                           f"{Path(path, 'feed.html')}\n\n" \
                           "[INFO] Fonts have been received\n\n" \
                           "[INFO] PDF generation started\n\n" \
                           "[INFO] PDF has been generated\n\n" \
                           "[INFO] A feed in PDF format was saved on the path: " \
                           f"{Path(path, 'feed.pdf')}\n\n"

    storage_control(date="10001023", source=None, verbose=True, to_html=None, to_pdf=None, limit=0, json=True)
    captured = capsys.readouterr()
    assert captured.out == "[INFO] The news has been successfully extracted from the storage\n\n" \
                           "[ERROR] The limit is less than or equal to 0, news cannot be printed.\n\n"

    Path.unlink(Path(path, "feed.html"))
    Path.unlink(Path(path, "feed.pdf"))
    shutil.rmtree(Path(path_to_storage, "1000-10"))


def test_storage_control_when_enter_date_and_source(capsys, path_to_storage):
    """test for storage_control when enter date and source"""
    if Path(Path(path_to_storage, "1000-10")).exists():
        shutil.rmtree(Path(path_to_storage, "1000-10"))

    data = [
        {
            "channel_title": "Люди Onlíner",
            "source": "source"
        },
        {
            "title": "title",
            "date": "Sat, 23 Oct 1000 17:51:11 +0300",
            "link": "link",
            "author": None,
            "category": ["Здоровье"],
            "description": "description",
            "more_description": None,
            "comments": None,
            "media_object": ["media_object"],
            "extra_links": "extra_links",
            "source_feed": None,
        }
    ]
    path = Path(__file__).parent
    storage_control(date="10001023", source="sour.ce", verbose=True, to_html=None, to_pdf=None, limit=1, json=True)
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] No news was found for this date - 1000-10-23\n\n"

    # make file for test
    storage_control(data=data, source="sour.ce", verbose=False, to_html=None, to_pdf=None)
    capsys.readouterr()

    path = Path(__file__).parent
    storage_control(date="10001023", source="sour.ce", verbose=True, to_html=path, to_pdf=path, limit=1, json=True)
    captured = capsys.readouterr()
    assert Path(Path(path, "feed.html")).exists()
    assert Path(Path(path, "feed.pdf")).exists()
    assert Path(Path(path_to_storage, "1000-10", "1000-10-23")).exists()
    assert captured.out == "[INFO] The news has been successfully extracted from the storage\n\n" \
                           "[INFO] The news was searched in the " \
                           "storage by date: 1000-10-23, " \
                           "and source: sour.ce\n\n" \
                           "[INFO] News will be printed in JSON format\n\n" \
                           "[\n" \
                           "    {\n" \
                           '        "channel_title": "Люди Onlíner",\n' \
                           '        "source": "source"\n' \
                           "    },\n" \
                           "    {\n" \
                           '        "title": "title",\n' \
                           '        "date": "Sat, 23 Oct 1000 17:51:11 +0300",\n' \
                           '        "link": "link",\n' \
                           '        "author": null,\n' \
                           '        "category": [\n' \
                           '            "Здоровье"\n' \
                           '        ],\n' \
                           '        "description": "description",\n' \
                           '        "more_description": null,\n' \
                           '        "comments": null,\n' \
                           '        "media_object": [\n' \
                           '            "media_object"\n' \
                           '        ],\n' \
                           '        "extra_links": "extra_links",\n' \
                           '        "source_feed": null\n' \
                           '    }\n' \
                           ']\n' \
                           "[INFO] Conversion to HTML started\n\n" \
                           "[INFO] Conversion to HTML ended\n\n" \
                           "[INFO] A feed in HTML format was saved on the path: " \
                           f"{Path(path, 'feed.html')}\n\n" \
                           "[INFO] Fonts have been received\n\n" \
                           "[INFO] PDF generation started\n\n" \
                           "[INFO] PDF has been generated\n\n" \
                           "[INFO] A feed in PDF format was saved on the path: " \
                           f"{Path(path, 'feed.pdf')}\n\n"

    storage_control(date="10001023", source="sour.ce", verbose=True, to_html=None, to_pdf=None, limit=0, json=True)
    captured = capsys.readouterr()
    assert captured.out == "[INFO] The news has been successfully extracted from the storage\n\n" \
                           "[INFO] The news was searched in the " \
                           "storage by date: 1000-10-23, " \
                           "and source: sour.ce\n\n" \
                           "[ERROR] The limit is less than or equal to 0, news cannot be printed.\n\n"

    p = Path(path_to_storage, "1000-10", "1000-10-23", "1000-10-23_sour_ce.json")
    target = Path(path_to_storage, "1000-10", "1000-10-23", "1000-10-23_sou3_ce.json")
    p.rename(target)
    storage_control(date="10001023", source="sour.ce", verbose=True, to_html=None, to_pdf=None, limit=1, json=True)
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] No news was founded for this date" \
                           " and: 1000-10-23, and this " \
                           "source: sour.ce\n\n"

    Path.unlink(Path(path, "feed.html"))
    Path.unlink(Path(path, "feed.pdf"))
    shutil.rmtree(Path(path_to_storage, "1000-10"))

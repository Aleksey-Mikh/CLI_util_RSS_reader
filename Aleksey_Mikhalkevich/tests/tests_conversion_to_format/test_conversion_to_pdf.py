from pathlib import Path

import pytest

from cool_project.conversion_to_format.conversion_to_pdf import (
    PDF,
    convertor_to_pdf,
)


@pytest.fixture()
def del_dir():
    """A fixture that deletes a directory"""
    path = Path(Path(__file__).parent, "test_dir")
    yield path
    Path.rmdir(path)


@pytest.fixture()
def del_file_pdf():
    """A fixture that deletes file"""
    path = Path(Path(__file__).parent, "feed.pdf")
    yield
    Path.unlink(path)


@pytest.fixture()
def init_pdf():
    """A fixture that init pdf"""
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(True, 10)
    path_to_ttf = Path(
        Path(__file__).parent.parent.parent,
        "cool_project",
        "conversion_to_format",
        "files_for_pdf",
        "DejaVuSansCondensed.ttf")
    pdf.add_font("DejaVu", "", path_to_ttf, uni=True)
    pdf.set_font("DejaVu", "", 14)
    yield pdf


@pytest.mark.parametrize("obj, correct_res",
                         [("soup_fix", False),
                          ([1, 2], True)]
                         )
def test_PDF_method_is_list(obj, correct_res):
    """test for PDF method is list"""
    pdf = PDF()
    assert pdf.is_list(obj) == correct_res


def test_PDF_method_make_dir(del_dir):
    """test PDF method make dir"""
    path = del_dir
    PDF.make_dir(path)
    assert Path(path).exists()


def test_PDF_method_footer(init_pdf):
    """test for PDF method footer"""
    pdf = init_pdf
    pdf.footer()


def test_PDF_method_body(init_pdf):
    """test PDF method body"""
    pdf = init_pdf
    data = [
        {
            "channel_title": "channel_title",
            "source": "source"
        },
        {
            "title": "title",
            "date": "date",
            "link": "link",
            "author": "author",
            "category": ["Здоровье"],
            "description": 'description',
            "more_description": "more_description",
            "comments": "comments",
            "media_object": ["media_object"],
            "extra_links": ["extra_links"],
            "source_feed": ["source_feed"],
        }
    ]
    pdf.body(data)


def test_PDF_method_get_item(init_pdf):
    """test PDF method _get_item"""
    pdf = init_pdf
    data = {
        "title": "title",
        "date": "date",
        "link": "link",
        "author": "author",
        "category": "Здоровье",
        "description": 'description',
        "more_description": "more_description",
        "comments": "comments",
        "media_object": "media_object",
        "extra_links": "extra_links",
        "source_feed": "source_feed",
    }

    pdf._get_item(data)


def test_convertor_to_pdf(del_file_pdf, capsys):
    """test for convertor_to_pdf"""
    data = [
        {
            "channel_title": "channel_title",
            "source": "source"
        },
        {
            "title": "title",
            "date": "date",
            "link": "link",
            "author": "author",
            "category": ["Здоровье"],
            "description": 'description',
            "more_description": "more_description",
            "comments": "comments",
            "media_object": ["media_object"],
            "extra_links": ["extra_links"],
            "source_feed": ["source_feed"],
        }
    ]

    convertor_to_pdf(data, Path(__file__).parent, True)
    captured = capsys.readouterr()
    assert captured.out == f"[INFO] Fonts have been received\n\n" \
                           f"[INFO] PDF generation started\n\n" \
                           f"[INFO] PDF has been generated\n\n" \
                           f"[INFO] A feed in PDF format was saved on the path: " \
                           f"{Path(Path(__file__).parent, 'feed.pdf')}\n\n"

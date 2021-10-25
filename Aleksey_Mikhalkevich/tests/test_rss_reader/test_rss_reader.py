import pytest

from cool_project.rss_reader import RSSParser, start_parsing
from cool_project.project_settings import PROGRAM_VERSION


@pytest.mark.parametrize("args, expected",
                         [("source --json --verbose --limit=2 "
                           "--date=2020 --to-html=path --to-pdf=path",
                           ("source", True, True, 2, "2020", "path", "path")),
                          (" ",
                           (None, False, False, None, None, None, None)),
                          ("source --verbose",
                           ("source", False, True, None, None, None, None)),
                          ("--json --verbose --limit=2 --date=2020",
                           (None, True, True, 2, "2020", None, None)),
                          ("source --json --verbose --limit=2 --date=2020",
                           ("source", True, True, 2, "2020", None, None)),
                          ("source --verbose --limit=2 "
                           "--date=2020 --to-html=path",
                           ("source", False, True, 2, "2020", "path", None)),
                          ("source --json --verbose --limit=2 "
                           "--date=2020 --to-pdf=path",
                           ("source", True, True, 2, "2020", None, "path")),
                          ("--json --verbose --limit=2 --date=2020 "
                           "--to-html=path --to-pdf=path",
                           (None, True, True, 2, "2020", "path", "path")),
                          ]
                         )
def test_RSSParser_method_init_argparse(args, expected):
    """test for method init_argparse"""
    parser = RSSParser(args.split())
    actual = (
        parser.source, parser.json, parser.verbose,
        parser.limit, parser.date, parser.to_html, parser.to_pdf
    )
    assert actual == expected


@pytest.mark.parametrize("args, expected",
                         [("--version",
                           f"Version {PROGRAM_VERSION}\n"),
                          ("source --json --verbose --limit=2 --date=2020 "
                           "--to-html=path --to-pdf=path --version",
                           f"Version {PROGRAM_VERSION}\n"),
                          ]
                         )
def test_RSSParser_method_init_argparse(args, expected, capsys):
    """test for method init_argparse"""
    try:
        parser = RSSParser(["--version"])
        captured = capsys.readouterr()
    except SystemExit:
        captured = capsys.readouterr()
    finally:
        assert captured.out == expected


def test_RSSParser_method_parsing(capsys):
    """test for method parsing"""
    parser = RSSParser("https://people.onliner.by/feed --limit=1".split())
    parser.parsing()
    captured = capsys.readouterr()
    assert captured.out == "[INFO] Receiving the news was successful\n\n"

    parser = RSSParser("https://people.onliner.by --limit=1".split())
    parser.parsing()
    captured = capsys.readouterr()
    assert captured.out == "[WARNING] 'https://people.onliner.by' " \
                           "isn't a RSS. Please try to " \
                           "enter a correct URL\n\n" \
                           "[ERROR] Data wasn't received\n\n"


class Response:
    """The class which simulates the response.status_code"""
    def __init__(self, value):
        self.status_code = value


def test_RSSParser_method_isvalid(capsys):
    """test for method isvalid"""
    parser = RSSParser("https://people.onliner.by/feed --limit=1".split())
    actual = parser._isvalid(Response(200))
    assert actual

    parser = RSSParser(
        "https://people.onliner.by/feed --limit=1 --verbose".split()
    )
    parser._isvalid(None)
    captured = capsys.readouterr()
    assert captured.out == "[INFO] The program stop running with error," \
                           " when it try to get information " \
                           "from 'https://people.onliner.by/feed'\n\n"

    parser = RSSParser("https://people.onliner.by/feed --limit=1".split())
    parser._isvalid(Response(404))
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] 'https://people.onliner.by/feed': " \
                           "404 Page Not Found\n\n"


def test_RSSParser_method_get_html():
    """test for method get_html"""
    parser = RSSParser("https://people.onliner.by/feed --limit=1".split())
    response = parser._get_html()
    assert response.status_code == 200


def test_RSSParser_method_check_error_status_code(capsys):
    """test for method check_error_status_code"""
    parser = RSSParser("https://people.onliner.by/feed --limit=1".split())
    parser._check_error_status_code(405)
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] Error seems to have been caused by" \
                           " the client. Check url which you give.\n\n"

    parser._check_error_status_code(500)
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] The server failed to " \
                           "execute a request\n\n"

    parser._check_error_status_code(700)
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] Error which can't be processed" \
                           " because status code don't defined\n\n"


def test_RSSParser_method_check_date_and_source(capsys):
    """test for method check_date_and_source"""
    parser = RSSParser("https://people.onliner.by/feed --limit=1".split())
    actual = parser.check_date_and_source()
    assert actual

    parser = RSSParser("--limit=1 --verbose".split())
    actual = parser.check_date_and_source()
    captured = capsys.readouterr()
    assert captured.out == "[INFO] Source is None\n\n" \
                           "[ERROR] A source wasn't enter\n\n"


def test_RSSParser_method_print_data_in_console(capsys):
    """test for method print_data_in_console"""
    parser = RSSParser(
        "https://people.onliner.by/feed --limit=1 --json --verbose".split()
    )
    parser.serializable_data = None
    actual = parser.print_data_in_console()
    assert not actual

    parser = RSSParser(
        "https://people.onliner.by/feed --limit=1 --json --verbose".split()
    )
    parser.serializable_data = [{"data": "data"}]
    parser.print_data_in_console()
    captured = capsys.readouterr()
    assert captured.out == "[INFO] Output news in JSON format\n\n" \
                           '[\n' \
                           '    {\n' \
                           '        "data": "data"\n' \
                           '    }\n' \
                           ']\n'

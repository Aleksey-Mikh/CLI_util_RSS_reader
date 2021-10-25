from cool_project.cervices.print_functions import (
    info_print, warning_print, error_print
)


def test_info_print(capsys):
    """test for info_print"""
    info_print("Message")
    captured = capsys.readouterr()
    assert captured.out == "[INFO] Message\n\n"


def test_warning_print(capsys):
    """test for warning_print"""
    warning_print("Message")
    captured = capsys.readouterr()
    assert captured.out == "[WARNING] Message\n\n"


def test_error_print(capsys):
    """test for error_print"""
    error_print("Message")
    captured = capsys.readouterr()
    assert captured.out == "[ERROR] Message\n\n"
    assert captured.out != "[ERROR] Message\n"

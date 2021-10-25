from pathlib import Path

from bs4 import BeautifulSoup
import pytest

from cool_project.serializers.serializers import (
    serialization_data,
    serialization_item,
    checking_the_source_is_the_rss,
    get_channel_data,
    percent_generator,
    check_limit,
)


@pytest.fixture()
def news_data():
    """fixture which read data.xml file"""
    path = Path(Path(__file__).parent, "data.xml")
    with open(path, encoding="utf-8") as file:
        data = file.read()
    return data


@pytest.fixture()
def news_data_full():
    """fixture which read full_data.xml file"""
    path = Path(Path(__file__).parent, "full_data.xml")
    with open(path, encoding="utf-8") as file:
        data = file.read()
    return data


def test_get_channel_data(soup_fix):
    """test for get_channel_data"""
    result_data = get_channel_data(soup_fix, "source")
    correct_result = {
        "channel_title": "Люди Onlíner",
        "source": "source"
    }
    assert result_data == correct_result

    result_data = get_channel_data(None, "source")
    correct_result = {
        "channel_title": None,
        "source": "source"
    }
    assert result_data == correct_result


def test_percent_generator(capsys):
    """test for percent_generator"""
    list_items = [1]
    gen = percent_generator(list_items, 5)
    list_items.append(2)
    next(gen)
    captured = capsys.readouterr()
    assert captured.out == f"[INFO] News received [1/5], " \
                           f"percent of execution program=20%\n\n"
    list_items.append(2)
    next(gen)
    captured = capsys.readouterr()
    assert captured.out == f"[INFO] News received [2/5], " \
                           f"percent of execution program=40%\n\n"
    list_items.append(2)
    next(gen)
    capsys.readouterr()
    list_items.append(2)
    next(gen)
    capsys.readouterr()
    list_items.append(2)
    next(gen)
    captured = capsys.readouterr()
    assert captured.out == f"[INFO] News received [5/5], " \
                           f"percent of execution program=100%\n\n"


@pytest.mark.parametrize("soup, verbose, source, correct_res",
                         [("soup_fix", True, "source", True),
                          ("soup_fix", False, "source", True),
                          ("", True, "source", False),
                          ("", False, "source", False)]
                         )
def test_checking_the_source_is_the_rss(
        soup, verbose, source, correct_res, request, capsys
):
    """test for checking_the_source_is_the_rss"""
    if soup:
        # This function dynamically runs a named fixture function.
        soup = request.getfixturevalue(soup)
    result = checking_the_source_is_the_rss(soup, verbose, "source")
    capsys.readouterr()
    assert result == correct_res


@pytest.mark.parametrize("limit, count_news, correct_res",
                         [(None, 10, 10),
                          (15, 10, 10),
                          (-1, 10, False),
                          (5, 10, 5)]
                         )
def test_check_limit(limit, count_news, correct_res, capsys):
    """test for check_limit"""
    result = check_limit(limit, count_news)
    capsys.readouterr()
    assert result == correct_res


def test_serialization_item(soup_fix, news_data_full):
    """test for serialization_item"""
    item = soup_fix.find("item")
    data = serialization_item(item)
    correct_res = {
        "title": "Пиневич: 40% коечного фонда "
                 "перепрофилировано под ковидных пациентов",
        "date": "Sat, 23 Oct 2021 17:51:11 +0300",
        "link": "https://people.onliner.by/2021/10/23/"
                "pereprofilirovano-pod-kovidnyx-pacientov",
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
        "media_object": ["https://content.onliner.by/news/thumbnail/"
                         "5a7aa9c81d307b0ddc03a0f10746bffe.jpeg"],
        "extra_links": "https://people.onliner.by/2021/10/23/"
                       "pereprofilirovano-pod-kovidnyx-pacientov",
        "source_feed": None,
    }
    assert data == correct_res

    data = serialization_item(None)
    correct_res = {
        "title": None,
        "date": None,
        "link": None,
        "author": None,
        "category": None,
        "description": None,
        "more_description": None,
        "comments": None,
        "media_object": None,
        "extra_links": None,
        "source_feed": None,
    }
    assert data == correct_res

    soup = BeautifulSoup(news_data_full, "xml")
    item_full = soup.find("item")
    data_full = serialization_item(item_full)
    correct_res_full = {
        "title": "Пиневич: 40% коечного фонда перепрофилировано "
                 "под ковидных пациентов",
        "date": "Sat, 23 Oct 2021 17:51:11 +0300",
        "link": "https://people.onliner.by/2021/10/23/"
                "pereprofilirovano-pod-kovidnyx-pacientov",
        "author": "Onliner",
        "category": ["Здоровье"],
        "description": 'passs',
        "more_description": "Marissa talks to long.",
        "comments": "passs",
        "media_object": "passs",
        "extra_links": "https://people.onliner.by/2021/10/23/"
                       "pereprofilirovano-pod-kovidnyx-pacientov",
        "source_feed": ['passs', 'passs'],
    }
    assert data_full == correct_res_full


def test_serialization_data(news_data, capsys):
    """test for serialization_data"""
    data = serialization_data(news_data, 3, True, "source")
    capsys.readouterr()
    correct_res = [
        {
            "channel_title": "Люди Onlíner",
            "source": "source"
        },
        {
            "title": "Пиневич: 40% коечного фонда "
                     "перепрофилировано под ковидных пациентов",
            "date": "Sat, 23 Oct 2021 17:51:11 +0300",
            "link": "https://people.onliner.by/2021/10/23/"
                    "pereprofilirovano-pod-kovidnyx-pacientov",
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
            "media_object": ["https://content.onliner.by/news/thumbnail/"
                             "5a7aa9c81d307b0ddc03a0f10746bffe.jpeg"],
            "extra_links": "https://people.onliner.by/2021/10/23/"
                           "pereprofilirovano-pod-kovidnyx-pacientov",
            "source_feed": None,
        }
    ]
    assert data == correct_res

    incorrect_data = f"<item></item>"
    data = serialization_data(incorrect_data, 3, True, "source")
    captured = capsys.readouterr()
    assert captured.out == "[WARNING] 'source' isn't a RSS. Please try " \
                           "to enter a correct URL\n\n[INFO] If your " \
                           "sure that this URL is correct, please check" \
                           " your URL, maybe it use old rss version and" \
                           " parser don't understand it.\n\n"

import shutil
from math import ceil

import pytest

from cool_project.cervices.data_output import (
    console_output_feed,
    output_feed,
    line_break,
    rebuild_value,
    console_json_output,
)

DATA = [
    {
        'channel_title': 'Lenta.ru : Новости',
        'source': 'https://lenta.ru/rss'
    },
    {
        'title': '«Краснодар» разгромил новичка РПЛ и вышел на третье место',
        'date': 'Sat, 23 Oct 2021 15:51:57 +0300',
        'link': 'https://lenta.ru/news/2021/10/23/tretyemesto/',
        'author': 'Алексей Гусев',
        'category': ['Спорт'],
        'description': '«Краснодар» на выезде обыграл «Нижний Новгород» в матче 12-го тура Российской премьер-лиги'
                       ' (РПЛ). Встреча прошла в субботу, 23 октября, и завершилась со счетом 4:1 в пользу гостей. '
                       'Одержать разгромную победу краснодарцам позволили голы Гжегожа Крыховяка, '
                       'Эдуарда Сперцяна, Александра Черникова и Владимира Ильина.',
        'more_description': None,
        'comments': None,
        'media_object': 'https://icdn.lenta.ru/images/2021/10/23/15/20211023154554818/'
                        'pic_fbc5daebf5e79eab60893757b5d7f532.jpg',
        'extra_links': 'https://lenta.ru/news/2021/10/23/tretyemesto/',
        'source_feed': None
    },
    {
        'title': 'Потомков западных интервентов в России призвали изучать историю',
        'date': 'Sat, 23 Oct 2021 15:39:00 +0300',
        'link': 'https://lenta.ru/news/2021/10/23/naryshkin_/',
        'author': 'Варвара Кошечкина',
        'category': ['Россия'],
        'description': 'Западные страны, которые в прошлом планировали захватить Россию, '
                       'должны как следует изучать историю, чтобы смириться с невыполнимостью '
                       'подобных надежд. С таким заявлением выступил глава Службы внешней разведки'
                       ' России Сергей Нарышкин в ходе церемонии награждения победителей '
                       'Всероссийского конкурса краеведов.',
        'more_description': None,
        'comments': None,
        'media_object': 'https://icdn.lenta.ru/images/2021/10/23/15/20211023151836599/'
                        'pic_ec551103d6e4f2e3642e3ba58ac8ca1b.jpg',
        'extra_links': 'https://lenta.ru/news/2021/10/23/naryshkin_/',
        'source_feed': None
    }
]


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


def test_console_output_feed(capsys):
    """test for console_output_feed function"""
    console_output_feed(DATA, False)
    captured = capsys.readouterr()

    first_line_1 = calculate_terminal_size("News 3")
    first_line_2 = calculate_terminal_size("News 4")
    last_line = calculate_terminal_size(None)

    output = f'\n\nFeed source: {DATA[0]["source"]}\n' \
             f'Feed: {DATA[0]["channel_title"]}\n\n' \
             f'{"-" * first_line_1[0]}{first_line_1[2]}{"-" * first_line_1[1]}\n' \
             f'Title: {DATA[1]["title"]}\n' \
             f'Date: {DATA[1]["date"]}\n' \
             f'Link: {DATA[1]["link"]}\n' \
             f'Author: {DATA[1]["author"]}\n' \
             f'Category: {DATA[1]["category"][0]}\n\n' \
             f'Description: {DATA[1]["description"]}\n\n' \
             f'Media Object: {DATA[1]["media_object"]}\n' \
             f'Extra Links: {DATA[1]["extra_links"]}\n' \
             f'{"-" * last_line[0]}{last_line[2]}{"-" * last_line[1]}\n\n' \
             f'{"-" * first_line_2[0]}{first_line_2[2]}{"-" * first_line_2[1]}\n' \
             f'Title: {DATA[2]["title"]}\n' \
             f'Date: {DATA[2]["date"]}\n' \
             f'Link: {DATA[2]["link"]}\n' \
             f'Author: {DATA[2]["author"]}\n' \
             f'Category: {DATA[2]["category"][0]}\n\n' \
             f'Description: {DATA[2]["description"]}\n\n' \
             f'Media Object: {DATA[2]["media_object"]}\n' \
             f'Extra Links: {DATA[2]["extra_links"]}\n' \
             f'{"-" * last_line[0]}{last_line[2]}{"-" * last_line[1]}\n\n' \

    assert captured.out == output

@pytest.mark.parametrize("news, colorize",
                         [("News 5", False),
                          ("News 6", True)]
                         )
def test_output_feed(capsys, news, colorize):
    """test for output_feed function"""
    output_feed(DATA[1], colorize)
    captured = capsys.readouterr()

    first_line_1 = calculate_terminal_size(news)
    last_line = calculate_terminal_size(None)
    output = f'{"-" * first_line_1[0]}{first_line_1[2]}{"-" * first_line_1[1]}\n' \
             f'Title: {DATA[1]["title"]}\n' \
             f'Date: {DATA[1]["date"]}\n' \
             f'Link: {DATA[1]["link"]}\n' \
             f'Author: {DATA[1]["author"]}\n' \
             f'Category: {DATA[1]["category"][0]}\n\n' \
             f'Description: {DATA[1]["description"]}\n\n' \
             f'Media Object: {DATA[1]["media_object"]}\n' \
             f'Extra Links: {DATA[1]["extra_links"]}\n' \
             f'{"-" * last_line[0]}{last_line[2]}{"-" * last_line[1]}\n'

    assert captured.out == output


@pytest.mark.parametrize("word, res",
                         [("KEK", ""),
                          ("description", "\n"),
                          ("comments", "\n")]
                         )
def test_line_break(capsys, word, res):
    """test for line_break function"""
    line_break(word)
    captured = capsys.readouterr()
    assert captured.out == res

@pytest.mark.parametrize("ls, res",
                         [(["How", "I", "Met", "Your", "Mother"],
                           "How, I, Met, Your, Mother"),
                          (["20", "12"], "20, 12")]
                         )
def test_rebuild_value(ls, res):
    """How I Met Your Mother is an American sitcom -
    https://en.wikipedia.org/wiki/How_I_Met_Your_Mother"""
    result = rebuild_value(ls)
    assert result == res


def test_console_json_output(capsys):
    """test for console_json_output function"""
    console_json_output([DATA[0], DATA[1]])
    captured = capsys.readouterr()
    output = "[\n" \
             "    {\n" \
             '        "channel_title": "Lenta.ru : Новости",\n' \
             '        "source": "https://lenta.ru/rss"\n' \
             '    },\n' \
             '    {\n' \
             '        "title": "«Краснодар» разгромил новичка РПЛ и вышел на третье место",\n' \
             '        "date": "Sat, 23 Oct 2021 15:51:57 +0300",\n' \
             '        "link": "https://lenta.ru/news/2021/10/23/tretyemesto/",\n' \
             '        "author": "Алексей Гусев",\n' \
             '        "category": [\n' \
             '            "Спорт"\n' \
             '        ],\n' \
             '        "description": ' \
             '"«Краснодар» на выезде обыграл ' \
             '«Нижний Новгород» в матче 12-го тура Российской ' \
             'премьер-лиги (РПЛ). Встреча прошла в субботу, ' \
             '23 октября, и завершилась со счетом 4:1 в ' \
             'пользу гостей. Одержать разгромную победу ' \
             'краснодарцам позволили голы Гжегожа Крыховяка,' \
             ' Эдуарда Сперцяна, Александра Черникова ' \
             'и Владимира Ильина.",\n' \
             '        "more_description": null,\n' \
             '        "comments": null,\n' \
             '        "media_object": ' \
             '"https://icdn.lenta.ru/images' \
             '/2021/10/23/15/20211023154554818/' \
             'pic_fbc5daebf5e79eab60893757b5d7f532.jpg",\n' \
             '        "extra_links": ' \
             '"https://lenta.ru/news/2021/10/23/tretyemesto/",\n' \
             '        "source_feed": null\n' \
             '    }\n' \
             ']\n'

    assert captured.out == output

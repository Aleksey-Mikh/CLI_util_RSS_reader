from cool_project.cervices.print_functions import info_print
from cool_project.data_storage.storage_managers import (
    FindManagerWhenEnterDate,
    FindManagerWhenEnterDateAndSource,
    DataManagerInStorageAfterParsing
)
from cool_project.conversion_to_format.conversion_to_html import convert_to_html
from cool_project.conversion_to_format.conversion_to_pdf import convertor_to_pdf


def interface_to_convert(data, to_html, to_pdf, verbose):
    """
    Interface to convert data to some format.

    :param data: a data to convert
    :param to_html: a flag
    :param to_pdf: a flag
    :param verbose: a flag
    """
    if to_html is not None:
        convert_to_html(data, to_html, verbose)

    if to_pdf is not None:
        convertor_to_pdf(data, to_pdf, verbose)


def storage_control(*, date=None, source=None, data=None, verbose=None, **kwargs):
    """
    The interface between rss_reader and data storage.
    Depending on the received data,
    call the following managers to work with the storage:

    DataManagerInStorageAfterParsing - if the data and the source
    are received, the case when data save in the storage after parsing;

    FindManagerWhenEnterDate - if date is received and source is None,
    case when a date-only search in the storage;

    FindManagerWhenEnterDateAndSource - if date and source
    are received, case when a search in the storage by date and source;

    Accepts only keyword arguments.

    :param date: the date on which you need to receive the news
    :param source: news source
    :param data: data that need to write to the storage
    :param verbose: verbose mode
    :param kwargs: --json value, --limit value or other
    :return:
    """
    # after parsing, writing a data to the storage
    if data is not None and source is not None:
        st_manager = DataManagerInStorageAfterParsing(
            source, data=data, verbose=verbose, colorize=kwargs["colorize"]
        )
        response_from_split_data_by_news = st_manager.split_data_by_news()

        if response_from_split_data_by_news is None:
            return False

        channel_data, dict_for_data_saving = response_from_split_data_by_news
        st_manager.make_dir_by_key(dict_for_data_saving)
        st_manager.control_of_exist(dict_for_data_saving, channel_data)

        interface_to_convert(
            data, kwargs["to_html"], kwargs["to_pdf"], verbose
        )

    # if user enter only a date
    elif date is not None and source is None:
        json_flag, limit = kwargs["json"], kwargs["limit"]
        st_manager = FindManagerWhenEnterDate(
            source, date=date, verbose=verbose, json_flag=json_flag,
            limit=limit, colorize=kwargs["colorize"]
        )
        paths = st_manager.check_news_by_date()

        if not paths:
            return False

        list_of_content = st_manager.get_content_by_paths(paths)
        if verbose:
            info_print(
                "The news has been successfully extracted from the storage"
            )
        list_of_content = st_manager.slice_content_by_limit(list_of_content)
        if not list_of_content:
            return False
        st_manager.data_output(list_of_content)

        interface_to_convert(
            list_of_content, kwargs["to_html"], kwargs["to_pdf"], verbose
        )

    # if user enter a date and a source
    elif date is not None and source is not None:
        json_flag, limit = kwargs["json"], kwargs["limit"]
        st_manager = FindManagerWhenEnterDateAndSource(
            source, date=date, verbose=verbose, json_flag=json_flag,
            limit=limit, colorize=kwargs["colorize"]
        )
        paths = st_manager.check_news_by_date()
        st_manager.date = st_manager.get_date_in_correct_format(date)

        if not paths:
            return False
        file_name = st_manager.get_file_name()

        path = list(filter(lambda x: x[-len(file_name):] == file_name, paths))
        if not path:
            st_manager.news_was_not_founded()
            return False

        data = st_manager.read_from_storage(path[0])
        if verbose:
            info_print(
                "The news has been successfully extracted from the storage"
            )

        data = st_manager.slice_content_by_limit(data)
        if not data:
            return False
        st_manager.data_output(data)

        interface_to_convert(
            data, kwargs["to_html"], kwargs["to_pdf"], verbose
        )

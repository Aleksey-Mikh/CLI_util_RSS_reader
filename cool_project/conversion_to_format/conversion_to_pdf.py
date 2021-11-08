from pathlib import Path

from fpdf import FPDF

from cool_project.cervices.print_functions import info_print, error_print
from project_settings import FILE_NAME_PDF


class PDF(FPDF):
    """
    Class that generates the PDF file
    """

    def _get_item(self, news):
        """
        the method that generates the news.

        :param news: dict
        """
        if news["title"]:
            self.multi_cell(0, 5, f"Title: {news['title']}")
            self.ln()
        if news["date"]:
            self.multi_cell(0, 5, f"date of publication: {news['date']}")
            self.ln()
        if news["link"]:
            self.multi_cell(0, 5, f"Link: {news['link']}")
            self.ln()
        if news["author"]:
            self.multi_cell(0, 5, f"Author: {news['author']}")
            self.ln()

        if news["category"]:
            if self.is_list(news["category"]):
                for category in news["category"]:
                    self.cell(0, 5, "Categories: ", ln=1)
                    self.multi_cell(0, 5, f"{' ' * 5}{category}")
            else:
                self.multi_cell(0, 5, f"Category: {news['category']}")
            self.ln()

        if news["description"]:
            self.multi_cell(0, 5, f"Description: {news['description']}")
            self.ln()
        if news["more_description"]:
            self.multi_cell(
                0, 5, f"More description: {news['more_description']}"
            )
            self.ln()
        if news["comments"]:
            self.multi_cell(0, 5, f"Comments: {news['comments']}")
            self.ln()

        if news["media_object"]:
            if self.is_list(news["media_object"]):
                for media in news["media_object"]:
                    self.cell(0, 5, "Media objects: ", ln=1)
                    self.multi_cell(0, 5, f"{' ' * 5}{media}")
            else:
                self.multi_cell(0, 5, f"Media object: {news['media_object']}")
            self.ln()

        if news["extra_links"]:
            if self.is_list(news["extra_links"]):
                for extra_link in news["extra_links"]:
                    self.cell(0, 5, "Extra links: ", ln=1)
                    self.multi_cell(0, 5, f"{' ' * 5}{extra_link}")
            else:
                self.multi_cell(0, 5, f"Extra link: {news['extra_links']}")
            self.ln()

        if news["source_feed"]:
            if self.is_list(news["source_feed"]):
                for source in news["source_feed"]:
                    self.cell(0, 5, "Sources: ", ln=1)
                    self.multi_cell(0, 5, f"{' ' * 5}{source}")
            else:
                self.multi_cell(0, 5, f"Source: {news['source_feed']}")

    def body(self, data):
        """
        the method that generates the feeds
        :param data: a list of dictionaries with news
        """
        if not self.is_list(data[0]):
            data = [data]

        for feed in data:
            self.cell(
                0, 5, f'Channel title: {feed[0]["channel_title"]}',
                align="C", ln=1
            )
            self.cell(0, 5, f'Source: {feed[0]["source"]}', align="C", ln=1)

            for news in feed[1:]:
                self.cell(0, 5, f"{'-' * 125}", align="C", ln=1)

                self._get_item(news)

                self.cell(0, 5, f"{'-' * 125}", align="C")
                self.ln()
                self.ln()

    def footer(self):
        """
        footer generation
        """
        self.set_y(-10)
        self.set_font("DejaVu", "", 15)
        self.cell(0, 5, f"Page {str(self.page_no())}", 0, 0, "C")

    @staticmethod
    def is_list(obj):
        """
        Check obj is list.

        :param obj: object
        :return: True or False
        """
        return isinstance(obj, list)

    @staticmethod
    def make_dir(path):
        """
        Creating a folder at the got path.
        If the folder already exists does nothing.

        :param path: the path where the folder should be created
        """
        if not Path(path).exists():
            p = Path(path)
            p.mkdir(parents=True)


def convertor_to_pdf(data, path, verbose):
    """
    Еhe function gets a list of dictionaries with
    news, a path, and a verbose flag.
    the function gets the path to TTF with fonts and
    sets the resulting fonts to the PDF class,
    generates PDF from the received data.
    Saves the file to the received path.

    :param data: a list of dictionaries with news
    :param path: the path to save the file
    :param verbose: verbose mode
    """
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    path_to_ttf = Path(
        Path(__file__).parent, "files_for_pdf", "DejaVuSansCondensed.ttf"
    )
    pdf.add_font("DejaVu", "", path_to_ttf, uni=True)

    if verbose:
        info_print("Fonts have been received")

    pdf.set_font("DejaVu", "", 14)
    pdf.set_auto_page_break(True, 10)

    if verbose:
        info_print("PDF generation started")
    pdf.body(data)
    if verbose:
        info_print("PDF has been generated")

    try:
        pdf.make_dir(path)
        path = Path(path, FILE_NAME_PDF)
        pdf.output(path, "F")
        info_print(f"A feed in PDF format was saved on the path: {path}")
    except PermissionError:
        error_print(
            f"it is not possible to save a PDF file on this path: {path}."
            f" Such file already exists or cannot access the folder."
        )
    except Exception:
        error_print("The entered path cannot be created")

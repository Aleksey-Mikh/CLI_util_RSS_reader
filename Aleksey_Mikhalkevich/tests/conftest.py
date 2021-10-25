import pytest
from bs4 import BeautifulSoup


@pytest.fixture()
def soup_fix(news_data):
    """fixture which make soup obj"""
    soup = BeautifulSoup(news_data, "xml")
    return soup

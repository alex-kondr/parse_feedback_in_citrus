from typing import List

import requests
from bs4 import BeautifulSoup


def get_categories(url: str) -> List:

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    ul_categories = soup.find("ul", class_='menu-0-2-51')
    categories = ul_categories.find_all("li")

    return categories

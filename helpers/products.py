import json
import re
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from lxml import etree


def get_products(url: str) -> List:
    print("get_products_url: ", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    products = soup.find("div", class_=re.compile("catalog-facet"))
    products = products.find_all("a", class_=re.compile("link"))
    return products


def get_product_name(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    product_ = soup.find("div", class_="widgets")

    product_name = (
        soup.find("h1", class_="title-0-2-1676")
        .text
        .replace("/", "_")
        .replace('"', "")
        .strip()
    )

    return product_name


def handler_comments(soup_comments: List, url: str) -> List[Dict]:
    comments = []

    for comment in soup_comments:
        author_name = comment.find(class_=re.compile("author-0-2-1832")).p.text.strip()
        grade = comment.find_all("path", fill="rgb(255, 193, 7)")
        date = comment.find("p", class_=re.compile("date-0-2-1833")).text.strip()
        text = comment.find("p", class_=re.compile("description-0-2-1824")).text.strip()

        comments.append(
            {
                "title": "",
                "author_name": author_name,
                "url": url,
                "grade": len(grade),
                "date": date,
                "text": text
            }
        )

    return comments


def get_comments(url: str) -> List:
    print("product_url: ", url)
    HEADERS = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', \
                'Accept-Language': 'en-US, en;q=0.5'})

    response = requests.get("https://api.ctrs.com.ua/products/707505/reviews?page=1&productId=707505")
    result = response.content["data"]["reviews"]

    with open("test.json", "w", encoding="utf-8") as fd:
        json.dump(result, fd, ensure_ascii=False, indent=2)
    # response = requests.get(url + "?tab=reviews", headers=HEADERS)
    # soup = BeautifulSoup(response.text, "lxml")
    # dom = etree.HTML(str(soup))
    # a = dom.xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[2]/div[1]/@class')
    # soup_comments = soup.find_all("div", class_=re.compile("review-0-2-1822"))

    # if not all_comments:
    #     return []
    #
    # soup_comments = all_comments.find_all("article")
                # /html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[2]/div[1]

    return handler_comments(soup_comments, url)

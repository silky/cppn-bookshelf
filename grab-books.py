#!/usr/bin/env python

import bs4
import requests
import click
import re
import urllib.request
import pandas as pd
import math
import hashlib
from utils import ensure_dir_exists


@click.command()
@click.option("--goodreads_id", default=None,
                help="Goodreads ID, like 1252466.",
                required=True)

@click.option("--shelf",
                default="read",
                help="Shelf to query.",
                required=True)

@click.option("--count",
                default=10,
                help="Maximum number of books to return.",
                required=True)

@click.option("--csv_path",
                default="out.csv",
                help="CSV file in which to save data.",
                required=True)

@click.option("--img_path",
                default="images",
                help="Folder to save images.",
                required=True)
def main (goodreads_id=None, shelf=None, count=None, csv_path=None,
        img_path=None):
    """ Collect book images and titles from Goodreads.
    """

    books = raw_books(goodreads_id, shelf, count)
    data  = book_data(books, img_path)

    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)


def book_data (books, img_path):
    def clean (x):  
        x = x.replace("\r", "").replace("\n", "").replace("\t", "")
        x = re.sub("\s+", " ", x)
        x = x.strip()
        return x

    data = []
    ensure_dir_exists(img_path)

    for i, b in enumerate(books):
        title_elt  = b.find("td", attrs={"class": "field title"}).find("a")
        title      = title_elt.get_text()
        title_link = "https://www.goodreads.com/" + title_elt["href"]
        
        author = b.find("td", attrs={"class": "field author"}).find("a").get_text()
        title   = clean(title)
        
        img = b.find("td", attrs={"class": "field cover"}).find("img")["src"]
        img = img.replace("SX50", "SX200")
        img = img.replace("SY75", "SX200")

        hash = hashlib.md5(title.encode()).hexdigest()
        img_filename = f"{img_path}/{hash}.jpg"

        urllib.request.urlretrieve(img, img_filename)
        print(f"Collected {title} by {author}")

        data.append(
            { "link":   title_link
            , "title":  title
            , "img":    img_filename
            , "author": author
            })

    return data
    

def raw_books (goodreads_id=None, shelf=None, count=None):
    books    = []
    per_page = 30
    n        = math.ceil(count / per_page)
    page     = 1
    base_url = "https://www.goodreads.com/review/list/"

    while page <= n:
        url  = f"{base_url}{goodreads_id}?shelf={shelf}&page={page}&per_page={per_page}"
        resp = requests.get(url)
        html = resp.text

        soup = bs4.BeautifulSoup(html, "html.parser")

        some_books = soup.find_all("tr", attrs={"class": "bookalike review"})

        for b in some_books:
            if len(books) > count:
                break
            books.append(b)

        page  += 1

    return books


if __name__ == "__main__":
    main()

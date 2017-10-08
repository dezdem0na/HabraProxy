from termcolor import colored
from urllib.request import urlopen
from bs4 import BeautifulSoup as Soup

import time
import re
import codecs


def add_trademark(word):
    """
    Adds a trademark to a given word.
    :param word: str
    :return: srt
    """
    symbol = "\u2122"
    return f"{word}{symbol}"


def process_text(text):
    """
    Extracts separate words from a batch of strings.
    Then applies 'add_trademark' function to a word
    if it's length equals 6.
    :param text: srt
    :return: str
    """
    pattern, result = re.compile('([a-zA-Zа-яА-ЯёЁ0-9]+)'), ''
    for word in re.split(pattern, text):
        result += (add_trademark(word)
                   if len(word) == 6 and not word.isdigit()
                   else word)
    return result


def fix_wrong_html_render(soup):
    """
    Fixes wrong html entity render for '&plus;' symbol.
    :param soup: bs4.BeautifulSoup
    :return: None
    """
    for span in soup.findAll("span"):
        for text in span.find_all(text=True):
            fixed_text = text.replace('&plus;', '+')
            text.replace_with(fixed_text)
    for strong in soup.findAll("strong"):
        for text in strong.find_all(text=True):
            fixed_text = text.replace('&plus;', '+')
            text.replace_with(fixed_text)


def modify_absolute_links(soup):
    """
    Removes absolute URLs.
    :param soup: bs4.BeautifulSoup
    :return: None
    """
    for a in soup.findAll("a"):
        if a.get('href'):
            if a.get('href').startswith("https://habrahabr.ru"):
                a['href'] = a['href'].replace("https://habrahabr.ru", '')


def modify_text(url):
    """
    Modifies given text by adding trademark to every
    6th word.
    :param url: str
    :return: bytes
    """
    output = codecs.decode(urlopen(url).read(),
                           encoding='utf-8',
                           errors='strict')
    soup = Soup(output, "html.parser")
    articles = (soup
                .select("div.post__body > div.post__text"))

    for article in articles:
        for piece in article.find_all(text=True):
            piece.replace_with(process_text(piece))

    modify_absolute_links(soup)
    fix_wrong_html_render(soup)

    return soup.encode()


def say_hello(local_host_name, port_number):
    print("\r", time.asctime(),
          colored(f"HTTP Server is starting on "
                  f"{local_host_name}:{port_number}",
                  "green"))


def say_bye():
    print("\r", time.asctime(),
          colored(f"HTTP Server is stopping",
                  "red"))

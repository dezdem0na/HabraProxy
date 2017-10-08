from utils import add_trademark, process_text, modify_text

LOCAL_HOST, LISTEN_PORT = '127.0.0.1', 9000
TARGET_HOST = 'https://habrahabr.ru'


def test_add_trademark():
    word, tm = "foo", "\u2122"
    assert add_trademark(word) == f"{word}{tm}"


def test_process_text():
    tm = "\u2122"
    text = "У Google новые смартфоны, наушники, камера"
    result = f"У Google{tm} новые смартфоны, наушники, камера{tm}"
    assert isinstance(process_text(text), str)
    assert process_text(text) == result


def test_modify_text():
    url = "https://habrahabr.ru"
    assert isinstance(modify_text(url), bytes)

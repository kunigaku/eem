#!/usr/bin/env python

from pyquery import PyQuery as pq

BASE_URL = 'https://ekimemo.wiki.fc2.com'


def read_file(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text


def run_main(filename):
    html_text = read_file(filename)
    html = pq(html_text)
    ol = html('ol')
    lis = ol('li')
    for l in lis:
        li = pq(l)
        a = li('a')
        print(a.text() + "," + BASE_URL + a.attr('href'))


if __name__ == "__main__":
    run_main("list.html")

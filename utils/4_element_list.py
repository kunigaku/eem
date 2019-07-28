#!/usr/bin/env python

from pyquery import PyQuery as pq


def read_file(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text


def parse_file(filename):
    html_text = read_file(filename)
    return parse_html(html_text)


def parse_html(html_text):
    html = pq(html_text)
    tables = find_station_tables(html)
    if len(tables) == 0:
        raise Exception('No table')
    ret = []
    for table in tables:
        elist = get_element_list(table)
        ret.extend(elist)
    return ret


def find_station_tables(html):
    tables = html('table')
    ret = []
    for t in tables:
        table = pq(t)
        if is_station_table(table):
            ret.append(table)
    return ret


def is_station_table(table):
    trs = table('tr')
    for t in trs:
        tr = pq(t)
        ths = tr('th')
        for t in ths:
            th = pq(t)
            if th.text().replace("\n", "").startswith("駅名えきめい"):
                return True
    return False


def get_element_list(table):
    trs = table('tr')
    station_index = 0
    for t in trs:
        tr = pq(t)
        ths = tr('th')
        for index, t in enumerate(ths):
            th = pq(t)
            if th.text().replace("\n", "").startswith("駅名えきめい"):
                station_index = index

    ret = []
    for t in trs:
        tr = pq(t)
        tds = tr('td')
        for index, t in enumerate(tds):
            td = pq(t)
            if index == station_index and td.attr('colspan') is None:
                text = td.text()
                name = text.split("\n")[0]
                element = 'flat'
                if text.find('eco') >= 0:
                    element = 'eco'
                if text.find('heat') >= 0:
                    element = 'heat'
                if text.find('cool') >= 0:
                    element = 'cool'
                ret.append([name, element])
    if len(ret) == 0:
        raise Exception('no station')
    return ret


def run_main(file_num):
    all_stations = []
    for i in range(file_num):
        try:
            filename = str(i) + '.html'
            ret = parse_file(filename)
            add_filename_list = [i + [filename] for i in ret]
            all_stations.extend(add_filename_list)
        except:
            # print(i)
            pass
    # print(all_stations)
    for l in all_stations:
        print(','.join(l))
    # print(len(all_stations))


if __name__ == "__main__":
    run_main(626)
    # print(parse_file('17.html'))

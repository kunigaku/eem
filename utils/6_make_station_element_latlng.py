#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pandas as pd


def read_file(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text


def read_locations(filename):
    text = read_file(filename)
    d = json.loads(text)
    return d


def make_location_dictionary(locations):
    ret = {}
    location_list = locations['stations']
    for record in location_list:
        if ret.get(record['name']) is None:
            ret[record['name']] = []
        ret[record['name']].append(record)
    return ret


def load_location_dictionary():
    locations = read_locations("station_location.json")
    dic = make_location_dictionary(locations)
    print(dic)


def read_elements(filename):
    df = pd.read_csv(filename, names=('name', 'element', 'basefile'))
    df = df.dropna()  # 空行あったわ
    ele_list = df.values
    return [e for e in ele_list if not e[0].startswith('・')]


def make_elements_dctionary(elements):
    ret = {}
    for record in elements:
        name = record[0]
        if ret.get(name) is None:
            ret[name] = record
        else:
            if ret[name][1] != record[1]:
                if ret[name][1] == 'flat':
                    # flatだったら上書きしとくか
                    ret[name] = record
                elif record[1] != 'flat':
                    pass
                    # print("Not match")
                    # print([ret[name], record])
                    # TODO センター南 センター北 薬院 上越妙高 に不一致あり
    return ret


def merge_elements_locations(element_dic, location_dic):
    # print(element_dic)
    ret = []
    nodata = []
    for name, element in element_dic.items():
        location = find_match_location(name, location_dic)
        if location is not None:
            location['wikiname'] = element[0]
            location['element'] = element[1]
            location['base_file'] = element[2]
            ret.append(location)
            # print(location)
        else:
            n = {
                'wikiname': element[0],
                'element': element[1],
                'base_file': element[2]
            }
            nodata.append(n)
    ret_dic = {'stations': ret, 'nodata_stations': nodata}
    return ret_dic


def find_match_location(name, location_dic):
    if location_dic.get(name) is not None:
        location = location_dic[name]
        if len(location) == 1:
            return location[0]
        else:
            if len(uniq_list([l['pref_cd'] for l in location])) == 1:
                # 同じ県だったらそれでいいじゃん。だめ？
                return location[0]
            # TODO 違う駅があるやんけ e_statusで現役を優先
            return location[0]

    kakko = name.split('(')
    if len(kakko) == 2 and len(kakko[0]) > 0:
        name2 = kakko[0]
        note = kakko[1].replace(')', '')
        if location_dic.get(name2) is not None:
            location = location_dic[name2]
            if len(location) == 1:
                return location[0]
            elif len(uniq_list([l['pref_cd'] for l in location])) == 1:
                # 同じ県だったらそれでいいじゃん。だめ？
                return location[0]
            else:
                match_pref = [
                    a for a in location if a['pref'].startswith(note)]
                if len(match_pref) == 1:
                    return match_pref[0]
                if len(match_pref) > 1:
                    # 重複だけどとりあえずOK 池田 追分 北海道
                    # print(note)
                    # print(match_pref)
                    return match_pref[0]
                # if len(match_pref) == 0:
                #     print(name)
                #     print(location)
        else:
            pass
            # print(name + ' ' + name2 + " not found")
    else:
        pass
        # print(name + ' no kakko')

    if name.find('ヶ') >= 0:
        newname = name.replace('ヶ', 'ケ')
        return find_match_location(newname, location_dic)

    # print(name + " not found")
    return None


def uniq_list(l):
    return list(set(l))


if __name__ == "__main__":
    elements = read_elements('element_list.csv')
    element_dic = make_elements_dctionary(elements)

    locations = read_locations("station_location.json")
    location_dic = make_location_dictionary(locations)

    d = merge_elements_locations(element_dic, location_dic)
    j = json.dumps(d, ensure_ascii=False, indent=1)
    print(j)

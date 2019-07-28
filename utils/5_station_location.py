#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import json


def read_csv(filename):
    df = pd.read_csv(filename, encoding="utf-8")
    return df


def read_station(filename):
    df = read_csv(filename)
    df = df[['station_name', 'lat', 'lon', 'pref_cd']]
    df = df.rename(columns={'station_name': 'name',
                            'lat': 'latitude', 'lon': 'longitude'})

    # df['pref'] = "-"

    # for index, item in df.iterrows():
    #     # pref = pref_df[pref_df['pref_cd'] == item['pref_cd']]
    #     # print(pref['pref_name'])
    #     df.loc[index, 'pref'] = 'a'  # pref['pref_name'][0]

    # print(df)

    return df


def read_pref():
    df = read_csv('pref.csv')
    # print(df)
    return df


def run_main(filename):
    pref_df = read_pref()
    df = read_station(filename)

    station_list = [{'name': r['name'],
                     'latitude': r['latitude'],
                     'longitude': r['longitude'],
                     'pref': pref_df[pref_df['pref_cd'] == r['pref_cd']][['pref_name']].iat[0, 0],
                     'pref_cd': r['pref_cd']
                     } for i, r in df.iterrows()]

    station_json = json.dumps(
        {'stations': station_list}, ensure_ascii=False)
    print(station_json)


if __name__ == "__main__":
    run_main("station20190405free.csv")

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:54:50 2024

@author: nice2
"""

import os
import pandas as pd
import numpy as np
import csv

task_3_path = "C:/Users/nice2/Downloads/Re_Mlodszy_inzynier_danych/PP0006_MULTI.csv"

df = pd.read_csv(task_3_path, delimiter=';') 

wybrane_kolumny = df[['Column3', 'Column4', 'Column7', 'Column8']]

wybrane_kolumny = wybrane_kolumny.rename(
    columns={'Column3': 'Indeks', 'Column4': 'Nazwa',
             'Column7': 'Cena', 'Column8': 'Ilosc_w_opakowaniu_i_Grupa_rabatowa'})
wybrane_kolumny['Indeks'] = wybrane_kolumny['Indeks'].str.replace('\s', '', regex=True)
wybrane_kolumny['Nazwa'] = wybrane_kolumny['Nazwa'].str.replace('\s+', ' ', regex=True)


def transform_price_column(price):
    for char in price:
        if char != '0':
            return price[price.index(char):]
    return ''

wybrane_kolumny['Cena'] = wybrane_kolumny['Cena'].apply(transform_price_column)

wybrane_kolumny['Cena'] = wybrane_kolumny['Cena'].apply(lambda x: ''.join([ch if ch.isdigit() else '' for ch in str(x)]) if pd.notnull(x) else '')

wybrane_kolumny['Cena'] = wybrane_kolumny['Cena'].apply(lambda x: x[:-2] + ',' + x[-2:] if len(x) > 2 else x)
wybrane_kolumny['Ilosc_w_opakowaniu'] = wybrane_kolumny['Ilosc_w_opakowaniu_i_Grupa_rabatowa'].str[:5]
wybrane_kolumny['Ilosc_w_opakowaniu'] = wybrane_kolumny['Ilosc_w_opakowaniu'].apply(transform_price_column)
wybrane_kolumny['Ilosc_w_opakowaniu_i_Grupa_rabatowa'] = wybrane_kolumny['Ilosc_w_opakowaniu_i_Grupa_rabatowa'].str.replace('\s', '', regex=True)

wybrane_kolumny['Grupa_rabatowa'] = wybrane_kolumny['Ilosc_w_opakowaniu_i_Grupa_rabatowa'].str[-1]
wybrane_kolumny = wybrane_kolumny.drop('Ilosc_w_opakowaniu_i_Grupa_rabatowa', axis=1)

wybrane_kolumny.to_csv('C:/Users/nice2/Downloads/Re_Mlodszy_inzynier_danych/archive.csv', sep=',', index=False)

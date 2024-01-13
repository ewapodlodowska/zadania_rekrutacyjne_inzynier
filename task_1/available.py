# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:53:52 2024

@author: nice2
"""

import os
import pandas as pd
import numpy as np
import csv

dane=[]

data_path = "C:/Users/nice2/Downloads/Re_Mlodszy_inzynier_danych/first_task/data.csv"
prices_path = "C:/Users/nice2/Downloads/Re_Mlodszy_inzynier_danych/first_task/prices.csv"
quantity_path = "C:/Users/nice2/Downloads/Re_Mlodszy_inzynier_danych/first_task/quantity.csv"
sample_path = "C:/Users/nice2/Downloads/Re_Mlodszy_inzynier_danych/first_task/tabela2.xlsx"

pierwsza_linijka = True

with open(data_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Pomin pierwsza linijke
        if pierwsza_linijka:
            pierwsza_linijka = False
            continue

        #pierwsze siedem znakow jako pierwsza kolumna, reszta jako druga
        kolumna1 = line[:7]
        kolumna2 = line[7:].strip()  # Usun biale znaki na koncu linii

        # Dodaj dane do listy
        dane.append([kolumna1, kolumna2])


data = pd.DataFrame(dane, columns=['part_number', 'manufacturer'])


dane=[]
pierwsza_linijka = True

with open(prices_path, 'r', encoding='utf-8') as file:
    for line in file:
        
        if pierwsza_linijka:
            pierwsza_linijka = False
            continue

        kolumna1 = line[:7]
        kolumna2 = line[7:].strip()  

        
        dane.append([kolumna1, kolumna2])


prices = pd.DataFrame(dane, columns=['part_number', 'price'])


dane=[]

with open(quantity_path, 'r', encoding='utf-8') as file:
    for line in file:
         
        kolumna1 = line[:7]
        kolumna2 = line[7:].strip()  

        
        dane.append([kolumna1, kolumna2])


quantity = pd.DataFrame(dane, columns=['part_number', 'quantity'])

merged_df = pd.merge(data, prices, on='part_number', how='outer')
merged_df = pd.merge(merged_df, quantity, on='part_number', how='outer')
merged_df = merged_df.dropna()
merged_df['quantity'] = merged_df['quantity'].astype('category')

#print(merged_df["quantity"].cat.categories)
# wszystkie sa dostepne

merged_df['price'] = merged_df['price'].str.replace(',', '.')

merged_df['price'] = pd.to_numeric(merged_df['price'], errors='coerce')

merged_df = merged_df.loc[merged_df['price'] > 0]

merged_df['quantity'] = merged_df['quantity'].replace('>10', '20')

merged_df['quantity'] = pd.to_numeric(merged_df['quantity'], errors='coerce')
grouped_df = merged_df.groupby(['part_number', 'manufacturer', 'price'], as_index=False)['quantity'].agg('sum')
grouped_df['quantity'] = np.where(grouped_df['quantity'] > 10, 20, grouped_df['quantity'])
grouped_df['quantity'] = grouped_df['quantity'].astype(str)

grouped_df['quantity'] = grouped_df['quantity'].replace('20', '>10')


#grouped_df.to_csv('C:/Users/nice2/Downloads/Re_Mlodszy_inzynier_danych/first_task/price_list.csv', sep=',', index=False, decimal=',')

grouped_df['manufacturer'] = grouped_df['manufacturer'].astype('category')

sum_quantity_by_manufacturer = grouped_df.groupby('manufacturer').size().reset_index()
sum_quantity_by_manufacturer = sum_quantity_by_manufacturer.rename(columns={0: 'quantity'})

#sum_quantity_by_manufacturer.to_csv('C:/Users/nice2/Downloads/Re_Mlodszy_inzynier_danych/first_task/manufacturer_report.csv', sep=',', index=False, decimal=',')


sample = pd.read_excel(sample_path)


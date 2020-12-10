# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 22:09:29 2020

@author: adamisch

Example that gets the daily readings and the text of the readings for the Greek Orthodox Church in America
"""

from orthodoxcalendars import text
import re

from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import copy

key = pd.read_csv(
    "https://raw.githubusercontent.com/adamisch/orthodoxcalendars/main/bible_data/key_english.csv")

kjv = pd.read_csv(
    "https://raw.githubusercontent.com/adamisch/orthodoxcalendars/main/bible_data/t_kjv.csv")


with open('C:\\Users\\adamisch\\Documents\\Python Scripts\\Church\\Calendars\\GOA\\2021goa.txt', 'rb') as cal_goa:
    soup_goa = bs(cal_goa, 'html.parser')

for x in soup_goa.find_all():
    if len(x.get_text(strip=True)) == 0:
        x.extract()

dates_goa = soup_goa.find_all('li', {'class': 'cal-day'})

date_names_goa = [x.find('span', {'class': 'date mobile'}).text.strip(
) for x in dates_goa if x.find('span', {'class': 'date mobile'})]

readings_goa = [[re.findall('(?<=–\r\n\r\n).*', x.text)[0].strip()
                 for x in my_date.find_all('li', {'class': 'sub-event sr block'})
                 if len(re.findall('(?<=–\r\n\r\n).*', x.text)) > 0]
                for my_date in dates_goa if my_date.find_all('li', {'class': 'sub-event sr block'})]


goa_dict = dict(zip(date_names_goa, readings_goa))

df_goa = pd.DataFrame.from_dict(goa_dict, orient='index').reset_index().rename(
    {'index': 'Date', 0: 'Reading1', 1: 'Reading2', 2: 'Reading3'}, axis='columns')
df_goa.replace({'III ': '3 ', 'II ': '2 ', 'I ': '1 ',
                'Matt. ': 'Matthew ', 'Jud. ': 'Jude '}, inplace=True, regex=True)


### Work in progress: Avoiding this step ###

# At this point, copy the df_goa DataFrame into a CSV.
# Separate out any readings that are strung together (in particular, Holy Thursday)

df_goa_manual = pd.read_csv(
    'https://raw.githubusercontent.com/adamisch/orthodoxcalendars/main/goa_files/manualgoa.csv')

df_goa_manual = df_goa_manual.replace({np.nan: None})

# Find the row that has the twelve passion gospels, delete reading2
# passion_row = df_goa[df_goa.apply(lambda r: r.str.contains('Twelve',
#                                                           case=False).any(),
#                                  axis = 1)].index.astype(int)[-1]
# passion_gospel_col = [x for x in df_goa.columns if str(x).startswith("Reading")][-1]

# df_goa[passion_gospel_col].iloc[passion_row] = None

# df_goa_manual= copy.deepcopy(df_goa)
### End Work in progress ###

df_goa_manual=text.text_columns(df_goa_manual, key = key, bible = kjv)

cal_df=copy.deepcopy(df_goa_manual)

cal_df=cal_df[['Date', 'Reading1', 'Text1', 'Reading2', 'Text2',
                 'Reading3', 'Text3', 'Reading4', 'Text4', 'Reading5',
                 'Text5', 'Reading6', 'Text6', 'Reading7', 'Text7']]

cal_df = cal_df.stack().reset_index()
cal_df = cal_df[cal_df[0] != " "]

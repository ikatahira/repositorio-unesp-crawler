# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def clean_text(text:str, regex_rules:list = []):
    text = text.strip().upper()
    for rule in regex_rules:
        text = re.sub(rule, '', text)
    return text

def get_keywords():
    offset = 0
    npp = 10000
    
    keywords = {}
    
    while(True):
        html = ''
        url = 'https://repositorio.unesp.br/browse?rpp='+str(npp)+'&sort_by=-1&type=subject&offset='+str(offset)+'&etal=-1&order=ASC'
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        num_max = soup.find('p', attrs={"class": "pagination-info"}).text.split('de')[-1]
        
        print('----')
        print('url: ' + url)
        print('offset: ' + str(offset))
        print('npp: ' + str(npp))
        print('max_items:' + num_max)
        print('items: ' + str(len(keywords)))
        
        for kw in soup.find_all('td', attrs={"class": "ds-table-cell odd"}):
            if kw.a.text not in keywords.keys():
                keywords[kw.a.text] = 1
            else:
                keywords[kw.a.text] += 1
        offset += npp
        if offset > int(num_max):
            break;
    return keywords.keys()

def select_keywords(keywords:list, min_lenght:int = 0, regex_rules:list = []):
    result = []
    for kw in keywords:
        kw = clean_text(kw, regex_rules)
        if len(kw) > 0 and len(kw) >= min_lenght:
            if kw not in result:
                result.append(kw)
    return result

keywords = get_keywords()
sel = select_keywords(keywords, 3, [r'"', r'^[0-9]+', r'^[0-9]+\-[0-9]+'])

df_keywords = pd.DataFrame(keywords, columns=['Termos'])
df_keywords.sort_values(by=['Termos']).to_excel(excel_writer='./data/products/keywords.xlsx', index=False)

df_sel_keywords = pd.DataFrame(sel, columns=['Termos'])
df_sel_keywords.sort_values(by=['Termos']).to_excel(excel_writer='./data/products/selected_keywords.xlsx', index=False)


